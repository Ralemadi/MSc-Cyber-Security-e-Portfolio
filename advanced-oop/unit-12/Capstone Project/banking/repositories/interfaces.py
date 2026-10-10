from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any
from banking.domain.models import (
    Account,
    AccountStatus,
    Customer,
    Transaction,
)
from banking.domain.money import Money
from banking.security.roles import UserRole


class BankRepository(ABC):
    #Persistence contract used by the service layer.

    #Validate and create the requested customer through this responsibility boundary.
    @abstractmethod
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
        ...

    #Retrieve the requested customer without exposing persistence details to callers.
    @abstractmethod
    def get_customer(self, customer_id: int) -> Customer | None:
        ...

    #Retrieve the requested customer by username without exposing persistence details to callers.
    @abstractmethod
    def get_customer_by_username(self, username: str) -> Any | None:
        ...

    #Retrieve the requested customer by email without exposing persistence details to callers.
    @abstractmethod
    def get_customer_by_email(self, email: str) -> Any | None:
        ...

    #Return the authorised collection of customers records.
    @abstractmethod
    def list_customers(self) -> list[Customer]:
        ...

    #Persist the requested customer enabled change and return controlled results.
    @abstractmethod
    def update_customer_enabled(
        self,
        customer_id: int,
        enabled: bool,
    ) -> Customer:
        ...

    #Persist the requested customer role change and return controlled results.
    @abstractmethod
    def update_customer_role(
        self,
        customer_id: int,
        role: UserRole,
    ) -> Customer:
        ...

    #Persist the requested customer password change and return controlled results.
    @abstractmethod
    def update_customer_password(
        self,
        customer_id: int,
        pin_salt_hex: str,
        pin_hash_hex: str,
    ) -> None:
        ...

    #Atomically increment and return the persisted failed-login counter for the identity.
    @abstractmethod
    def increment_failed_login_attempts(
        self,
        customer_id: int,
    ) -> int:
        ...

    #Apply the requested customer lockout state change through the owning component.
    @abstractmethod
    def set_customer_lockout(
        self,
        customer_id: int,
        locked_until: datetime,
    ) -> Customer:
        ...

    #Clear the current customer login security state in a controlled way.
    @abstractmethod
    def clear_customer_login_security(
        self,
        customer_id: int,
    ) -> Customer:
        ...

    #Validate and create the requested account through this responsibility boundary.
    @abstractmethod
    def create_account(
        self,
        customer_id: int,
        account_type: str,
        initial_balance: Money,
    ) -> Account:
        ...

    #Retrieve the requested account without exposing persistence details to callers.
    @abstractmethod
    def get_account(self, account_id: int) -> Account | None:
        ...

    #Return the authorised collection of accounts for customer records.
    @abstractmethod
    def list_accounts_for_customer(
        self,
        customer_id: int,
    ) -> list[Account]:
        ...

    #Return the authorised collection of all accounts records.
    @abstractmethod
    def list_all_accounts(self) -> list[Account]:
        ...

    #Persist the requested account status change and return controlled results.
    @abstractmethod
    def update_account_status(
        self,
        account_id: int,
        status: AccountStatus,
    ) -> Account:
        ...

    #Validate authorization and account state before applying the deposit.
    @abstractmethod
    def deposit(
        self,
        account_id: int,
        amount: Money,
        description: str,
    ) -> Account:
        ...

    #Validate authorization, account state and funds before applying the withdrawal.
    @abstractmethod
    def withdraw(
        self,
        account_id: int,
        amount: Money,
        description: str,
    ) -> Account:
        ...

    #Execute the coordinated transfer workflow through policy, fraud, persistence and notification controls.
    @abstractmethod
    def transfer(
        self,
        from_account_id: int,
        to_account_id: int,
        amount: Money,
        description: str,
    ) -> Transaction:
        ...

    #Return the authorised collection of transactions for account records.
    @abstractmethod
    def list_transactions_for_account(
        self,
        account_id: int,
    ) -> list[Transaction]:
        ...

    #Calculate the stored outgoing transfers since value needed by the policy check.
    @abstractmethod
    def sum_outgoing_transfers_since(
        self,
        account_id: int,
        since: datetime,
    ) -> Money:
        ...
