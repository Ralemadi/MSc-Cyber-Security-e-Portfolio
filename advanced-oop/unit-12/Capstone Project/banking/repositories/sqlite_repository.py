from __future__ import annotations
import sqlite3
from contextlib import closing, contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator

from banking.domain.models import (
    Account,
    AccountStatus,
    Customer,
    Transaction,
    TransactionStatus,
    TransactionType,
)
from banking.domain.money import Money
from banking.exceptions import (
    AccountNotFoundError,
    AccountStatusError,
    DuplicateEmailError,
    DuplicateUsernameError,
    InsufficientFundsError,
    RepositoryError,
)
from banking.repositories.interfaces import BankRepository
from banking.security.roles import UserRole


class SQLiteBankRepository(BankRepository):
    #SQLite implementation with atomic transaction helpers.

    #Initialise this component with its required dependencies and local state.
    def __init__(self, db_path: str | Path) -> None:
        path = Path(db_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        self.db_path = str(path)
        self._initialise_schema()

    #Open a configured SQLite connection with foreign keys and WAL enabled.
    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(
            self.db_path,
            timeout=30,
            isolation_level=None,
        )
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA journal_mode = WAL")
        return conn

    #Wrap SQLite changes in BEGIN IMMEDIATE, COMMIT and ROLLBACK semantics.
    @contextmanager
    def _transaction(self) -> Iterator[sqlite3.Connection]:
        #Guarantee BEGIN/COMMIT/ROLLBACK in one reusable context manager.
        conn = self._connect()

        try:
            #Acquire the write transaction before changing related financial state.
            conn.execute("BEGIN IMMEDIATE")
            yield conn
            #Commit only after every operation inside the transaction completes successfully.
            conn.execute("COMMIT")
        #Any failure rolls back the complete transaction so partial balance changes are not preserved.
        except Exception:
            conn.execute("ROLLBACK")
            raise
        finally:
            conn.close()

    #Create the database schema and migrate login-lockout columns when required.
    def _initialise_schema(self) -> None:
        with closing(self._connect()) as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS customers (
                    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE COLLATE NOCASE,
                    full_name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE COLLATE NOCASE,
                    role TEXT NOT NULL
                        CHECK(role IN (
                            'CUSTOMER',
                            'BANK_STAFF',
                            'ADMINISTRATOR'
                        )),
                    enabled INTEGER NOT NULL DEFAULT 1
                        CHECK(enabled IN (0, 1)),
                    failed_login_attempts INTEGER NOT NULL DEFAULT 0
                        CHECK(failed_login_attempts >= 0),
                    locked_until TEXT,
                    pin_salt_hex TEXT NOT NULL,
                    pin_hash_hex TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS accounts (
                    account_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_id INTEGER NOT NULL,
                    account_type TEXT NOT NULL
                        CHECK(account_type IN ('CURRENT', 'SAVINGS', 'SALARY')),
                    balance_cents INTEGER NOT NULL CHECK(balance_cents >= 0),
                    status TEXT NOT NULL DEFAULT 'ACTIVE'
                        CHECK(status IN ('ACTIVE', 'FROZEN', 'CLOSED')),
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
                );

                CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    transaction_type TEXT NOT NULL
                        CHECK(transaction_type IN (
                            'OPENING_BALANCE',
                            'DEPOSIT',
                            'WITHDRAWAL',
                            'TRANSFER'
                        )),
                    from_account_id INTEGER,
                    to_account_id INTEGER,
                    amount_cents INTEGER NOT NULL CHECK(amount_cents > 0),
                    status TEXT NOT NULL
                        CHECK(status IN ('COMPLETED', 'FAILED', 'REJECTED')),
                    description TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );

                CREATE INDEX IF NOT EXISTS idx_accounts_customer
                    ON accounts(customer_id);

                CREATE INDEX IF NOT EXISTS idx_transactions_from_date
                    ON transactions(from_account_id, created_at);

                CREATE INDEX IF NOT EXISTS idx_transactions_to
                    ON transactions(to_account_id);
                """
            )

            columns = {
                row["name"]
                for row in conn.execute(
                    "PRAGMA table_info(customers)"
                ).fetchall()
            }

            if "failed_login_attempts" not in columns:
                conn.execute(
                    """
                    ALTER TABLE customers
                    ADD COLUMN failed_login_attempts INTEGER NOT NULL DEFAULT 0
                    """
                )

            if "locked_until" not in columns:
                conn.execute(
                    """
                    ALTER TABLE customers
                    ADD COLUMN locked_until TEXT
                    """
                )

    #Convert the SQLite row into the customer domain representation.
    @staticmethod
    def _to_customer(row: sqlite3.Row) -> Customer:
        locked_until_raw = row["locked_until"]

        return Customer(
            customer_id=row["customer_id"],
            username=row["username"],
            full_name=row["full_name"],
            email=row["email"],
            role=UserRole(row["role"]),
            enabled=bool(row["enabled"]),
            failed_login_attempts=row["failed_login_attempts"],
            locked_until=(
                datetime.fromisoformat(locked_until_raw)
                if locked_until_raw
                else None
            ),
        )

    #Convert the SQLite row into the account domain representation.
    @staticmethod
    def _to_account(row: sqlite3.Row) -> Account:
        return Account(
            account_id=row["account_id"],
            customer_id=row["customer_id"],
            account_type=row["account_type"],
            balance=Money.from_cents(row["balance_cents"]),
            status=AccountStatus(row["status"]),
            created_at=datetime.fromisoformat(row["created_at"]),
        )

    #Convert the SQLite row into the transaction domain representation.
    @staticmethod
    def _to_transaction(row: sqlite3.Row) -> Transaction:
        return Transaction(
            transaction_id=row["transaction_id"],
            transaction_type=TransactionType(row["transaction_type"]),
            from_account_id=row["from_account_id"],
            to_account_id=row["to_account_id"],
            amount=Money.from_cents(row["amount_cents"]),
            status=TransactionStatus(row["status"]),
            description=row["description"],
            created_at=datetime.fromisoformat(row["created_at"]),
        )

    #Perform the internal require active row step used by this workflow.
    @staticmethod
    def _require_active_row(
        row: sqlite3.Row,
        operation: str,
    ) -> None:
        if row["status"] != AccountStatus.ACTIVE.value:
            raise AccountStatusError(
                f"{operation} is not allowed because the account "
                f"is {row['status']}."
            )

    #Validate and create the requested customer through this responsibility boundary.
    def create_customer(
        self,
        username: str,
        full_name: str,
        email: str,
        pin_salt_hex: str,
        pin_hash_hex: str,
        role: UserRole,
        enabled: bool = True,
    ) -> Customer:
        with closing(self._connect()) as conn:
            try:
                cursor = conn.execute(
                    """
                    INSERT INTO customers(
                        username,
                        full_name,
                        email,
                        role,
                        enabled,
                        pin_salt_hex,
                        pin_hash_hex
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        username,
                        full_name,
                        email,
                        role.value,
                        int(enabled),
                        pin_salt_hex,
                        pin_hash_hex,
                    ),
                )
            except sqlite3.IntegrityError as exc:
                message = str(exc).lower()

                if "username" in message:
                    raise DuplicateUsernameError(
                        "This username already exists."
                    ) from exc

                if "email" in message:
                    raise DuplicateEmailError(
                        "This email address already exists."
                    ) from exc

                raise RepositoryError(
                    "User could not be created."
                ) from exc

        customer = self.get_customer(cursor.lastrowid)

        if customer is None:
            raise RepositoryError(
                "User creation could not be verified."
            )

        return customer

    #Retrieve the requested customer without exposing persistence details to callers.
    def get_customer(
        self,
        customer_id: int,
    ) -> Customer | None:
        with closing(self._connect()) as conn:
            row = conn.execute(
                """
                SELECT customer_id, username, full_name, email, role, enabled,
                       failed_login_attempts, locked_until
                FROM customers
                WHERE customer_id = ?
                """,
                (customer_id,),
            ).fetchone()

        return self._to_customer(row) if row else None

    #Retrieve the requested customer by username without exposing persistence details to callers.
    def get_customer_by_username(
        self,
        username: str,
    ) -> sqlite3.Row | None:
        with closing(self._connect()) as conn:
            return conn.execute(
                "SELECT * FROM customers WHERE username = ? COLLATE NOCASE",
                (username,),
            ).fetchone()

    #Retrieve the requested customer by email without exposing persistence details to callers.
    def get_customer_by_email(
        self,
        email: str,
    ) -> sqlite3.Row | None:
        with closing(self._connect()) as conn:
            return conn.execute(
                "SELECT * FROM customers WHERE email = ? COLLATE NOCASE",
                (email,),
            ).fetchone()

    #Return the authorised collection of customers records.
    def list_customers(self) -> list[Customer]:
        with closing(self._connect()) as conn:
            rows = conn.execute(
                """
                SELECT customer_id, username, full_name, email, role, enabled,
                       failed_login_attempts, locked_until
                FROM customers
                ORDER BY
                    CASE role
                        WHEN 'ADMINISTRATOR' THEN 0
                        WHEN 'BANK_STAFF' THEN 1
                        ELSE 2
                    END,
                    username
                """
            ).fetchall()

        return [self._to_customer(row) for row in rows]

    #Persist the requested customer enabled change and return controlled results.
    def update_customer_enabled(
        self,
        customer_id: int,
        enabled: bool,
    ) -> Customer:
        with closing(self._connect()) as conn:
            cursor = conn.execute(
                "UPDATE customers SET enabled = ? WHERE customer_id = ?",
                (int(enabled), customer_id),
            )

            if cursor.rowcount != 1:
                raise RepositoryError(
                    "The requested user does not exist."
                )

        customer = self.get_customer(customer_id)

        if customer is None:
            raise RepositoryError(
                "User status update could not be verified."
            )

        return customer

    #Persist the requested customer role change and return controlled results.
    def update_customer_role(
        self,
        customer_id: int,
        role: UserRole,
    ) -> Customer:
        with closing(self._connect()) as conn:
            cursor = conn.execute(
                "UPDATE customers SET role = ? WHERE customer_id = ?",
                (role.value, customer_id),
            )

            if cursor.rowcount != 1:
                raise RepositoryError(
                    "The requested user does not exist."
                )

        customer = self.get_customer(customer_id)

        if customer is None:
            raise RepositoryError(
                "Role update could not be verified."
            )

        return customer

    #Persist the requested customer password change and return controlled results.
    def update_customer_password(
        self,
        customer_id: int,
        pin_salt_hex: str,
        pin_hash_hex: str,
    ) -> None:
        with closing(self._connect()) as conn:
            cursor = conn.execute(
                """
                UPDATE customers
                SET pin_salt_hex = ?, pin_hash_hex = ?
                WHERE customer_id = ?
                """,
                (
                    pin_salt_hex,
                    pin_hash_hex,
                    customer_id,
                ),
            )

            if cursor.rowcount != 1:
                raise RepositoryError(
                    "The requested user does not exist."
                )

    #Atomically increment and return the persisted failed-login counter for the identity.
    def increment_failed_login_attempts(
        self,
        customer_id: int,
    ) -> int:
        with self._transaction() as conn:
            cursor = conn.execute(
                """
                UPDATE customers
                SET failed_login_attempts = failed_login_attempts + 1
                WHERE customer_id = ?
                """,
                (customer_id,),
            )

            if cursor.rowcount != 1:
                raise RepositoryError(
                    "The requested user does not exist."
                )

            row = conn.execute(
                """
                SELECT failed_login_attempts
                FROM customers
                WHERE customer_id = ?
                """,
                (customer_id,),
            ).fetchone()

        if row is None:
            raise RepositoryError(
                "Failed-login update could not be verified."
            )

        return int(row["failed_login_attempts"])

    #Apply the requested customer lockout state change through the owning component.
    def set_customer_lockout(
        self,
        customer_id: int,
        locked_until: datetime,
    ) -> Customer:
        with closing(self._connect()) as conn:
            cursor = conn.execute(
                """
                UPDATE customers
                SET failed_login_attempts = 0,
                    locked_until = ?
                WHERE customer_id = ?
                """,
                (
                    locked_until.astimezone(timezone.utc).isoformat(),
                    customer_id,
                ),
            )

            if cursor.rowcount != 1:
                raise RepositoryError(
                    "The requested user does not exist."
                )

        customer = self.get_customer(customer_id)

        if customer is None:
            raise RepositoryError(
                "Temporary lockout could not be verified."
            )

        return customer

    #Clear the current customer login security state in a controlled way.
    def clear_customer_login_security(
        self,
        customer_id: int,
    ) -> Customer:
        with closing(self._connect()) as conn:
            cursor = conn.execute(
                """
                UPDATE customers
                SET failed_login_attempts = 0,
                    locked_until = NULL
                WHERE customer_id = ?
                """,
                (customer_id,),
            )

            if cursor.rowcount != 1:
                raise RepositoryError(
                    "The requested user does not exist."
                )

        customer = self.get_customer(customer_id)

        if customer is None:
            raise RepositoryError(
                "Login security reset could not be verified."
            )

        return customer

    #Validate and create the requested account through this responsibility boundary.
    def create_account(
        self,
        customer_id: int,
        account_type: str,
        initial_balance: Money,
    ) -> Account:
        created_at = datetime.now(timezone.utc).isoformat()

        with closing(self._connect()) as conn:
            cursor = conn.execute(
                """
                INSERT INTO accounts(
                    customer_id,
                    account_type,
                    balance_cents,
                    status,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    customer_id,
                    account_type,
                    initial_balance.cents,
                    AccountStatus.ACTIVE.value,
                    created_at,
                ),
            )
            account_id = cursor.lastrowid

            if initial_balance.cents > 0:
                conn.execute(
                    """
                    INSERT INTO transactions(
                        transaction_type,
                        from_account_id,
                        to_account_id,
                        amount_cents,
                        status,
                        description,
                        created_at
                    )
                    VALUES (?, NULL, ?, ?, ?, ?, ?)
                    """,
                    (
                        TransactionType.OPENING_BALANCE.value,
                        account_id,
                        initial_balance.cents,
                        TransactionStatus.COMPLETED.value,
                        "Initial account funding",
                        created_at,
                    ),
                )

        account = self.get_account(account_id)

        if account is None:
            raise RepositoryError(
                "Account creation could not be verified."
            )

        return account

    #Retrieve the requested account without exposing persistence details to callers.
    def get_account(
        self,
        account_id: int,
    ) -> Account | None:
        with closing(self._connect()) as conn:
            row = conn.execute(
                "SELECT * FROM accounts WHERE account_id = ?",
                (account_id,),
            ).fetchone()

        return self._to_account(row) if row else None

    #Return the authorised collection of accounts for customer records.
    def list_accounts_for_customer(
        self,
        customer_id: int,
    ) -> list[Account]:
        with closing(self._connect()) as conn:
            rows = conn.execute(
                """
                SELECT * FROM accounts
                WHERE customer_id = ?
                ORDER BY account_id
                """,
                (customer_id,),
            ).fetchall()

        return [self._to_account(row) for row in rows]

    #Return the authorised collection of all accounts records.
    def list_all_accounts(self) -> list[Account]:
        with closing(self._connect()) as conn:
            rows = conn.execute(
                "SELECT * FROM accounts ORDER BY customer_id, account_id"
            ).fetchall()

        return [self._to_account(row) for row in rows]

    #Persist the requested account status change and return controlled results.
    def update_account_status(
        self,
        account_id: int,
        status: AccountStatus,
    ) -> Account:
        with closing(self._connect()) as conn:
            cursor = conn.execute(
                "UPDATE accounts SET status = ? WHERE account_id = ?",
                (status.value, account_id),
            )

            if cursor.rowcount != 1:
                raise AccountNotFoundError(
                    "The requested account does not exist."
                )

        account = self.get_account(account_id)

        if account is None:
            raise AccountNotFoundError(
                "The requested account does not exist."
            )

        return account

    #Validate authorization and account state before applying the deposit.
    def deposit(
        self,
        account_id: int,
        amount: Money,
        description: str,
    ) -> Account:
        created_at = datetime.now(timezone.utc).isoformat()

        with self._transaction() as conn:
            row = conn.execute(
                "SELECT balance_cents, status FROM accounts WHERE account_id = ?",
                (account_id,),
            ).fetchone()

            if row is None:
                raise AccountNotFoundError(
                    "The requested account does not exist."
                )

            self._require_active_row(row, "Deposit")

            conn.execute(
                """
                UPDATE accounts
                SET balance_cents = balance_cents + ?
                WHERE account_id = ?
                """,
                (amount.cents, account_id),
            )

            conn.execute(
                """
                INSERT INTO transactions(
                    transaction_type,
                    from_account_id,
                    to_account_id,
                    amount_cents,
                    status,
                    description,
                    created_at
                )
                VALUES (?, NULL, ?, ?, ?, ?, ?)
                """,
                (
                    TransactionType.DEPOSIT.value,
                    account_id,
                    amount.cents,
                    TransactionStatus.COMPLETED.value,
                    description,
                    created_at,
                ),
            )

        account = self.get_account(account_id)

        if account is None:
            raise RepositoryError(
                "Deposit result could not be verified."
            )

        return account

    #Validate authorization, account state and funds before applying the withdrawal.
    def withdraw(
        self,
        account_id: int,
        amount: Money,
        description: str,
    ) -> Account:
        created_at = datetime.now(timezone.utc).isoformat()

        with self._transaction() as conn:
            row = conn.execute(
                "SELECT balance_cents, status FROM accounts WHERE account_id = ?",
                (account_id,),
            ).fetchone()

            if row is None:
                raise AccountNotFoundError(
                    "The requested account does not exist."
                )

            self._require_active_row(row, "Withdrawal")

            if row["balance_cents"] < amount.cents:
                raise InsufficientFundsError(
                    "Insufficient funds."
                )

            conn.execute(
                """
                UPDATE accounts
                SET balance_cents = balance_cents - ?
                WHERE account_id = ?
                """,
                (amount.cents, account_id),
            )

            conn.execute(
                """
                INSERT INTO transactions(
                    transaction_type,
                    from_account_id,
                    to_account_id,
                    amount_cents,
                    status,
                    description,
                    created_at
                )
                VALUES (?, ?, NULL, ?, ?, ?, ?)
                """,
                (
                    TransactionType.WITHDRAWAL.value,
                    account_id,
                    amount.cents,
                    TransactionStatus.COMPLETED.value,
                    description,
                    created_at,
                ),
            )

        account = self.get_account(account_id)

        if account is None:
            raise RepositoryError(
                "Withdrawal result could not be verified."
            )

        return account

    #Execute the coordinated transfer workflow through policy, fraud, persistence and notification controls.
    def transfer(
        self,
        from_account_id: int,
        to_account_id: int,
        amount: Money,
        description: str,
    ) -> Transaction:
        created_at = datetime.now(timezone.utc).isoformat()

        with self._transaction() as conn:
            from_row = conn.execute(
                "SELECT balance_cents, status FROM accounts WHERE account_id = ?",
                (from_account_id,),
            ).fetchone()
            to_row = conn.execute(
                "SELECT balance_cents, status FROM accounts WHERE account_id = ?",
                (to_account_id,),
            ).fetchone()

            if from_row is None:
                raise AccountNotFoundError(
                    "Source account does not exist."
                )

            if to_row is None:
                raise AccountNotFoundError(
                    "Destination account does not exist."
                )

            self._require_active_row(from_row, "Transfer")
            self._require_active_row(to_row, "Transfer")

            if from_row["balance_cents"] < amount.cents:
                raise InsufficientFundsError(
                    "Insufficient funds for transfer."
                )

            conn.execute(
                """
                UPDATE accounts
                SET balance_cents = balance_cents - ?
                WHERE account_id = ?
                """,
                (amount.cents, from_account_id),
            )
            conn.execute(
                """
                UPDATE accounts
                SET balance_cents = balance_cents + ?
                WHERE account_id = ?
                """,
                (amount.cents, to_account_id),
            )
            cursor = conn.execute(
                """
                INSERT INTO transactions(
                    transaction_type,
                    from_account_id,
                    to_account_id,
                    amount_cents,
                    status,
                    description,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    TransactionType.TRANSFER.value,
                    from_account_id,
                    to_account_id,
                    amount.cents,
                    TransactionStatus.COMPLETED.value,
                    description,
                    created_at,
                ),
            )
            transaction_id = cursor.lastrowid

        with closing(self._connect()) as conn:
            row = conn.execute(
                "SELECT * FROM transactions WHERE transaction_id = ?",
                (transaction_id,),
            ).fetchone()

        if row is None:
            raise RepositoryError(
                "Transfer transaction could not be verified."
            )

        return self._to_transaction(row)

    #Return the authorised collection of transactions for account records.
    def list_transactions_for_account(
        self,
        account_id: int,
    ) -> list[Transaction]:
        with closing(self._connect()) as conn:
            rows = conn.execute(
                """
                SELECT * FROM transactions
                WHERE from_account_id = ? OR to_account_id = ?
                ORDER BY transaction_id DESC
                """,
                (account_id, account_id),
            ).fetchall()

        return [self._to_transaction(row) for row in rows]

    #Calculate the stored outgoing transfers since value needed by the policy check.
    def sum_outgoing_transfers_since(
        self,
        account_id: int,
        since: datetime,
    ) -> Money:
        with closing(self._connect()) as conn:
            row = conn.execute(
                """
                SELECT COALESCE(SUM(amount_cents), 0) AS total
                FROM transactions
                WHERE transaction_type = ?
                  AND status = ?
                  AND from_account_id = ?
                  AND created_at >= ?
                """,
                (
                    TransactionType.TRANSFER.value,
                    TransactionStatus.COMPLETED.value,
                    account_id,
                    since.isoformat(),
                ),
            ).fetchone()

        return Money.from_cents(int(row["total"]))
