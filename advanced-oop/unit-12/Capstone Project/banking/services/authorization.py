from __future__ import annotations
from abc import ABC, abstractmethod
from banking.domain.models import Account, Customer
from banking.exceptions import AccountNotFoundError, AuthorizationError
from banking.repositories.interfaces import BankRepository
from banking.security.privileges import Privilege, privileges_for
from banking.security.roles import UserRole



class AccountAccessPolicy(ABC):
 

    #Initialise this component with its required dependencies and local state
    def __init__(
        self,
        repository: BankRepository,
        customer: Customer,
    ) -> None:
        self.repository = repository
        self.customer = customer

    #Return accounts permitted by the current accounts access policy
    @abstractmethod
    def accessible_accounts(
        self,
    ) -> list[Account]:
        ...

    #Report whether the requested access action is permitted
    @abstractmethod
    def can_access(
        self,
        account: Account,
    ) -> bool:
        ...



class CustomerAccountAccessPolicy(
    AccountAccessPolicy
):
    #CUSTOMER can access only accounts owned by the same identity


    def accessible_accounts(
        self,
    ) -> list[Account]:
        return self.repository.list_accounts_for_customer(
            self.customer.customer_id
        )

    #Report whether the requested access action is permitted.
    def can_access(
        self,
        account: Account,
    ) -> bool:
        return (
            account.customer_id
            == self.customer.customer_id
        )


#Encapsulate the bank wide customer account access rule independently from orchestration code
class BankWideCustomerAccountAccessPolicy(
    AccountAccessPolicy
):
    #BANK_STAFF/ADMINISTRATOR scope covers bank accounts owned by CUSTOMER users


    def accessible_accounts(
        self,
    ) -> list[Account]:
        return [
            account
            for account in self.repository.list_all_accounts()
            if self._is_customer_account(account)
        ]

    #Report whether the requested access action is permitted.
    def can_access(
        self,
        account: Account,
    ) -> bool:
        return self._is_customer_account(account)

    #Perform the internal is customer account step used by this workflow
    def _is_customer_account(
        self,
        account: Account,
    ) -> bool:
        owner = self.repository.get_customer(
            account.customer_id
        )
        return (
            owner is not None
            and owner.role == UserRole.CUSTOMER
        )



class AuthorizationService:
    #Role-Based Access Control.

    #Initialise this component with its required dependencies and local state
    def __init__(
        self,
        repository: BankRepository,
    ) -> None:
        self.repository = repository

    #Check whether the actor's role contains the requested privilege
    def has_privilege(
        self,
        customer: Customer,
        privilege: Privilege,
    ) -> bool:
        return (
            customer.enabled
            and privilege in privileges_for(customer.role)
        )

    #Reject the operation unless the actor owns the requested privilege
    def require_privilege(
        self,
        customer: Customer,
        privilege: Privilege,
    ) -> None:
        if not self.has_privilege(
            customer,
            privilege,
        ):
            raise AuthorizationError(
                f"Missing privilege: {privilege.value}."
            )

    #Select the resource-access policy that corresponds to the actor and requested privilege
    def policy_for(
        self,
        customer: Customer,
    ) -> AccountAccessPolicy:
        if customer.role == UserRole.CUSTOMER:
            return CustomerAccountAccessPolicy(
                self.repository,
                customer,
            )

        return BankWideCustomerAccountAccessPolicy(
            self.repository,
            customer,
        )

    #Return accounts permitted by the current accounts access policy
    def accessible_accounts(
        self,
        customer: Customer,
        privilege: Privilege,
    ) -> list[Account]:
        self.require_privilege(
            customer,
            privilege,
        )
        return self.policy_for(
            customer
        ).accessible_accounts()

    #Enforce both action privilege and resource-level account access before banking work proceeds
    def require_account_access(
        self,
        customer: Customer,
        account_id: int,
        privilege: Privilege,
    ) -> Account:
        self.require_privilege(
            customer,
            privilege,
        )
        account = self.repository.get_account(
            account_id
        )

        if account is None:
            raise AccountNotFoundError(
                "The selected account does not exist."
            )

        if not self.policy_for(
            customer
        ).can_access(account):
            raise AuthorizationError(
                "You are not authorised to access this account."
            )

        return account
