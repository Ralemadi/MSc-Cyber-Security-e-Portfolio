from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Protocol
from banking.domain.money import Money
from banking.security.roles import UserRole


#Enumerate the supported ACTIVE, FROZEN and CLOSED account states
class AccountStatus(str, Enum):
    ACTIVE = "ACTIVE"
    FROZEN = "FROZEN"
    CLOSED = "CLOSED"


#Enumerate the supported opening-balance, deposit, withdrawal and transfer transaction types
class TransactionType(str, Enum):
    OPENING_BALANCE = "OPENING_BALANCE"
    DEPOSIT = "DEPOSIT"
    WITHDRAWAL = "WITHDRAWAL"
    TRANSFER = "TRANSFER"


#Enumerate the supported transaction completion states
class TransactionStatus(str, Enum):
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    REJECTED = "REJECTED"


#Define the Visitor contract implemented by reporting components.
class BankEntityVisitor(Protocol):
    #Visitor Pattern contract for reporting over domain entities.

    #Accumulate summary information from the visited account entity.
    def visit_account(self, account: "Account") -> None:
        ...

    #Accumulate summary information from the visited transaction entity.
    def visit_transaction(self, transaction: "Transaction") -> None:
        ...


#Represent an authenticated system identity and its current authentication-security state.
@dataclass(frozen=True)
class Customer:
    #Authenticated system user

    customer_id: int
    username: str
    full_name: str
    email: str
    role: UserRole
    enabled: bool = True
    failed_login_attempts: int = 0
    locked_until: datetime | None = None

    #Report whether the current object satisfies the customer condition.
    @property
    def is_customer(self) -> bool:
        return self.role == UserRole.CUSTOMER

    #Report whether the current object satisfies the bank staff condition.
    @property
    def is_bank_staff(self) -> bool:
        return self.role == UserRole.BANK_STAFF

    #Report whether the current object satisfies the administrator condition.
    @property
    def is_administrator(self) -> bool:
        return self.role == UserRole.ADMINISTRATOR

    #Report whether the current object satisfies the admin condition.
    @property
    def is_admin(self) -> bool:
        #Compatibility alias for presentation helpers.
        return self.is_administrator

    #Report whether the current object satisfies the temporarily locked condition.
    @property
    def is_temporarily_locked(self) -> bool:
        return (
            self.locked_until is not None
            and self.locked_until > datetime.now(timezone.utc)
        )

    #Build the Administrator-facing status text from enablement and temporary-lockout state.
    @property
    def status_description(self) -> str:
        lock_text = None

        if self.is_temporarily_locked:
            lock_text = (
                "TEMP LOCKED until "
                f"{self.locked_until.astimezone(timezone.utc):%H:%M UTC}"
            )

        if not self.enabled and lock_text:
            return f"DISABLED / {lock_text}"

        if not self.enabled:
            return "DISABLED"

        if lock_text:
            return lock_text

        return "ENABLED"


#Represent one CUSTOMER-owned bank account and its current balance and status.
@dataclass(frozen=True)
class Account:
    account_id: int
    customer_id: int
    account_type: str
    balance: Money
    status: AccountStatus
    created_at: datetime

    #Expose the account balance as integer cents for persistence and reporting calculations.
    @property
    def balance_cents(self) -> int:
        #Compatibility property for persistence/reporting calculations.
        return self.balance.cents

    #Dispatch this domain object to the matching Visitor method without embedding reporting logic in the model.
    def accept(self, visitor: BankEntityVisitor) -> None:
        visitor.visit_account(self)


#Represent one immutable banking transaction record.
@dataclass(frozen=True)
class Transaction:
    transaction_id: int
    transaction_type: TransactionType
    from_account_id: int | None
    to_account_id: int | None
    amount: Money
    status: TransactionStatus
    description: str
    created_at: datetime

    #Expose the transaction amount as integer cents for calculations and tests.
    @property
    def amount_cents(self) -> int:
        #Compatibility property for calculations and tests.
        return self.amount.cents

    #Dispatch this domain object to the matching Visitor method without embedding reporting logic in the model.
    def accept(self, visitor: BankEntityVisitor) -> None:
        visitor.visit_transaction(self)
