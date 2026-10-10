from __future__ import annotations
import tempfile
import unittest
from pathlib import Path
from banking.app.container import ApplicationContainer
from banking.security.roles import UserRole

#Group automated checks for demo seed behaviour
class DemoSeedTests(unittest.TestCase):
    #Verify that the demo seed creates the documented users, roles, credentials and CUSTOMER accounts
    def test_final_demo_roles_accounts_and_credentials(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            app = ApplicationContainer(
                db_path=base / "db" / "seed.db",
                audit_path=base / "audit.jsonl",
                console_notifications=False,
                seed_demo_data=True,
            )

            admin = app.customer_service.authenticate(
                "admin",
                "P@ssw0rdQTR!@#",
            )
            staff = app.customer_service.authenticate(
                "staff1",
                "StaffQWE!@#",
            )

            self.assertIsNotNone(admin)
            self.assertIsNotNone(staff)
            self.assertEqual(
                admin.role,
                UserRole.ADMINISTRATOR,
            )
            self.assertEqual(
                staff.role,
                UserRole.BANK_STAFF,
            )
            self.assertEqual(
                app.account_service.list_accounts(
                    admin.customer_id
                ),
                [],
            )
            self.assertEqual(
                app.account_service.list_accounts(
                    staff.customer_id
                ),
                [],
            )

            account_types = set()

            for username in (
                "user1",
                "user2",
                "user3",
            ):
                customer = (
                    app.customer_service.authenticate(
                        username,
                        "qweQWE!@#",
                    )
                )
                self.assertIsNotNone(customer)
                self.assertEqual(
                    customer.role,
                    UserRole.CUSTOMER,
                )
                accounts = app.account_service.list_accounts(
                    customer.customer_id
                )
                self.assertEqual(
                    len(accounts),
                    2,
                )
                account_types.update(
                    account.account_type
                    for account in accounts
                )

            self.assertEqual(
                account_types,
                {
                    "CURRENT",
                    "SAVINGS",
                    "SALARY",
                },
            )
