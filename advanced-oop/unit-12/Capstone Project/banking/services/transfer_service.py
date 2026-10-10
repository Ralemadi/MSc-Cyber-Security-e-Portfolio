from __future__ import annotations
import threading
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass
from banking.domain.account_identifier import format_account_id
from banking.domain.models import Transaction
from banking.domain.money import Money
from banking.domain.transaction_identifier import format_transaction_id
from banking.exceptions import FraudRejectedError
from banking.repositories.interfaces import BankRepository
from banking.services.fraud import (
    FraudDecision,
    FraudDetectionStrategy,
    RiskExplanationService,
)
from banking.services.notifications import NotificationObserver
from banking.services.transfer_policy import TransferPolicy


@dataclass(frozen=True)
class TransferResult:
    transaction: Transaction
    amount: Money
    from_account_id: int
    to_account_id: int
    risk_decision: FraudDecision
    risk_explanation: str

    @property
    def transaction_reference(self) -> str:
        return format_transaction_id(self.transaction.transaction_id)

    @property
    def customer_message(self) -> str:
        return (
            f"Reference: {self.transaction_reference} | "
            f"Transferred {self.amount} "
            f"from {format_account_id(self.from_account_id)} "
            f"to {format_account_id(self.to_account_id)}."
        )


class TransferService:
    #Coordinates transfer policy, risk, concurrency and persistence

    _locks: dict[int, threading.RLock] = defaultdict(threading.RLock)
    _locks_guard = threading.Lock()

    #Initialise this component with its required dependencies and local state
    def __init__(
        self,
        repository: BankRepository,
        transfer_policy: TransferPolicy,
        fraud_strategy: FraudDetectionStrategy,
        explainer: RiskExplanationService,
        observers: Iterable[NotificationObserver] = (),
    ) -> None:
        self.repository = repository
        self.transfer_policy = transfer_policy
        self.fraud_strategy = fraud_strategy
        self.explainer = explainer
        self.observers = list(observers)

    #Perform the internal get lock step used by this workflow
    @classmethod
    def _get_lock(cls, account_id: int) -> threading.RLock:
        with cls._locks_guard:
            return cls._locks[account_id]

    #Execute the coordinated transfer workflow through policy, fraud, persistence and notification controls
    def transfer(
        self,
        from_account_id: int,
        to_account_id: int,
        amount: str | int | Money,
        description: str = "Account transfer",
        actor_username: str = "SYSTEM",
    ) -> TransferResult:
        if from_account_id == to_account_id:
            raise ValueError(
                "Source and destination accounts must be different."
            )

        money = Money.parse(amount).require_positive("Transfer amount")
        first_id, second_id = sorted((from_account_id, to_account_id))
        first_lock = self._get_lock(first_id)
        second_lock = self._get_lock(second_id)

        with first_lock:
            with second_lock:

                self.transfer_policy.validate(from_account_id, money)

                #Fraud assessment runs before the repository transfer so rejection cannot partially modify balances
                decision = self.fraud_strategy.evaluate(
                    from_account_id,
                    to_account_id,
                    money,
                )
                explanation = self.explainer.explain(decision)

                if not decision.allowed:
                    raise FraudRejectedError(
                        risk_score=decision.risk_score,
                        risk_reason=explanation,
                    )

                transaction = self.repository.transfer(
                    from_account_id,
                    to_account_id,
                    money,
                    description,
                )

        result = TransferResult(
            transaction=transaction,
            amount=money,
            from_account_id=from_account_id,
            to_account_id=to_account_id,
            risk_decision=decision,
            risk_explanation=explanation,
        )

        for observer in self.observers:
            observer.update(result.customer_message)

        return result
