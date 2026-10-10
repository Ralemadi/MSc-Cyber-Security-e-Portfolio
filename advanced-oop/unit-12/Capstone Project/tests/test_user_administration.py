from __future__ import annotations
from datetime import datetime, timedelta, timezone
from unittest.mock import Mock
from banking.domain.models import AccountStatus
from banking.security.roles import UserRole
from banking.ui.handlers.administrator import AdministratorCommandHandler
from banking.services.results import AccountCreationResult
from base_test_case import BankSecureTestCase


#automated checks for user administration
class UserAdministrationTests(BankSecureTestCase):
    #Verify that BANK_STAFF can create a new CUSTOMER with an initial bank account
    def test_bank_staff_can_create_customer_and_first_account(self) -> None:
            result = (
                self.app.bank_staff_service
                .create_customer_with_account(
                    actor=self.staff,
                    username="createdcustomer",
                    full_name="Created Customer",
                    email="created@example.com",
                    password="CreatedPASS!@#",
                    account_type="CURRENT",
                    opening_balance="900.00",
                )
            )
            self.assertIsInstance(
                result,
                AccountCreationResult,
            )
            self.assertEqual(
                result.customer.role,
                UserRole.CUSTOMER,
            )

    #Verify that an ADMINISTRATOR can create a new system user with the selected role
    def test_administrator_can_create_user(self) -> None:
            created = (
                self.app.user_admin_service
                .create_user(
                    actor=self.admin,
                    username="newstaff",
                    full_name="New Staff",
                    email="newstaff@example.com",
                    password="RoleSecure!@#",
                    role=UserRole.BANK_STAFF,
                )
            )
            self.assertEqual(
                created.role,
                UserRole.BANK_STAFF,
            )
            self.assertTrue(
                created.enabled
            )

    #Verify that an ADMINISTRATOR can change another eligible users role
    def test_administrator_can_change_user_role(self) -> None:
            target = self.app.user_admin_service.create_user(
                actor=self.admin,
                username="roleuser",
                full_name="Role User",
                email="role@example.com",
                password="RolePASS!@#",
                role=UserRole.BANK_STAFF,
            )
            updated = self.app.user_admin_service.change_user_role(
                actor=self.admin,
                target=target,
                role=UserRole.ADMINISTRATOR,
            )
            self.assertEqual(
                updated.role,
                UserRole.ADMINISTRATOR,
            )

    #Verify that a CUSTOMER who owns bank accounts cannot be converted to BANK_STAFF
    def test_customer_with_accounts_cannot_be_changed_to_staff(self) -> None:
            with self.assertRaises(
                ValueError
            ):
                self.app.user_admin_service.change_user_role(
                    actor=self.admin,
                    target=self.customer1,
                    role=UserRole.BANK_STAFF,
                )

    #Verify that the active ADMINISTRATOR cannot disable their own account
    def test_administrator_cannot_disable_self(self) -> None:
            with self.assertRaises(
                ValueError
            ):
                self.app.user_admin_service.set_user_enabled(
                    actor=self.admin,
                    target=self.admin,
                    enabled=False,
                )

    #Verify that an ADMINISTRATOR can freeze a CUSTOMER bank account
    def test_administrator_can_freeze_customer_account(self) -> None:
            updated = self.app.user_admin_service.set_account_status(
                actor=self.admin,
                account_id=self.a.account_id,
                status=AccountStatus.FROZEN,
            )
            self.assertEqual(
                updated.status,
                AccountStatus.FROZEN,
            )

    #Verify that an ADMINISTRATOR can clear an active temporary login lockout before expiry
    def test_administrator_can_unlock_temporarily_locked_user(self) -> None:
        self.app.repository.set_customer_lockout(
            self.customer1.customer_id,
            datetime.now(timezone.utc) + timedelta(minutes=5),
        )
        locked = self.app.customer_service.get_customer(
            self.customer1.customer_id
        )
        self.assertIsNotNone(locked)
        self.assertTrue(
            locked.is_temporarily_locked
        )

        unlocked = self.app.user_admin_service.unlock_user(
            actor=self.admin,
            target=locked,
        )

        self.assertTrue(
            unlocked.enabled
        )
        self.assertFalse(
            unlocked.is_temporarily_locked
        )
        self.assertIsNone(
            unlocked.locked_until
        )
        self.assertEqual(
            unlocked.failed_login_attempts,
            0,
        )

    #Verify that View Users clearly displays the TEMP LOCKED state for an affected identity
    def test_view_users_displays_temporary_lockout_status(self) -> None:
        self.app.repository.set_customer_lockout(
            self.customer1.customer_id,
            datetime.now(timezone.utc) + timedelta(minutes=5),
        )
        self.app.session_manager.login(
            "adminuser",
            "AdminPASS!@#",
        )

        console = Mock()
        handler = AdministratorCommandHandler(
            self.app,
            console,
        )
        handler.view_users()

        displayed_rows = [
            str(call.args[0])
            for call in console.admin_info.call_args_list
            if call.args
        ]

        customer_row = next(
            row
            for row in displayed_rows
            if "customer1" in row
        )

        self.assertIn(
            "TEMP LOCKED until",
            customer_row,
        )

