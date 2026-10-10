from __future__ import annotations
from typing import Protocol
from banking.domain.account_identifier import format_account_id
from banking.domain.money import Money
from banking.exceptions import FraudRejectedError
from banking.services.audit_details import TransferAuditDetails
from banking.services.audit_service import AuditLogService
from banking.services.transfer_service import TransferResult


#Define the common transfer interface used by the core service and its Decorator.
class TransferComponent(Protocol):
    #Execute the coordinated transfer workflow through policy, fraud, persistence and notification controls.
    def transfer(
        self,
        from_account_id: int,
        to_account_id: int,
        amount: str | int | Money,
        description: str = "Account transfer",
        actor_username: str = "SYSTEM",
    ) -> TransferResult:
        ...


#Adds audit persistence around a transfer service
class AuditedTransferService:
    #Decorator that adds structured auditing around transfer execution.

    #Initialise this component with its required dependencies and local state.
    def __init__(
        self,
        wrapped: TransferComponent,
        audit_service: AuditLogService,
    ) -> None:
        self.wrapped = wrapped
        self.audit_service = audit_service

    #Execute the coordinated transfer workflow through policy, fraud, persistence and notification controls.
    def transfer(
        self,
        from_account_id: int,
        to_account_id: int,
        amount: str | int | Money,
        description: str = "Account transfer",
        actor_username: str = "SYSTEM",
    ) -> TransferResult:
        display_amount = str(Money.parse(amount))
        base_details = TransferAuditDetails(
            from_account=format_account_id(from_account_id),
            to_account=format_account_id(to_account_id),
            amount=display_amount,
        )

        try:
            result = self.wrapped.transfer(
                from_account_id=from_account_id,
                to_account_id=to_account_id,
                amount=amount,
                description=description,
                actor_username=actor_username,
            )
        except FraudRejectedError as exc:
            self.audit_service.record(
                actor=actor_username,
                action="TRANSFER",
                outcome="REJECTED",
                details=base_details,
                risk_score=exc.risk_score,
                risk_reason=exc.risk_reason,
            )
            raise
        except Exception as exc:
            self.audit_service.record(
                actor=actor_username,
                action="TRANSFER",
                outcome="FAILED",
                details=TransferAuditDetails(
                    from_account=base_details.from_account,
                    to_account=base_details.to_account,
                    amount=base_details.amount,
                    error_type=type(exc).__name__,
                ),
            )
            raise

        self.audit_service.record(
            actor=actor_username,
            action="TRANSFER",
            outcome="COMPLETED",
            details=TransferAuditDetails(
                from_account=base_details.from_account,
                to_account=base_details.to_account,
                amount=base_details.amount,
                transaction_reference=result.transaction_reference,
            ),
            risk_score=result.risk_decision.risk_score,
            risk_reason=result.risk_explanation,
        )

        return result
