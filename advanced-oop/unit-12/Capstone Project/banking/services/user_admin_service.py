from __future__ import annotations
from banking.domain.account_identifier import format_account_id
from banking.domain.models import Account, AccountStatus, Customer
from banking.security.privileges import Privilege
from banking.security.roles import UserRole
from banking.services.account_service import AccountService
from banking.services.audit_details import (
    AccountStatusAuditDetails,
    LoginSecurityAuditDetails,
    PasswordAuditDetails,
    RoleChangeAuditDetails,
    UserAuditDetails,
    UserStatusAuditDetails,
)
from banking.services.audit_service import AuditLogService, AuditRecord
from banking.services.authorization import AuthorizationService
from banking.services.customer_service import CustomerService


class UserAdministrationService:

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

    #Create a system identity through the ADMINISTRATOR workflow.
    def create_user(
        self,
        *,
        actor: Customer,
        username: str,
        full_name: str,
        email: str,
        password: str,
        role: UserRole,
    ) -> Customer:
        self.authorization_service.require_privilege(
            actor,
            Privilege.CREATE_USER,
        )
        created = self.customer_service.register_customer(
            username=username,
            full_name=full_name,
            email=email,
            password=password,
            role=role,
            enabled=True,
        )
        self.audit_service.record(
            actor=actor.username,
            action="CREATE_USER",
            outcome="COMPLETED",
            details=UserAuditDetails(
                username=created.username,
                role=created.role.value,
                enabled=created.enabled,
            ),
        )
        return created

    #Return the authorised collection of users records.
    def list_users(
        self,
        actor: Customer,
    ) -> list[Customer]:
        self.authorization_service.require_privilege(
            actor,
            Privilege.VIEW_USERS,
        )
        return self.customer_service.list_customers()

    #Change administrative enablement while preserving temporary-lockout state as a separate control
    def set_user_enabled(
        self,
        *,
        actor: Customer,
        target: Customer,
        enabled: bool,
    ) -> Customer:
        privilege = (
            Privilege.ENABLE_USER
            if enabled
            else Privilege.DISABLE_USER
        )
        self.authorization_service.require_privilege(
            actor,
            privilege,
        )

        if actor.customer_id == target.customer_id and not enabled:
            raise ValueError(
                "You cannot disable your own active administrator account."
            )

        updated = self.customer_service.set_enabled(
            target,
            enabled,
        )
        self.audit_service.record(
            actor=actor.username,
            action="ENABLE_USER" if enabled else "DISABLE_USER",
            outcome="COMPLETED",
            details=UserStatusAuditDetails(
                username=updated.username,
                enabled=updated.enabled,
            ),
        )
        return updated

    #Clear an active temporary login lockout through the ADMINISTRATOR-only workflow
    def unlock_user(
        self,
        *,
        actor: Customer,
        target: Customer,
    ) -> Customer:
        self.authorization_service.require_privilege(
            actor,
            Privilege.UNLOCK_USER,
        )

        if not target.is_temporarily_locked:
            raise ValueError(
                "This user is not currently under a temporary login lockout."
            )

        updated = self.customer_service.unlock_temporary_lock(
            target
        )
        self.audit_service.record(
            actor=actor.username,
            action="UNLOCK_USER",
            outcome="COMPLETED",
            details=LoginSecurityAuditDetails(
                username=updated.username,
                failed_attempts=0,
            ),
        )
        return updated

    #Apply role-change restrictions before persisting the new system role
    def change_user_role(
        self,
        *,
        actor: Customer,
        target: Customer,
        role: UserRole,
    ) -> Customer:
        self.authorization_service.require_privilege(
            actor,
            Privilege.ASSIGN_USER_ROLE,
        )

        if actor.customer_id == target.customer_id:
            raise ValueError(
                "Use another administrator account to change your own role."
            )

        if (
            target.role == UserRole.CUSTOMER
            and role != UserRole.CUSTOMER
            and self.account_service.list_accounts(target.customer_id)
        ):
            raise ValueError(
                "A CUSTOMER with bank accounts cannot be changed to "
                "BANK_STAFF or ADMINISTRATOR."
            )

        old_role = target.role
        updated = self.customer_service.change_role(
            target,
            role,
        )
        self.audit_service.record(
            actor=actor.username,
            action="CHANGE_USER_ROLE",
            outcome="COMPLETED",
            details=RoleChangeAuditDetails(
                username=updated.username,
                old_role=old_role.value,
                new_role=updated.role.value,
            ),
        )
        return updated

    #Reset another users password through the ADMINISTRATOR-only workflow
    def reset_user_password(
        self,
        *,
        actor: Customer,
        target: Customer,
        new_password: str,
    ) -> None:
        self.authorization_service.require_privilege(
            actor,
            Privilege.RESET_USER_PASSWORD,
        )
        self.customer_service.reset_password(
            target,
            new_password,
        )
        self.audit_service.record(
            actor=actor.username,
            action="RESET_USER_PASSWORD",
            outcome="COMPLETED",
            details=PasswordAuditDetails(
                username=target.username,
                mode="ADMIN_RESET",
            ),
        )

    #Return privileged audit records only after ADMINISTRATOR authorization
    def audit_records(
        self,
        actor: Customer,
        limit: int = 50,
    ) -> list[AuditRecord]:
        self.authorization_service.require_privilege(
            actor,
            Privilege.VIEW_AUDIT,
        )
        return self.audit_service.list_records(
            limit=limit
        )

    #Return accounts permitted by the current accounts for status access policy
    def accessible_accounts_for_status(
        self,
        actor: Customer,
    ) -> list[Account]:
        return self.authorization_service.accessible_accounts(
            actor,
            Privilege.MANAGE_ACCOUNT_STATUS,
        )

    #Apply an ADMINISTRATOR-controlled account status change and audit the action
    def set_account_status(
        self,
        *,
        actor: Customer,
        account_id: int,
        status: AccountStatus,
    ) -> Account:
        self.authorization_service.require_account_access(
            actor,
            account_id,
            Privilege.MANAGE_ACCOUNT_STATUS,
        )
        updated = self.account_service.set_account_status(
            account_id,
            status,
        )
        self.audit_service.record(
            actor=actor.username,
            action="ACCOUNT_STATUS_CHANGE",
            outcome="COMPLETED",
            details=AccountStatusAuditDetails(
                account=format_account_id(account_id),
                new_status=status.value,
            ),
        )
        return updated
