from __future__ import annotations
from banking.domain.account_identifier import format_account_id
from banking.domain.models import Account, Customer, Transaction
from banking.domain.money import Money
from banking.patterns.decorators import TransferComponent
from banking.security.privileges import Privilege
from banking.services.account_service import AccountService
from banking.services.audit_details import BalanceChangeAuditDetails
from banking.services.audit_service import AuditLogService
from banking.services.authorization import AuthorizationService
from banking.services.results import DepositResult, WithdrawalResult
from banking.services.transfer_service import TransferResult


class BankingOperationsService:
    #Privilege-aware facade for CUSTOMER and BANK_STAFF banking operations.

    #Initialise this component with its required dependencies and local state.
    def __init__(
        self,
        account_service: AccountService,
        authorization_service: AuthorizationService,
        transfer_service: TransferComponent,
        audit_service: AuditLogService,
    ) -> None:
        self.account_service = account_service
        self.authorization_service = authorization_service
        self.transfer_service = transfer_service
        self.audit_service = audit_service

    #Return accounts permitted by the current accounts access policy.
    def accessible_accounts(
        self,
        actor: Customer,
        privilege: Privilege,
    ) -> list[Account]:
        return self.authorization_service.accessible_accounts(
            actor,
            privilege,
        )

    #Retrieve the requested accessible account without exposing persistence details to callers.
    def get_accessible_account(
        self,
        actor: Customer,
        account_id: int,
        privilege: Privilege,
    ) -> Account:
        return self.authorization_service.require_account_access(
            actor,
            account_id,
            privilege,
        )

    #Validate authorization and account state before applying the deposit
    def deposit(
        self,
        actor: Customer,
        account_id: int,
        amount: str | int | Money,
    ) -> DepositResult:
        self.authorization_service.require_account_access(
            actor,
            account_id,
            Privilege.DEPOSIT_FUNDS,
        )
        money = Money.parse(amount).require_positive("Deposit amount")

        try:
            updated = self.account_service.deposit(
                account_id,
                money,
            )
        except Exception as exc:
            self.audit_service.record(
                actor=actor.username,
                action="DEPOSIT",
                outcome="FAILED",
                details=BalanceChangeAuditDetails(
                    account=format_account_id(account_id),
                    amount=str(money),
                    error_type=type(exc).__name__,
                ),
            )
            raise

        self.audit_service.record(
            actor=actor.username,
            action="DEPOSIT",
            outcome="COMPLETED",
            details=BalanceChangeAuditDetails(
                account=format_account_id(account_id),
                amount=str(money),
            ),
        )
        return DepositResult(
            account=updated,
            amount=money,
        )

    #Validate authorization, account state and funds before applying the withdrawal
    def withdraw(
        self,
        actor: Customer,
        account_id: int,
        amount: str | int | Money,
    ) -> WithdrawalResult:
        self.authorization_service.require_account_access(
            actor,
            account_id,
            Privilege.WITHDRAW_FUNDS,
        )
        money = Money.parse(amount).require_positive("Withdrawal amount")

        try:
            updated = self.account_service.withdraw(
                account_id,
                money,
            )
        except Exception as exc:
            self.audit_service.record(
                actor=actor.username,
                action="WITHDRAWAL",
                outcome="FAILED",
                details=BalanceChangeAuditDetails(
                    account=format_account_id(account_id),
                    amount=str(money),
                    error_type=type(exc).__name__,
                ),
            )
            raise

        self.audit_service.record(
            actor=actor.username,
            action="WITHDRAWAL",
            outcome="COMPLETED",
            details=BalanceChangeAuditDetails(
                account=format_account_id(account_id),
                amount=str(money),
            ),
        )
        return WithdrawalResult(
            account=updated,
            amount=money,
        )

    #Execute the coordinated transfer workflow through policy, fraud, persistence and notification controls
    def transfer(
        self,
        actor: Customer,
        from_account_id: int,
        to_account_id: int,
        amount: str | int | Money,
    ) -> TransferResult:
        self.authorization_service.require_account_access(
            actor,
            from_account_id,
            Privilege.TRANSFER_FUNDS,
        )
        destination = self.account_service.get_account(
            to_account_id
        )
        destination_owner = self.authorization_service.repository.get_customer(
            destination.customer_id
        )

        if (
            destination_owner is None
            or not destination_owner.is_customer
        ):
            raise ValueError(
                "Transfers can be sent only to CUSTOMER bank accounts."
            )

        return self.transfer_service.transfer(
            from_account_id=from_account_id,
            to_account_id=to_account_id,
            amount=amount,
            actor_username=actor.username,
        )

    #Return transaction history for an account after resource-access checks.
    def history(
        self,
        actor: Customer,
        account_id: int,
    ) -> list[Transaction]:
        self.authorization_service.require_account_access(
            actor,
            account_id,
            Privilege.VIEW_TRANSACTION_HISTORY,
        )
        return self.account_service.history(account_id)
