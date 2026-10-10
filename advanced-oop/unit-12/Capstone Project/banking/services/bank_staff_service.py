from __future__ import annotations
from dataclasses import dataclass
from banking.domain.account_identifier import format_account_id
from banking.domain.models import Account, Customer
from banking.domain.money import Money
from banking.security.privileges import Privilege
from banking.security.roles import UserRole
from banking.services.account_service import AccountService
from banking.services.audit_details import CustomerAuditDetails
from banking.services.audit_service import AuditLogService
from banking.services.authorization import AuthorizationService
from banking.services.customer_service import CustomerService
from banking.services.results import AccountCreationResult



@dataclass(frozen=True)
class CustomerOverview:
    customer: Customer
    accounts: tuple[Account, ...]


#Restrict customer-account administration to authorised BANK_STAFF identities.
class BankStaffService:


    #Initialise this component with its required dependencies and local state.
    def __init__(
        self,
        customer_service: CustomerService,
        account_service: AccountService,
        authorization_service: AuthorizationService,
        audit_service: AuditLogService,
    ) -> None:
        self.customer_service = customer_service
        self.account_service = account_service
        self.authorization_service = authorization_service
        self.audit_service = audit_service

    #Create a CUSTOMER identity and first account through the BANK_STAFF workflow.
    def create_customer_with_account(
        self,
        *,
        actor: Customer,
        username: str,
        full_name: str,
        email: str,
        password: str,
        account_type: str,
        opening_balance: str | int | Money,
    ) -> AccountCreationResult:
        self.authorization_service.require_privilege(
            actor,
            Privilege.CREATE_CUSTOMER,
        )
        normalised_type = self.account_service.validate_account_type(
            account_type
        )
        opening_money = self.account_service.opening_balance_to_money(
            opening_balance
        )
        customer = self.customer_service.register_customer(
            username=username,
            full_name=full_name,
            email=email,
            password=password,
            role=UserRole.CUSTOMER,
        )
        account = self.account_service.create_account(
            customer_id=customer.customer_id,
            account_type=normalised_type,
            initial_balance=opening_money,
        )
        self.audit_service.record(
            actor=actor.username,
            action="CREATE_CUSTOMER",
            outcome="COMPLETED",
            details=CustomerAuditDetails(
                customer=customer.username,
                account=format_account_id(account.account_id),
                account_type=account.account_type,
            ),
        )
        return AccountCreationResult(
            customer=customer,
            account=account,
        )

    #Add the requested account after validation and authorization checks
    def add_account(
        self,
        *,
        actor: Customer,
        customer: Customer,
        account_type: str,
        opening_balance: str | int | Money,
    ) -> AccountCreationResult:
        self.authorization_service.require_privilege(
            actor,
            Privilege.ADD_CUSTOMER_ACCOUNT,
        )

        if customer.role != UserRole.CUSTOMER:
            raise ValueError(
                "Bank accounts can be added only to CUSTOMER users."
            )

        account = self.account_service.create_account(
            customer_id=customer.customer_id,
            account_type=account_type,
            initial_balance=opening_balance,
        )
        self.audit_service.record(
            actor=actor.username,
            action="CREATE_ACCOUNT",
            outcome="COMPLETED",
            details=CustomerAuditDetails(
                customer=customer.username,
                account=format_account_id(account.account_id),
                account_type=account.account_type,
            ),
        )
        return AccountCreationResult(
            customer=customer,
            account=account,
        )

    #Build BANK_STAFF customer summaries with each CUSTOMER account collection
    def customer_overviews(
        self,
        actor: Customer,
        privilege: Privilege,
    ) -> list[CustomerOverview]:
        self.authorization_service.require_privilege(
            actor,
            privilege,
        )
        overviews: list[CustomerOverview] = []

        for customer in self.customer_service.list_customers():
            if customer.role != UserRole.CUSTOMER:
                continue

            overviews.append(
                CustomerOverview(
                    customer=customer,
                    accounts=tuple(
                        self.account_service.list_accounts(
                            customer.customer_id
                        )
                    ),
                )
            )

        return overviews
