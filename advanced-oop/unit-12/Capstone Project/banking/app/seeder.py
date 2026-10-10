from __future__ import annotations
import random
from dataclasses import dataclass
from banking.domain.models import Customer, TransactionType
from banking.patterns.decorators import TransferComponent
from banking.security.roles import UserRole
from banking.services.account_service import AccountService
from banking.services.customer_service import CustomerService


#Hold the deterministic seed identity data used to build one demo account profile
@dataclass(frozen=True)
class SeedUser:
    username: str
    full_name: str
    email: str
    password: str
    role: UserRole
    account_types: tuple[str, ...]


#Create deterministic demonstration identities, accounts and transactions
class DemoDataSeeder:
    #Reproducible educational seed data kept outside production workflows

    RANDOM_SEED = 20260925

    DEFAULT_USERS = (
        SeedUser(
            "admin",
            "BankSecure Administrator",
            "admin@banksecure.local",
            "P@ssw0rdQTR!@#",
            UserRole.ADMINISTRATOR,
            (),
        ),
        SeedUser(
            "staff1",
            "Demo Bank Staff",
            "staff1@banksecure.local",
            "StaffQWE!@#",
            UserRole.BANK_STAFF,
            (),
        ),
        SeedUser(
            "user1",
            "Demo User 1",
            "user1@banksecure.local",
            "qweQWE!@#",
            UserRole.CUSTOMER,
            ("CURRENT", "SAVINGS"),
        ),
        SeedUser(
            "user2",
            "Demo User 2",
            "user2@banksecure.local",
            "qweQWE!@#",
            UserRole.CUSTOMER,
            ("SALARY", "CURRENT"),
        ),
        SeedUser(
            "user3",
            "Demo User 3",
            "user3@banksecure.local",
            "qweQWE!@#",
            UserRole.CUSTOMER,
            ("SAVINGS", "SALARY"),
        ),
    )

    #Initialise this component with its required dependencies and local state
    def __init__(
        self,
        customer_service: CustomerService,
        account_service: AccountService,
        transfer_service: TransferComponent,
    ) -> None:
        self.customer_service = customer_service
        self.account_service = account_service
        self.transfer_service = transfer_service
        self.random = random.Random(self.RANDOM_SEED)

    #Populate the demo database only when the expected seeded identities are not already present
    def seed(self) -> None:
        customers = self._seed_identities_and_accounts()
        self._seed_activity(customers)

    #Perform the internal seed identities and accounts step used by this workflow
    def _seed_identities_and_accounts(
        self,
    ) -> list[Customer]:
        customers: list[Customer] = []

        for definition in self.DEFAULT_USERS:
            customer = self.customer_service.get_customer_by_username(
                definition.username
            )

            if customer is None:
                customer = self.customer_service.register_customer(
                    username=definition.username,
                    full_name=definition.full_name,
                    email=definition.email,
                    password=definition.password,
                    role=definition.role,
                )

            customers.append(customer)

            if customer.role != UserRole.CUSTOMER:
                continue

            existing_types = {
                item.account_type
                for item in self.account_service.list_accounts(
                    customer.customer_id
                )
            }

            for account_type in definition.account_types:
                if account_type in existing_types:
                    continue

                self.account_service.create_account(
                    customer_id=customer.customer_id,
                    account_type=account_type,
                    initial_balance=self._random_balance(),
                )

        return customers

    #Perform the internal random balance step.
    def _random_balance(self) -> str:
        whole = self.random.randint(2_500, 8_500)
        cents = self.random.randint(0, 99)
        return f"{whole}.{cents:02d}"

    #Perform the internal seed activity step.
    def _seed_activity(
        self,
        customers: list[Customer],
    ) -> None:
        for customer in customers:
            if customer.role != UserRole.CUSTOMER:
                continue

            accounts = self.account_service.list_accounts(
                customer.customer_id
            )

            if len(accounts) < 2:
                continue

            tx_types = {
                tx.transaction_type
                for account in accounts
                for tx in self.account_service.history(
                    account.account_id
                )
            }
            source, destination = accounts[0], accounts[1]

            if TransactionType.WITHDRAWAL not in tx_types:
                amount = self.random.randint(40, 150)
                self.account_service.withdraw(
                    source.account_id,
                    f"{amount}.00",
                    f"Seeded withdrawal for {customer.username}",
                )

            if TransactionType.TRANSFER not in tx_types:
                amount = self.random.randint(75, 200)
                self.transfer_service.transfer(
                    source.account_id,
                    destination.account_id,
                    f"{amount}.00",
                    f"Seeded transfer for {customer.username}",
                    actor_username="SEEDER",
                )
