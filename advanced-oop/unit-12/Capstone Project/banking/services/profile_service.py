from __future__ import annotations
from banking.domain.models import Customer
from banking.security.privileges import Privilege
from banking.services.audit_details import PasswordAuditDetails
from banking.services.audit_service import AuditLogService
from banking.services.authorization import AuthorizationService
from banking.services.customer_service import CustomerService


class ProfileService:
    #Self-service profile operations shared by all enabled roles

    #Initialise this component with its required dependencies and local state
    def __init__(
        self,
        customer_service: CustomerService,
        authorization_service: AuthorizationService,
        audit_service: AuditLogService,
    ) -> None:
        self.customer_service = customer_service
        self.authorization_service = authorization_service
        self.audit_service = audit_service

    #Apply the requested own password change through the owning service.
    def change_own_password(
        self,
        *,
        actor: Customer,
        current_password: str,
        new_password: str,
    ) -> None:
        self.authorization_service.require_privilege(
            actor,
            Privilege.CHANGE_OWN_PASSWORD,
        )
        self.customer_service.change_password(
            actor,
            current_password,
            new_password,
        )
        self.audit_service.record(
            actor=actor.username,
            action="CHANGE_OWN_PASSWORD",
            outcome="COMPLETED",
            details=PasswordAuditDetails(
                username=actor.username,
                mode="SELF_SERVICE",
            ),
        )
