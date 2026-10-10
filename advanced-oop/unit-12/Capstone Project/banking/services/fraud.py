from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from banking.config import DEFAULT_TRANSFER_REVIEW_LIMIT_CENTS
from banking.domain.money import Money





#Carry the fraud Strategy decision, internal risk score and reason.
@dataclass(frozen=True)
class FraudDecision:
    allowed: bool
    risk_score: int
    reason: str


class FraudDetectionStrategy(ABC):
    #Strategy Pattern contract for transaction risk assessment.
    #Evaluate transfer risk and return a structured fraud decision.
    @abstractmethod
    def evaluate(
        self,
        from_account_id: int,
        to_account_id: int,
        amount: Money,
    ) -> FraudDecision:
        ...


#Provide the risk explanation responsibility through the service layer.
class RiskExplanationService(ABC):
    #Convert an internal fraud decision into the configured risk explanation format.
    @abstractmethod
    def explain(self, decision: FraudDecision) -> str:
        ...


class RuleBasedFraudStrategy(FraudDetectionStrategy):
    #Initialise this component with its required dependencies and local state.
    def __init__(
        self,
        review_limit_cents: int = DEFAULT_TRANSFER_REVIEW_LIMIT_CENTS,
    ) -> None:
        self.review_limit = Money.from_cents(review_limit_cents)

    #Evaluate transfer risk and return a structured fraud decision.
    def evaluate(
        self,
        from_account_id: int,
        to_account_id: int,
        amount: Money,
    ) -> FraudDecision:
        if amount.cents > self.review_limit.cents:
            return FraudDecision(
                allowed=False,
                risk_score=90,
                reason="Amount exceeds the local review threshold.",
            )

        return FraudDecision(
            allowed=True,
            risk_score=10,
            reason="Transaction passed local rule-based checks.",
        )


#Provide the local risk explanation responsibility through the service layer.
class LocalRiskExplanationService(RiskExplanationService):
    #Convert an internal fraud decision into the configured risk explanation format.
    def explain(self, decision: FraudDecision) -> str:
        return (
            f"LOCAL: score={decision.risk_score}; "
            f"{decision.reason}"
        )


class SecurityServiceFactory(ABC):
    #Abstract Factory for compatible risk strategy/explainer families.

    @abstractmethod
    def create_fraud_strategy(self) -> FraudDetectionStrategy:
        ...

    #Validate and create the requested explainer through this responsibility boundary.
    @abstractmethod
    def create_explainer(self) -> RiskExplanationService:
        ...


class LocalSecurityFactory(SecurityServiceFactory):
    def create_fraud_strategy(self) -> FraudDetectionStrategy:
        return RuleBasedFraudStrategy()

    #Validate and create the requested explainer through this responsibility boundary.
    def create_explainer(self) -> RiskExplanationService:
        return LocalRiskExplanationService()
