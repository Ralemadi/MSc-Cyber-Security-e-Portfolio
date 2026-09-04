from __future__ import annotations

import threading
from decimal import Decimal
from typing import Iterable, Sequence

from banking_system import BankAccount


class TransactionSimulator:
    """
    Simulate multiple users operating on the same
    BankAccount concurrently.
    """

    # Each simulated user performs the same transactions.
    DEFAULT_TRANSACTIONS: Sequence[
        tuple[str, Decimal]
    ] = (
        ("deposit", Decimal("100.00")),
        ("withdraw", Decimal("30.00")),
        ("deposit", Decimal("50.00")),
        ("withdraw", Decimal("20.00")),
    )

    def __init__(
        self,
        account: BankAccount,
        user_count: int = 5,
        transactions: Iterable[
            tuple[
                str,
                Decimal | int | float | str
            ]
        ] | None = None,
    ) -> None:

        if not isinstance(account, BankAccount):
            raise TypeError(
                "account must be a BankAccount instance."
            )

        if user_count <= 0:
            raise ValueError(
                "user_count must be greater than zero."
            )

        # Composition: the simulator holds a BankAccount
        # reference and uses only its public methods.
        self.account = account
        self.user_count = user_count

        source = (
            transactions
            if transactions is not None
            else self.DEFAULT_TRANSACTIONS
        )

        self.transactions = tuple(source)

    def _perform_transactions(self) -> None:
        """
        Run the transaction plan for one simulated user.
        """

        for operation, amount in self.transactions:
            if operation == "deposit":
                self.account.deposit(amount)

            elif operation == "withdraw":
                self.account.withdraw(amount)

            else:
                raise ValueError(
                    f"Unsupported transaction type: {operation}"
                )

    def run(self) -> Decimal:
        """
        Start all user threads, wait for them to finish,
        and return the final account balance.
        """

        # Create one thread for each simulated user.
        threads = [
            threading.Thread(
                target=self._perform_transactions,
                name=f"User-{number}",
            )
            for number in range(
                1,
                self.user_count + 1
            )
        ]

        # Start all threads.
        for thread in threads:
            thread.start()

        # Wait until every user has completed.
        for thread in threads:
            thread.join()

        # Read the final balance safely through BankAccount.
        return self.account.get_balance()
