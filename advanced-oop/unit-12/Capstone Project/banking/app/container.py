from __future__ import annotations
from pathlib import Path
from banking.app.seeder import DemoDataSeeder
from banking.config import DEFAULT_DAILY_TRANSFER_LIMIT_CENTS
from banking.patterns.decorators import AuditedTransferService
from banking.repositories.sqlite_repository import SQLiteBankRepository
from banking.security.password_policy import BankSecurePasswordPolicy
from banking.security.pin_hasher import PinHasher
from banking.security.session import SessionManager
from banking.services.account_service import AccountService
from banking.services.audit_service import AuditLogService
from banking.services.authorization import AuthorizationService
from banking.services.bank_staff_service import BankStaffService
from banking.services.banking_operations import BankingOperationsService
from banking.services.customer_service import CustomerService
from banking.services.fraud import LocalSecurityFactory, SecurityServiceFactory
from banking.services.notifications import ConsoleNotificationObserver
from banking.services.profile_service import ProfileService
from banking.services.transfer_policy import DailyTransferLimitPolicy
from banking.services.transfer_service import TransferService
from banking.services.user_admin_service import UserAdministrationService
from banking.validation.account_validator import AccountValidator
from banking.validation.customer_validator import CustomerValidator


#Composition Root that creates and injects the concrete BankSecure dependencies
class ApplicationContainer:
    #Composition Root that creates and injects concrete dependencies

    #Initialise this component with its required dependencies and local state
    def __init__(
        self,
        db_path: str | Path,
        audit_path: str | Path,
        security_factory: SecurityServiceFactory | None = None,
        console_notifications: bool = False,
        seed_demo_data: bool = True,
        daily_transfer_limit_cents: int = DEFAULT_DAILY_TRANSFER_LIMIT_CENTS,
    ) -> None:
        self.repository = SQLiteBankRepository(db_path)
        self.audit_service = AuditLogService(audit_path)
        self.password_policy = BankSecurePasswordPolicy()
        self.customer_validator = CustomerValidator()
        self.account_validator = AccountValidator()

        self.customer_service = CustomerService(
            repository=self.repository,
            pin_hasher=PinHasher(),
            password_policy=self.password_policy,
            validator=self.customer_validator,
            audit_service=self.audit_service,
        )
        self.session_manager = SessionManager(
            self.customer_service
        )
        self.account_service = AccountService(
            self.repository,
            self.account_validator,
        )
        self.authorization_service = AuthorizationService(
            self.repository
        )
        self.security_factory = (
            security_factory
            or LocalSecurityFactory()
        )
        self.transfer_policy = DailyTransferLimitPolicy(
            repository=self.repository,
            daily_limit_cents=daily_transfer_limit_cents,
        )

        observers = []

        if console_notifications:
            observers.append(
                ConsoleNotificationObserver()
            )

        core_transfer = TransferService(
            repository=self.repository,
            transfer_policy=self.transfer_policy,
            fraud_strategy=(
                self.security_factory.create_fraud_strategy()
            ),
            explainer=(
                self.security_factory.create_explainer()
            ),
            observers=observers,
        )
        self.transfer_service = AuditedTransferService(
            wrapped=core_transfer,
            audit_service=self.audit_service,
        )
        self.banking_service = BankingOperationsService(
            account_service=self.account_service,
            authorization_service=self.authorization_service,
            transfer_service=self.transfer_service,
            audit_service=self.audit_service,
        )
        self.bank_staff_service = BankStaffService(
            customer_service=self.customer_service,
            account_service=self.account_service,
            authorization_service=self.authorization_service,
            audit_service=self.audit_service,
        )
        self.user_admin_service = UserAdministrationService(
            customer_service=self.customer_service,
            account_service=self.account_service,
            authorization_service=self.authorization_service,
            audit_service=self.audit_service,
        )
        self.profile_service = ProfileService(
            customer_service=self.customer_service,
            authorization_service=self.authorization_service,
            audit_service=self.audit_service,
        )

        if seed_demo_data:
            DemoDataSeeder(
                customer_service=self.customer_service,
                account_service=self.account_service,
                transfer_service=self.transfer_service,
            ).seed()
