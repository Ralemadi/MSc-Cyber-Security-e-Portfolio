from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from banking.config import DEFAULT_DAILY_TRANSFER_LIMIT_CENTS
from banking.domain.money import Money
from banking.exceptions import TransferPolicyError
from banking.repositories.interfaces import BankRepository


#Encapsulate the transfer rule independently from orchestration code.
class TransferPolicy(ABC):

    @abstractmethod
    def validate(self, from_account_id: int, amount: Money) -> None:
        ...


#Policy object that enforces the configured daily outgoing-transfer limit.
class DailyTransferLimitPolicy(TransferPolicy):
    #Initialise this component with its required dependencies and local state.
    def __init__(
        self,
        repository: BankRepository,
        daily_limit_cents: int = DEFAULT_DAILY_TRANSFER_LIMIT_CENTS,
    ) -> None:
        self.repository = repository
        self.daily_limit = Money.from_cents(daily_limit_cents)

    #Evaluate the supplied value against this component's validation rules.
    def validate(self, from_account_id: int, amount: Money) -> None:
        now = datetime.now(timezone.utc)
        start_of_day = now.replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )
        already_sent = self.repository.sum_outgoing_transfers_since(
            from_account_id,
            start_of_day,
        )

        if already_sent.cents + amount.cents > self.daily_limit.cents:
            raise TransferPolicyError(
                "Transfer exceeds the daily transfer limit of "
                f"{self.daily_limit}."
            )
