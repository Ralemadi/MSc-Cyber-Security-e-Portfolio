from __future__ import annotations
import tempfile
from pathlib import Path
from banking.app.container import ApplicationContainer
from banking.exceptions import (
    FraudRejectedError,
    TransferPolicyError,
)
from banking.security.roles import UserRole
from banking.services.ai_fraud import SimulatedAISecurityFactory
from banking.services.fraud import LocalSecurityFactory
from banking.services.notifications import (
    CollectingNotificationObserver,
)
from banking.services.transfer_policy import (
    DailyTransferLimitPolicy,
)
from banking.services.transfer_service import TransferService
from base_test_case import BankSecureTestCase


#Group automated checks for transfer risk behaviour
class TransferRiskTests(BankSecureTestCase):
    #Verify that a transfer immediately below the fraud threshold is allowed
    def test_fraud_boundary_4999_99_is_allowed(self) -> None:
            result = self.app.banking_service.transfer(
                actor=self.customer1,
                from_account_id=self.a.account_id,
                to_account_id=self.b.account_id,
                amount="4999.99",
            )
            self.assertTrue(
                result.transaction_reference.startswith(
                    "TXN"
                )
            )

    #Verify that a transfer exactly at the fraud threshold remains allowed
    def test_fraud_boundary_5000_00_is_allowed(self) -> None:
            result = self.app.banking_service.transfer(
                actor=self.customer1,
                from_account_id=self.a.account_id,
                to_account_id=self.b.account_id,
                amount="5000.00",
            )
            self.assertEqual(
                result.risk_decision.risk_score,
                10,
            )

    #Verify that a transfer one cent above the fraud threshold is rejected
    def test_fraud_boundary_5000_01_is_rejected(self) -> None:
            with self.assertRaises(
                FraudRejectedError
            ):
                self.app.banking_service.transfer(
                    actor=self.customer1,
                    from_account_id=self.a.account_id,
                    to_account_id=self.b.account_id,
                    amount="5000.01",
                )

    #Verify that a CUSTOMER may reach the configured daily transfer limit exactly
    def test_daily_limit_exactly_reached_is_allowed(self) -> None:
            self.app.banking_service.transfer(
                actor=self.customer1,
                from_account_id=self.a.account_id,
                to_account_id=self.b.account_id,
                amount="5000.00",
            )
            result = self.app.banking_service.transfer(
                actor=self.customer1,
                from_account_id=self.a.account_id,
                to_account_id=self.b.account_id,
                amount="5000.00",
            )
            self.assertTrue(
                result.transaction_reference.startswith(
                    "TXN"
                )
            )

    #Verify that one cent above the daily transfer limit is blocked.
    def test_daily_limit_plus_one_cent_is_blocked(self) -> None:
            self.app.banking_service.transfer(
                actor=self.customer1,
                from_account_id=self.a.account_id,
                to_account_id=self.b.account_id,
                amount="5000.00",
            )
            self.app.banking_service.transfer(
                actor=self.customer1,
                from_account_id=self.a.account_id,
                to_account_id=self.b.account_id,
                amount="5000.00",
            )

            with self.assertRaises(
                TransferPolicyError
            ):
                self.app.banking_service.transfer(
                    actor=self.customer1,
                    from_account_id=self.a.account_id,
                    to_account_id=self.b.account_id,
                    amount="0.01",
                )

    #Verify that customer-facing transfer messages do not expose internal fraud scores or reasons.
    def test_customer_message_never_leaks_internal_risk_details(self) -> None:
            result = self.app.banking_service.transfer(
                actor=self.customer1,
                from_account_id=self.a.account_id,
                to_account_id=self.b.account_id,
                amount="100.00",
            )
            message = result.customer_message
            self.assertNotIn(
                "score",
                message.lower(),
            )
            self.assertNotIn(
                "LOCAL",
                message,
            )
            self.assertNotIn(
                "AI-PROVIDER",
                message,
            )

    #Verify that authorised audit records retain internal transfer-risk evidence for traceability.
    def test_audit_contains_internal_risk_details(self) -> None:
            result = self.app.banking_service.transfer(
                actor=self.customer1,
                from_account_id=self.a.account_id,
                to_account_id=self.b.account_id,
                amount="100.00",
            )
            records = self.app.audit_service.list_records(
                limit=10
            )
            record = next(
                item
                for item in records
                if (
                    item.action == "TRANSFER"
                    and item.outcome == "COMPLETED"
                )
            )
            self.assertEqual(
                record.risk_score,
                10,
            )
            self.assertIn(
                "LOCAL",
                record.risk_reason,
            )
            self.assertEqual(
                record.details["transaction_reference"],
                result.transaction_reference,
            )

    def test_ai_factory_switch_requires_no_transfer_service_change(self) -> None:
            with tempfile.TemporaryDirectory() as tmp:
                base = Path(tmp)
                app = ApplicationContainer(
                    db_path=base / "db" / "ai.db",
                    audit_path=base / "audit.jsonl",
                    security_factory=SimulatedAISecurityFactory(),
                    console_notifications=False,
                    seed_demo_data=False,
                )
                customer = app.customer_service.register_customer(
                    "aiuser",
                    "AI Test User",
                    "ai@example.com",
                    "SecureAI!@#",
                    role=UserRole.CUSTOMER,
                )
                source = app.account_service.create_account(
                    customer.customer_id,
                    "CURRENT",
                    "5000.00",
                )
                destination = app.account_service.create_account(
                    customer.customer_id,
                    "SAVINGS",
                    "1000.00",
                )
                result = app.banking_service.transfer(
                    actor=customer,
                    from_account_id=source.account_id,
                    to_account_id=destination.account_id,
                    amount="1000.00",
                )
                self.assertIn(
                    "AI-PROVIDER",
                    result.risk_explanation,
                )

    #Verify that the Observer receives only the customer-safe transfer message.
    def test_observer_receives_customer_safe_message(self) -> None:
            observer = CollectingNotificationObserver()
            factory = LocalSecurityFactory()
            service = TransferService(
                repository=self.app.repository,
                transfer_policy=DailyTransferLimitPolicy(
                    self.app.repository
                ),
                fraud_strategy=(
                    factory.create_fraud_strategy()
                ),
                explainer=(
                    factory.create_explainer()
                ),
                observers=[observer],
            )
            service.transfer(
                self.a.account_id,
                self.b.account_id,
                "10.00",
            )
            self.assertEqual(
                len(observer.messages),
                1,
            )
            self.assertNotIn(
                "score",
                observer.messages[0].lower(),
            )

    #Verify that a rejected transfer preserves both account balances.
    def test_rejected_transfer_does_not_change_balances(self) -> None:
            before_a = self.app.account_service.get_account(
                self.a.account_id
            ).balance
            before_b = self.app.account_service.get_account(
                self.b.account_id
            ).balance

            with self.assertRaises(
                FraudRejectedError
            ):
                self.app.banking_service.transfer(
                    actor=self.customer1,
                    from_account_id=self.a.account_id,
                    to_account_id=self.b.account_id,
                    amount="6000.00",
                )

            self.assertEqual(
                self.app.account_service.get_account(
                    self.a.account_id
                ).balance,
                before_a,
            )
            self.assertEqual(
                self.app.account_service.get_account(
                    self.b.account_id
                ).balance,
                before_b,
            )

