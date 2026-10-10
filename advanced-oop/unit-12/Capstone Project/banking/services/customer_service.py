from __future__ import annotations
from datetime import datetime, timedelta, timezone
from banking.config import (
    MAX_FAILED_LOGIN_ATTEMPTS,
    TEMPORARY_LOCKOUT_MINUTES,
)
from banking.domain.models import Customer
from banking.exceptions import (
    AuthenticationError,
    UserDisabledError,
    UserTemporarilyLockedError,
)
from banking.repositories.interfaces import BankRepository
from banking.security.password_policy import BankSecurePasswordPolicy
from banking.security.pin_hasher import PinHasher
from banking.security.roles import UserRole
from banking.services.audit_details import LoginSecurityAuditDetails
from banking.services.audit_service import AuditLogService
from banking.validation.customer_validator import CustomerValidator


class CustomerService:
    #Identity registration, authentication and password management.

    def __init__(
        self,
        repository: BankRepository,
        pin_hasher: PinHasher,
        password_policy: BankSecurePasswordPolicy,
        validator: CustomerValidator,
        audit_service: AuditLogService | None = None,
    ) -> None:
        self.repository = repository
        self.pin_hasher = pin_hasher
        self.password_policy = password_policy
        self.validator = validator
        self.audit_service = audit_service

    #Validate username input before the operation continues.
    def validate_username(self, username: str) -> str:
        return self.validator.username(username)

    #Validate email input before the operation continues.
    def validate_email(self, email: str) -> str:
        return self.validator.email(email)

    #Validate the new identity, apply password policy and persist the customer securely.
    def register_customer(
        self,
        username: str,
        full_name: str,
        email: str,
        password: str,
        role: UserRole = UserRole.CUSTOMER,
        enabled: bool = True,
    ) -> Customer:
        username = self.validator.username(username)
        full_name = self.validator.full_name(full_name)
        email = self.validator.email(email)
        self._validate_new_password(
            username=username,
            password=password,
        )
        salt_hex, hash_hex = self.pin_hasher.hash_pin(password)

        return self.repository.create_customer(
            username=username,
            full_name=full_name,
            email=email,
            pin_salt_hex=salt_hex,
            pin_hash_hex=hash_hex,
            role=role,
            enabled=enabled,
        )

    #Authenticate credentials while enforcing temporary lockout and administrative account status.
    def authenticate(
        self,
        username: str,
        password: str,
    ) -> Customer | None:
        username = username.strip()
        row = self.repository.get_customer_by_username(
            username
        )

        if row is None:
            return None

        customer_id = int(row["customer_id"])
        now = datetime.now(timezone.utc)
        locked_until = self._locked_until_from_row(row)

        #Reject an active lockout, or clear an expired lock before validating the password.
        if locked_until is not None:
            if locked_until > now:
                raise UserTemporarilyLockedError(
                    locked_until
                )

            self.repository.clear_customer_login_security(
                customer_id
            )
            self._record_login_security_event(
                username=username,
                action="TEMPORARY_LOCKOUT_EXPIRED",
                outcome="COMPLETED",
            )
            row = self.repository.get_customer_by_username(
                username
            )

            if row is None:
                return None

        #A failed password increments the persisted counter before the lockout threshold is evaluated.
        if not self.pin_hasher.verify_pin(
            password,
            row["pin_salt_hex"],
            row["pin_hash_hex"],
        ):
            failed_attempts = (
                self.repository
                .increment_failed_login_attempts(
                    customer_id
                )
            )

            self._record_login_security_event(
                username=username,
                action="LOGIN_FAILED",
                outcome="REJECTED",
                failed_attempts=failed_attempts,
            )

            #The threshold creates a separate five-minute lock without changing administrative enablement.
            if failed_attempts >= MAX_FAILED_LOGIN_ATTEMPTS:
                locked_until = (
                    now
                    + timedelta(
                        minutes=TEMPORARY_LOCKOUT_MINUTES
                    )
                )
                self.repository.set_customer_lockout(
                    customer_id,
                    locked_until,
                )
                self._record_login_security_event(
                    username=username,
                    action="TEMPORARY_LOCKOUT",
                    outcome="LOCKED",
                    failed_attempts=failed_attempts,
                    locked_until=locked_until,
                )
                raise UserTemporarilyLockedError(
                    locked_until
                )

            return None

        if (
            int(row["failed_login_attempts"]) > 0
            or row["locked_until"] is not None
        ):
            self.repository.clear_customer_login_security(
                customer_id
            )
            row = self.repository.get_customer_by_username(
                username
            )

            if row is None:
                return None

        #Administrative disablement remains independent from the temporary authentication lockout.
        if not bool(row["enabled"]):
            self._record_login_security_event(
                username=username,
                action="LOGIN_DISABLED_USER",
                outcome="REJECTED",
            )
            raise UserDisabledError(
                "This user account is disabled."
            )

        customer = self._customer_from_row(row)

        self._record_login_security_event(
            username=username,
            action="LOGIN_SUCCESS",
            outcome="COMPLETED",
        )

        return customer

    #Verify the current password before replacing it with a policy-compliant new password.
    def change_password(
        self,
        customer: Customer,
        current_password: str,
        new_password: str,
    ) -> None:
        row = self.repository.get_customer_by_username(
            customer.username
        )

        if row is None:
            raise AuthenticationError(
                "User account could not be found."
            )

        if not self.pin_hasher.verify_pin(
            current_password,
            row["pin_salt_hex"],
            row["pin_hash_hex"],
        ):
            raise AuthenticationError(
                "Current password is incorrect."
            )

        if self.pin_hasher.verify_pin(
            new_password,
            row["pin_salt_hex"],
            row["pin_hash_hex"],
        ):
            raise ValueError(
                "New password must be different from the current password."
            )

        self.reset_password(
            customer,
            new_password,
        )

    #Apply password policy and persist a newly salted password hash.
    def reset_password(
        self,
        customer: Customer,
        new_password: str,
    ) -> None:
        self._validate_new_password(
            username=customer.username,
            password=new_password,
        )
        salt_hex, hash_hex = self.pin_hasher.hash_pin(
            new_password
        )
        self.repository.update_customer_password(
            customer.customer_id,
            salt_hex,
            hash_hex,
        )

    #Apply the requested enabled state change through the owning component.
    def set_enabled(
        self,
        customer: Customer,
        enabled: bool,
    ) -> Customer:
        return self.repository.update_customer_enabled(
            customer.customer_id,
            enabled,
        )

    def unlock_temporary_lock(
        self,
        customer: Customer,
    ) -> Customer:
        return self.repository.clear_customer_login_security(
            customer.customer_id
        )

    #Apply the requested role change through the owning service.
    def change_role(
        self,
        customer: Customer,
        role: UserRole,
    ) -> Customer:
        return self.repository.update_customer_role(
            customer.customer_id,
            role,
        )

    def get_customer(
        self,
        customer_id: int,
    ) -> Customer | None:
        return self.repository.get_customer(customer_id)

    def get_customer_by_username(
        self,
        username: str,
    ) -> Customer | None:
        row = self.repository.get_customer_by_username(
            username.strip()
        )

        if row is None:
            return None

        return self._customer_from_row(row)

    #Check whether username already exists before duplicate data is created.
    def username_exists(
        self,
        username: str,
    ) -> bool:
        return (
            self.repository.get_customer_by_username(
                username.strip()
            )
            is not None
        )

    #Check whether email already exists before duplicate data is created.
    def email_exists(
        self,
        email: str,
    ) -> bool:
        return (
            self.repository.get_customer_by_email(
                email.strip().lower()
            )
            is not None
        )

    #Return the authorised collection of customers records.
    def list_customers(self) -> list[Customer]:
        return self.repository.list_customers()

    #Apply internal validation for new password before persistence.
    def _validate_new_password(
        self,
        *,
        username: str,
        password: str,
    ) -> None:
        validation = self.password_policy.validate(
            password,
            username=username,
        )

        if not validation.valid:
            raise ValueError(
                " ".join(validation.errors)
            )

    #Record authentication-security evidence without storing the supplied password.
    def _record_login_security_event(
        self,
        *,
        username: str,
        action: str,
        outcome: str,
        failed_attempts: int | None = None,
        locked_until: datetime | None = None,
    ) -> None:
        if self.audit_service is None:
            return

        self.audit_service.record(
            actor=username,
            action=action,
            outcome=outcome,
            details=LoginSecurityAuditDetails(
                username=username,
                failed_attempts=failed_attempts,
                locked_until=(
                    locked_until.isoformat()
                    if locked_until is not None
                    else None
                ),
            ),
        )

    #Perform the internal locked until from row step used by this workflow.
    @staticmethod
    def _locked_until_from_row(
        row,
    ) -> datetime | None:
        raw = row["locked_until"]

        if not raw:
            return None

        return datetime.fromisoformat(raw)

    #Perform the internal customer from row step used by this workflow.
    @staticmethod
    def _customer_from_row(row) -> Customer:
        locked_until = CustomerService._locked_until_from_row(
            row
        )

        return Customer(
            customer_id=row["customer_id"],
            username=row["username"],
            full_name=row["full_name"],
            email=row["email"],
            role=UserRole(row["role"]),
            enabled=bool(row["enabled"]),
            failed_login_attempts=int(
                row["failed_login_attempts"]
            ),
            locked_until=locked_until,
        )
