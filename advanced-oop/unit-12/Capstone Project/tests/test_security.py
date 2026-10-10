from __future__ import annotations
import unittest
from datetime import datetime, timedelta, timezone
from banking.exceptions import (
    UserDisabledError,
    UserTemporarilyLockedError,
)
from banking.security.privileges import (
    Privilege,
    privileges_for,
)
from banking.security.roles import UserRole
from base_test_case import BankSecureTestCase


# automated checks for role privilege 
class RolePrivilegeTests(unittest.TestCase):
    #Verify that the CUSTOMER role receives only the intended customer banking privileges
    def test_customer_role_has_customer_privileges_only(self) -> None:
        privileges = privileges_for(
            UserRole.CUSTOMER
        )
        self.assertIn(
            Privilege.TRANSFER_FUNDS,
            privileges,
        )
        self.assertIn(
            Privilege.CHANGE_OWN_PASSWORD,
            privileges,
        )
        self.assertNotIn(
            Privilege.CREATE_CUSTOMER,
            privileges,
        )
        self.assertNotIn(
            Privilege.CREATE_USER,
            privileges,
        )

    #Verify that BANK_STAFF receives banking and customer-administration privileges without system administration
    def test_bank_staff_role_has_banking_and_customer_admin_privileges(self) -> None:
        privileges = privileges_for(
            UserRole.BANK_STAFF
        )
        self.assertIn(
            Privilege.CREATE_CUSTOMER,
            privileges,
        )
        self.assertIn(
            Privilege.ADD_CUSTOMER_ACCOUNT,
            privileges,
        )
        self.assertIn(
            Privilege.DEPOSIT_FUNDS,
            privileges,
        )
        self.assertNotIn(
            Privilege.CREATE_USER,
            privileges,
        )

    #Verify that ADMINISTRATOR receives system-management privileges without normal customer banking privileges.
    def test_administrator_role_has_user_management_but_not_banking_privileges(self) -> None:
        privileges = privileges_for(
            UserRole.ADMINISTRATOR
        )
        self.assertIn(
            Privilege.CREATE_USER,
            privileges,
        )
        self.assertIn(
            Privilege.RESET_USER_PASSWORD,
            privileges,
        )
        self.assertIn(
            Privilege.UNLOCK_USER,
            privileges,
        )
        self.assertIn(
            Privilege.VIEW_AUDIT,
            privileges,
        )
        self.assertNotIn(
            Privilege.DEPOSIT_FUNDS,
            privileges,
        )
        self.assertNotIn(
            Privilege.TRANSFER_FUNDS,
            privileges,
        )


#Group automated checks for authentication security behaviour.
class AuthenticationSecurityTests(BankSecureTestCase):
    #Verify that SessionManager establishes and clears authenticated session state correctly
    def test_session_manager_login_and_logout(self) -> None:
            user = self.app.session_manager.login(
                "customer1",
                "SecureONE!@#",
            )
            self.assertEqual(
                user.username,
                "customer1",
            )
            self.assertTrue(
                self.app.session_manager.is_authenticated
            )
            self.app.session_manager.logout()
            self.assertFalse(
                self.app.session_manager.is_authenticated
            )

    #Verify that administrative disablement blocks login even when the password is correct
    def test_disabled_user_cannot_login(self) -> None:
            disabled = self.app.user_admin_service.set_user_enabled(
                actor=self.admin,
                target=self.customer1,
                enabled=False,
            )
            self.assertFalse(
                disabled.enabled
            )

            with self.assertRaises(
                UserDisabledError
            ):
                self.app.session_manager.login(
                    "customer1",
                    "SecureONE!@#",
                )

    #Verify that a successful self-service password change invalidates the previous password
    def test_change_own_password_invalidates_old_password(self) -> None:
            self.app.profile_service.change_own_password(
                actor=self.customer1,
                current_password="SecureONE!@#",
                new_password="NewSecure!@#",
            )

            self.assertIsNone(
                self.app.customer_service.authenticate(
                    "customer1",
                    "SecureONE!@#",
                )
            )
            self.assertIsNotNone(
                self.app.customer_service.authenticate(
                    "customer1",
                    "NewSecure!@#",
                )
            )

    #Verify that an ADMINISTRATOR password reset makes the new password usable.
    def test_admin_reset_user_password(self) -> None:
            self.app.user_admin_service.reset_user_password(
                actor=self.admin,
                target=self.customer1,
                new_password="ResetPASS!@#",
            )

            self.assertIsNotNone(
                self.app.customer_service.authenticate(
                    "customer1",
                    "ResetPASS!@#",
                )
            )

    #Verify that the documented demonstration password satisfies the configured password policy
    def test_password_policy_accepts_demo_password(self) -> None:
            self.assertTrue(
                self.app.password_policy.validate(
                    "qweQWE!@#",
                    username="user1",
                ).valid
            )

    #Verify that the password policy rejects a weak password.
    def test_password_policy_rejects_weak_password(self) -> None:
            self.assertFalse(
                self.app.password_policy.validate(
                    "password",
                    username="normaluser",
                ).valid
            )

    #Verify that the fifth consecutive failed login creates the configured five-minute temporary lockout
    def test_fifth_failed_login_triggers_five_minute_temporary_lockout(self) -> None:
        for _ in range(4):
            self.assertIsNone(
                self.app.customer_service.authenticate(
                    "customer1",
                    "WrongPASS!@#",
                )
            )

        before_lock = datetime.now(timezone.utc)

        with self.assertRaises(
            UserTemporarilyLockedError
        ) as context:
            self.app.customer_service.authenticate(
                "customer1",
                "WrongPASS!@#",
            )

        after_lock = datetime.now(timezone.utc)
        locked_until = context.exception.locked_until

        self.assertGreaterEqual(
            locked_until,
            before_lock + timedelta(minutes=5),
        )
        self.assertLessEqual(
            locked_until,
            after_lock + timedelta(minutes=5, seconds=1),
        )

        locked_user = self.app.customer_service.get_customer(
            self.customer1.customer_id
        )
        self.assertIsNotNone(locked_user)
        self.assertTrue(
            locked_user.is_temporarily_locked
        )
        self.assertTrue(
            locked_user.enabled
        )
        self.assertEqual(
            locked_user.failed_login_attempts,
            0,
        )

    #Verify that even the correct password is rejected while a temporary authentication lockout is active
    def test_correct_password_is_blocked_during_temporary_lockout(self) -> None:
        locked_until = (
            datetime.now(timezone.utc)
            + timedelta(minutes=5)
        )
        self.app.repository.set_customer_lockout(
            self.customer1.customer_id,
            locked_until,
        )

        with self.assertRaises(
            UserTemporarilyLockedError
        ):
            self.app.session_manager.login(
                "customer1",
                "SecureONE!@#",
            )

        self.assertFalse(
            self.app.session_manager.is_authenticated
        )

    #Verify that an expired temporary lockout clears automatically before successful authentication
    def test_expired_temporary_lockout_clears_automatically(self) -> None:
        self.app.repository.set_customer_lockout(
            self.customer1.customer_id,
            datetime.now(timezone.utc) - timedelta(seconds=1),
        )

        authenticated = self.app.customer_service.authenticate(
            "customer1",
            "SecureONE!@#",
        )

        self.assertIsNotNone(authenticated)
        self.assertIsNone(
            authenticated.locked_until
        )
        self.assertEqual(
            authenticated.failed_login_attempts,
            0,
        )

        refreshed = self.app.customer_service.get_customer(
            self.customer1.customer_id
        )
        self.assertIsNotNone(refreshed)
        self.assertIsNone(
            refreshed.locked_until
        )

