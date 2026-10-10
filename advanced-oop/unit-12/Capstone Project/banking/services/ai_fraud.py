from __future__ import annotations

from banking.domain.money import Money
from banking.services.fraud import (
    FraudDecision,
    FraudDetectionStrategy,
    RiskExplanationService,
    SecurityServiceFactory,
)



class SimulatedAIFraudStrategy(FraudDetectionStrategy):
    #Deterministic AI-like provider used only to demonstrate extensibility

    #Evaluate transfer risk and return a structured fraud decision.
    def evaluate(
        self,
        from_account_id: int,
        to_account_id: int,
        amount: Money,
    ) -> FraudDecision:
        score = min(99, 20 + (amount.cents // 100_000) * 10)

        return FraudDecision(
            allowed=score < 80,
            risk_score=int(score),
            reason=(
                "Simulated AI risk score produced through "
                "the provider abstraction."
            ),
        )



class AILikeRiskExplanationService(RiskExplanationService):
    #Convert an internal fraud decision into the configured risk explanation format.
    def explain(self, decision: FraudDecision) -> str:
        return (
            f"AI-PROVIDER: score={decision.risk_score}; "
            f"{decision.reason}"
        )



class SimulatedAISecurityFactory(SecurityServiceFactory):
    #Validate and create the requested fraud strategy through this responsibility boundary
    def create_fraud_strategy(self) -> FraudDetectionStrategy:
        return SimulatedAIFraudStrategy()

    #Validate and create the requested explainer through this responsibility boundary
    def create_explainer(self) -> RiskExplanationService:
        return AILikeRiskExplanationService()
