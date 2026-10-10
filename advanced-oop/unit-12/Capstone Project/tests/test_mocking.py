from __future__ import annotations
import unittest
from datetime import datetime, timezone
from unittest.mock import Mock

from banking.domain.models import (
    Transaction,
    TransactionStatus,
    TransactionType,
)
from banking.domain.money import Money
from banking.repositories.interfaces import BankRepository
from banking.services.fraud import (
    FraudDecision,
    FraudDetectionStrategy,
    RiskExplanationService,
)
from banking.services.notifications import NotificationObserver
from banking.services.transfer_policy import TransferPolicy
from banking.services.transfer_service import TransferService


#Group automated checks for transfer service mocking behaviour
class TransferServiceMockingTests(unittest.TestCase):
    #Create a fresh isolated test environment before each test method
    def setUp(self) -> None:
        self.repository = Mock(spec=BankRepository)
        self.policy = Mock(spec=TransferPolicy)
        self.fraud_strategy = Mock(spec=FraudDetectionStrategy)
        self.explainer = Mock(spec=RiskExplanationService)
        self.observer = Mock(spec=NotificationObserver)

        self.service = TransferService(
            repository=self.repository,
            transfer_policy=self.policy,
            fraud_strategy=self.fraud_strategy,
            explainer=self.explainer,
            observers=[self.observer],
        )

        self.allowed_decision = FraudDecision(
            allowed=True,
            risk_score=25,
            reason="Mock AI assessment allowed the transfer.",
        )

        self.transaction = Transaction(
            transaction_id=77,
            transaction_type=TransactionType.TRANSFER,
            from_account_id=1,
            to_account_id=2,
            amount=Money.parse("125.50"),
            status=TransactionStatus.COMPLETED,
            description="Account transfer",
            created_at=datetime.now(timezone.utc),
        )

    #Verify that TransferService can be tested in isolation with mocked repository, policy, fraud, explanation and notification dependencies.
    def test_transfer_service_isolated_with_mocked_dependencies(self) -> None:
        self.fraud_strategy.evaluate.return_value = self.allowed_decision
        self.explainer.explain.return_value = (
            "MOCK-AI: score=25; transfer allowed."
        )
        self.repository.transfer.return_value = self.transaction

        result = self.service.transfer(
            from_account_id=1,
            to_account_id=2,
            amount="125.50",
        )

        expected_money = Money.parse("125.50")

        self.policy.validate.assert_called_once_with(
            1,
            expected_money,
        )
        self.fraud_strategy.evaluate.assert_called_once_with(
            1,
            2,
            expected_money,
        )
        self.explainer.explain.assert_called_once_with(
            self.allowed_decision
        )
        self.repository.transfer.assert_called_once_with(
            1,
            2,
            expected_money,
            "Account transfer",
        )
        self.observer.update.assert_called_once_with(
            result.customer_message
        )
        self.assertEqual(
            result.transaction_reference,
            "TXN00000077",
        )

    #Verify that a mocked persistence failure prevents transfer notification publication.
    def test_mock_repository_failure_does_not_publish_notification(self) -> None:
        self.fraud_strategy.evaluate.return_value = self.allowed_decision
        self.explainer.explain.return_value = (
            "MOCK-AI: score=25; transfer allowed."
        )
        self.repository.transfer.side_effect = RuntimeError(
            "Simulated repository failure."
        )

        with self.assertRaisesRegex(
            RuntimeError,
            "Simulated repository failure",
        ):
            self.service.transfer(
                from_account_id=1,
                to_account_id=2,
                amount="10.00",
            )

        self.repository.transfer.assert_called_once()
        self.observer.update.assert_not_called()

    #Verify that a simulated AI timeout stops processing before any repository transfer is attempted
    def test_mock_ai_timeout_does_not_reach_repository(self) -> None:
        #A timeout in the risk provider occurs before persistence and cannot alter balances.
        self.fraud_strategy.evaluate.side_effect = TimeoutError(
            "Simulated AI provider timeout."
        )

        with self.assertRaisesRegex(
            TimeoutError,
            "Simulated AI provider timeout",
        ):
            self.service.transfer(
                from_account_id=1,
                to_account_id=2,
                amount="10.00",
            )

        self.repository.transfer.assert_not_called()
        self.explainer.explain.assert_not_called()
        self.observer.update.assert_not_called()

    #Verify that a simulated unavailable AI provider cannot reach the financial persistence operation.
    def test_mock_ai_provider_unavailable_does_not_reach_repository(self) -> None:
        self.fraud_strategy.evaluate.side_effect = ConnectionError(
            "Simulated AI provider unavailable."
        )

        with self.assertRaisesRegex(
            ConnectionError,
            "Simulated AI provider unavailable",
        ):
            self.service.transfer(
                from_account_id=1,
                to_account_id=2,
                amount="10.00",
            )

        self.repository.transfer.assert_not_called()
        self.explainer.explain.assert_not_called()
        self.observer.update.assert_not_called()

    #Verify that a simulated risk-explanation failure occurs before the repository can modify balances.
    def test_mock_ai_explanation_failure_does_not_reach_repository(self) -> None:
        self.fraud_strategy.evaluate.return_value = self.allowed_decision
        self.explainer.explain.side_effect = RuntimeError(
            "Simulated AI explanation failure."
        )

        with self.assertRaisesRegex(
            RuntimeError,
            "Simulated AI explanation failure",
        ):
            self.service.transfer(
                from_account_id=1,
                to_account_id=2,
                amount="10.00",
            )

        self.repository.transfer.assert_not_called()
        self.observer.update.assert_not_called()


if __name__ == "__main__":
    unittest.main(
        verbosity=2
    )
