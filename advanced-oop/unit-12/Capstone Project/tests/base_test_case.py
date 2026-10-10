from __future__ import annotations
import tempfile
import unittest
from pathlib import Path
from banking.app.container import ApplicationContainer
from banking.security.roles import UserRole
from banking.services.fraud import LocalSecurityFactory


class BankSecureTestCase(unittest.TestCase):
    #Create a fresh isolated test environment before each test method
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        base = Path(self.temp.name)
        self.app = ApplicationContainer(
            db_path=base / "db" / "test.db",
            audit_path=base / "audit" / "audit.jsonl",
            security_factory=LocalSecurityFactory(),
            console_notifications=False,
            seed_demo_data=False,
        )

        self.customer1 = self.app.customer_service.register_customer(
            username="customer1",
            full_name="Customer One",
            email="customer1@example.com",
            password="SecureONE!@#",
            role=UserRole.CUSTOMER,
        )
        self.customer2 = self.app.customer_service.register_customer(
            username="customer2",
            full_name="Customer Two",
            email="customer2@example.com",
            password="SecureTWO!@#",
            role=UserRole.CUSTOMER,
        )
        self.staff = self.app.customer_service.register_customer(
            username="staffuser",
            full_name="Bank Staff",
            email="staff@example.com",
            password="StaffPASS!@#",
            role=UserRole.BANK_STAFF,
        )
        self.admin = self.app.customer_service.register_customer(
            username="adminuser",
            full_name="Administrator",
            email="admin@example.com",
            password="AdminPASS!@#",
            role=UserRole.ADMINISTRATOR,
        )

        self.a = self.app.account_service.create_account(
            self.customer1.customer_id,
            "CURRENT",
            "20000.00",
        )
        self.b = self.app.account_service.create_account(
            self.customer1.customer_id,
            "SAVINGS",
            "5000.00",
        )
        self.other = self.app.account_service.create_account(
            self.customer2.customer_id,
            "SALARY",
            "8000.00",
        )

    #Remove the temporary test environment after the test completes
    def tearDown(self) -> None:
        self.temp.cleanup()
