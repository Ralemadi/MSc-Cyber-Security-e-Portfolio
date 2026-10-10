from __future__ import annotations
import tempfile
import unittest
from pathlib import Path
from banking.app.container import ApplicationContainer
from banking.domain.models import AccountStatus, TransactionType
from banking.exceptions import UserDisabledError
from banking.security.roles import UserRole

#Group automated checks for bank secure integration behaviour
class BankSecureIntegrationTests(unittest.TestCase):
    #Verify one integrated workflow across ADMINISTRATOR, BANK_STAFF and CUSTOMER responsibilities
    def test_three_role_end_to_end_workflow(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            app = ApplicationContainer(
                db_path=base / "db" / "integration.db",
                audit_path=base / "audit" / "audit.jsonl",
                console_notifications=False,
                seed_demo_data=False,
            )

            admin = app.customer_service.register_customer(
                "adminint",
                "Integration Administrator",
                "adminint@example.com",
                "StrongADMIN!@#",
                role=UserRole.ADMINISTRATOR,
            )

            staff = app.user_admin_service.create_user(
                actor=admin,
                username="staffint",
                full_name="Integration Staff",
                email="staffint@example.com",
                password="SecureBank!@#",
                role=UserRole.BANK_STAFF,
            )

            created = (
                app.bank_staff_service
                .create_customer_with_account(
                    actor=staff,
                    username="integrationuser",
                    full_name="Integration Customer",
                    email="integration@example.com",
                    password="IntegrationPASS!@#",
                    account_type="CURRENT",
                    opening_balance="3000.00",
                )
            )
            added = app.bank_staff_service.add_account(
                actor=staff,
                customer=created.customer,
                account_type="SAVINGS",
                opening_balance="1000.00",
            )

            customer = app.session_manager.login(
                "integrationuser",
                "IntegrationPASS!@#",
            )
            deposit = app.banking_service.deposit(
                actor=customer,
                account_id=created.account.account_id,
                amount="200.00",
            )
            transfer = app.banking_service.transfer(
                actor=customer,
                from_account_id=created.account.account_id,
                to_account_id=added.account.account_id,
                amount="300.00",
            )
            history = app.banking_service.history(
                actor=customer,
                account_id=created.account.account_id,
            )

            self.assertEqual(
                str(deposit.amount),
                "200.00",
            )
            self.assertTrue(
                transfer.transaction_reference.startswith(
                    "TXN"
                )
            )
            self.assertTrue(
                any(
                    tx.transaction_type
                    is TransactionType.TRANSFER
                    for tx in history
                )
            )

            app.session_manager.logout()

            app.user_admin_service.set_account_status(
                actor=admin,
                account_id=created.account.account_id,
                status=AccountStatus.FROZEN,
            )
            self.assertEqual(
                app.account_service.get_account(
                    created.account.account_id
                ).status,
                AccountStatus.FROZEN,
            )

            app.user_admin_service.set_user_enabled(
                actor=admin,
                target=created.customer,
                enabled=False,
            )

            with self.assertRaises(
                UserDisabledError
            ):
                app.session_manager.login(
                    "integrationuser",
                    "IntegrationPASS!@#",
                )

            app.user_admin_service.set_user_enabled(
                actor=admin,
                target=created.customer,
                enabled=True,
            )
            app.user_admin_service.reset_user_password(
                actor=admin,
                target=created.customer,
                new_password="ResetINTEGRATION!@#",
            )

            relogged = app.session_manager.login(
                "integrationuser",
                "ResetINTEGRATION!@#",
            )
            self.assertEqual(
                relogged.role,
                UserRole.CUSTOMER,
            )

            actions = {
                record.action
                for record
                in app.audit_service.list_records(
                    limit=100
                )
            }
            self.assertIn(
                "CREATE_USER",
                actions,
            )
            self.assertIn(
                "CREATE_CUSTOMER",
                actions,
            )
            self.assertIn(
                "CREATE_ACCOUNT",
                actions,
            )
            self.assertIn(
                "DEPOSIT",
                actions,
            )
            self.assertIn(
                "TRANSFER",
                actions,
            )
            self.assertIn(
                "DISABLE_USER",
                actions,
            )
            self.assertIn(
                "ENABLE_USER",
                actions,
            )
            self.assertIn(
                "RESET_USER_PASSWORD",
                actions,
            )


if __name__ == "__main__":
    unittest.main(
        verbosity=2
    )
