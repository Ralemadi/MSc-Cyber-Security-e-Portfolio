from __future__ import annotations
from banking.domain.models import Account, AccountStatus, Transaction
from banking.domain.money import Money
from banking.exceptions import AccountNotFoundError
from banking.repositories.interfaces import BankRepository
from banking.security.roles import UserRole
from banking.validation.account_validator import AccountValidator


#Convert Money to integer cents for compatibility with persistence calculations.
def money_to_cents(value: str | int | Money) -> int:
    #Compatibility helper. New code should prefer Money directly.
    return Money.parse(value).require_positive().cents


#Convert stored integer cents back into the Money Value Object.
def cents_to_money(cents: int) -> str:
    #Compatibility helper.
    return str(Money.from_cents(cents))


class AccountService:
    #Account use cases and account-specific validation

    #Initialise this component with its required dependencies and local state
    def __init__(
        self,
        repository: BankRepository,
        validator: AccountValidator,
    ) -> None:
        self.repository = repository
        self.validator = validator

    #Validate account type input before the operation continues
    def validate_account_type(self, account_type: str) -> str:
        return self.validator.account_type(account_type)

    #Validate the opening balance and return it as Money.
    def opening_balance_to_money(
        self,
        initial_balance: str | int | Money,
    ) -> Money:
        return self.validator.opening_balance(initial_balance)

    def opening_balance_to_cents(
        self,
        initial_balance: str | int | Money,
    ) -> int:
        return self.opening_balance_to_money(initial_balance).cents

    #Validate and create the requested account through this responsibility boundary
    def create_account(
        self,
        customer_id: int,
        account_type: str,
        initial_balance: str | int | Money = "0.00",
    ) -> Account:
        owner = self.repository.get_customer(customer_id)

        if owner is None:
            raise ValueError(
                "The requested CUSTOMER user does not exist."
            )

        if owner.role != UserRole.CUSTOMER:
            raise ValueError(
                "Bank accounts can be created only for CUSTOMER users."
            )

        return self.repository.create_account(
            customer_id=customer_id,
            account_type=self.validator.account_type(account_type),
            initial_balance=self.validator.opening_balance(initial_balance),
        )

    #Retrieve the requested account without exposing persistence details to callers
    def get_account(self, account_id: int) -> Account:
        account = self.repository.get_account(account_id)

        if account is None:
            raise AccountNotFoundError(
                "The requested account does not exist."
            )

        return account

    #Return only the accounts visible within the actor's authorised resource scope
    def list_accounts(self, customer_id: int) -> list[Account]:
        return self.repository.list_accounts_for_customer(customer_id)

    #Return the authorised collection of all accounts records.
    def list_all_accounts(self) -> list[Account]:
        return self.repository.list_all_accounts()

    #Apply an ADMINISTRATOR controlled account status change and audit the action
    def set_account_status(
        self,
        account_id: int,
        status: AccountStatus,
    ) -> Account:
        return self.repository.update_account_status(account_id, status)

    #Validate authorization and account state before applying the deposit
    def deposit(
        self,
        account_id: int,
        amount: str | int | Money,
        description: str = "Cash deposit",
    ) -> Account:
        money = Money.parse(amount).require_positive("Deposit amount")
        return self.repository.deposit(
            account_id=account_id,
            amount=money,
            description=description,
        )

    #Validate authorization, account state and funds before applying the withdrawal
    def withdraw(
        self,
        account_id: int,
        amount: str | int | Money,
        description: str = "Cash withdrawal",
    ) -> Account:
        money = Money.parse(amount).require_positive("Withdrawal amount")
        return self.repository.withdraw(
            account_id=account_id,
            amount=money,
            description=description,
        )

    #Return transaction history for an account after resource access checks
    def history(self, account_id: int) -> list[Transaction]:
        self.get_account(account_id)
        return self.repository.list_transactions_for_account(account_id)
