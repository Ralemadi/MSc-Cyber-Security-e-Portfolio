from __future__ import annotations
from collections import Counter
from typing import Any
from banking.domain.models import Account, Transaction
from banking.domain.money import Money


class PortfolioSummaryVisitor:
    #Visitor Pattern implementation for portfolio/bank summaries.

    #Initialise this component with its required dependencies and local state.
    def __init__(self) -> None:
        self.total_balance = Money.zero()
        self.account_count = 0
        self.transaction_count = 0
        self.transaction_types: Counter[str] = Counter()

    #Accumulate summary information from the visited account entity.
    def visit_account(self, account: Account) -> None:
        self.account_count += 1
        self.total_balance = self.total_balance + account.balance

    #Accumulate summary information from the visited transaction entity.
    def visit_transaction(self, transaction: Transaction) -> None:
        self.transaction_count += 1
        self.transaction_types[transaction.transaction_type.value] += 1

    #Return the accumulated Visitor summary without changing the visited domain objects.
    def result(self) -> dict[str, Any]:
        return {
            "account_count": self.account_count,
            "total_balance": self.total_balance,
            "transaction_count": self.transaction_count,
            "transaction_types": dict(self.transaction_types),
        }
