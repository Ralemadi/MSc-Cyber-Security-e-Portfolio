from __future__ import annotations
from banking.domain.models import AccountStatus
from banking.domain.money import Money
from banking.exceptions import AuthorizationError
from banking.security.privileges import Privilege
from banking.security.roles import UserRole
from banking.services.results import DepositResult
from base_test_case import BankSecureTestCase

class AuthorizationTests(BankSecureTestCase):
    #Verify that a CUSTOMER can list only accounts owned by the same identity.
    def test_customer_only_lists_owned_accounts(self) -> None:
            ids = {
                account.account_id
                for account
                in self.app.banking_service.accessible_accounts(
                    self.customer1,
                    Privilege.VIEW_ACCOUNT_DETAILS,
                )
            }
            self.assertEqual(
                ids,
                {
                    self.a.account_id,
                    self.b.account_id,
                },
            )

    #Verify that BANK_STAFF can list CUSTOMER accounts across the bank-wide service scope
    def test_bank_staff_lists_all_customer_accounts(self) -> None:
            ids = {
                account.account_id
                for account
                in self.app.banking_service.accessible_accounts(
                    self.staff,
                    Privilege.VIEW_ACCOUNT_DETAILS,
                )
            }
            self.assertEqual(
                ids,
                {
                    self.a.account_id,
                    self.b.account_id,
                    self.other.account_id,
                },
            )

    #Verify that a CUSTOMER cannot deposit into another CUSTOMER account through the protected banking facade
    def test_customer_cannot_deposit_to_another_customer_account(self) -> None:
            with self.assertRaises(
                AuthorizationError
            ):
                self.app.banking_service.deposit(
                    actor=self.customer1,
                    account_id=self.other.account_id,
                    amount="10.00",
                )

    #Verify that authorised BANK_STAFF can deposit into a CUSTOMER account
    def test_bank_staff_can_deposit_to_customer_account(self) -> None:
            result = self.app.banking_service.deposit(
                actor=self.staff,
                account_id=self.other.account_id,
                amount="50.00",
            )
            self.assertIsInstance(
                result,
                DepositResult,
            )
            self.assertEqual(
                result.account.balance,
                Money.parse("8050.00"),
            )

    #Verify that ADMINISTRATOR privileges do not implicitly grant normal banking-operation access
            with self.assertRaises(
                AuthorizationError
            ):
                self.app.banking_service.deposit(
                    actor=self.admin,
                    account_id=self.other.account_id,
                    amount="50.00",
                )

    #Verify that only CUSTOMER identities can own bank accounts.
    def test_non_customer_cannot_own_bank_account(self) -> None:
            with self.assertRaises(
                ValueError
            ):
                self.app.account_service.create_account(
                    self.staff.customer_id,
                    "CURRENT",
                    "100.00",
                )

    #Verify that a CUSTOMER cannot invoke the BANK_STAFF customer-creation 
    def test_customer_cannot_use_bank_staff_create_customer_service(self) -> None:
            with self.assertRaises(
                AuthorizationError
            ):
                self.app.bank_staff_service.create_customer_with_account(
                    actor=self.customer1,
                    username="blockedcustomer",
                    full_name="Blocked Customer",
                    email="blocked@example.com",
                    password="BlockedPASS!@#",
                    account_type="CURRENT",
                    opening_balance="100.00",
                )

    #Verify that BANK_STAFF cannot create privileged system users.
    def test_staff_cannot_create_system_user(self) -> None:
            with self.assertRaises(
                AuthorizationError
            ):
                self.app.user_admin_service.create_user(
                    actor=self.staff,
                    username="newstaff",
                    full_name="New Staff",
                    email="newstaff@example.com",
                    password="RoleSecure!@#",
                    role=UserRole.BANK_STAFF,
                )

    #Verify that BANK_STAFF cannot perform ADMINISTRATOR account-status changes
    def test_bank_staff_cannot_change_account_status(self) -> None:
            with self.assertRaises(
                AuthorizationError
            ):
                self.app.user_admin_service.set_account_status(
                    actor=self.staff,
                    account_id=self.a.account_id,
                    status=AccountStatus.FROZEN,
                )

    #Verify that CUSTOMER identities cannot access privileged audit records.
    def test_customer_cannot_view_audit_records(self) -> None:
            with self.assertRaises(
                AuthorizationError
            ):
                self.app.user_admin_service.audit_records(
                    self.customer1
                )

    #Verify that BANK_STAFF identities cannot access privileged audit records
    def test_bank_staff_cannot_view_audit_records(self) -> None:
            with self.assertRaises(
                AuthorizationError
            ):
                self.app.user_admin_service.audit_records(
                    self.staff
                )

    #Verify that an ADMINISTRATOR can retrieve authorised audit records.
    def test_administrator_can_view_audit_records(self) -> None:
            records = self.app.user_admin_service.audit_records(
                self.admin
            )
            self.assertIsInstance(
                records,
                list,
            )

    #Verify that BANK_STAFF cannot clear another users temporary authentication lockout
    def test_bank_staff_cannot_unlock_user(self) -> None:
        with self.assertRaises(
            AuthorizationError
        ):
            self.app.user_admin_service.unlock_user(
                actor=self.staff,
                target=self.customer1,
            )

