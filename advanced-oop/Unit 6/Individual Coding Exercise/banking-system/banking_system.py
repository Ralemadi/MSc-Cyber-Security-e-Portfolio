from __future__ import annotations

import threading
from decimal import Decimal, ROUND_HALF_UP


# Monetary values are stored to two decimal places.
_CENT = Decimal("0.01")


def _to_money(
    value: Decimal | int | float | str
) -> Decimal:
    """Convert a numeric value to a two-decimal Decimal amount."""

    return Decimal(str(value)).quantize(
        _CENT,
        rounding=ROUND_HALF_UP
    )


class BankAccount:
    """
    Represent a bank account whose balance operations
    are thread-safe and whose account number is unique
    within the running application.
    """

    # Account numbers are registered once per process so that
    # two BankAccount objects cannot use the same identifier.
    _used_account_numbers: set[str] = set()
    _account_number_lock = threading.Lock()

    def __init__(
        self,
        account_number: str,
        balance: Decimal | int | float | str = 0,
    ) -> None:

        # Validate the account number.
        if not isinstance(account_number, str) or not account_number.strip():
            raise ValueError(
                "Account number must be a non-empty string."
            )

        # Convert and validate the opening balance.
        opening_balance = _to_money(balance)

        if opening_balance < 0:
            raise ValueError(
                "Opening balance cannot be negative."
            )

        # Register the account number atomically to enforce uniqueness.
        clean_account_number = account_number.strip()
        with BankAccount._account_number_lock:
            if clean_account_number in BankAccount._used_account_numbers:
                raise ValueError(
                    "Account number must be unique."
                )
            BankAccount._used_account_numbers.add(clean_account_number)

        # Internal account state.
        self._account_number = clean_account_number
        self._balance = opening_balance

        # Each account has its own balance lock.
        self._lock = threading.Lock()

    @property
    def account_number(self) -> str:
        """Return the account identifier as read-only"""

        return self._account_number

    @property
    def balance(self) -> Decimal:
        """
        Return the balance through the thread-safe
        get_balance() method
        """

        return self.get_balance()

    @staticmethod
    def _validate_amount(
        amount: Decimal | int | float | str,
    ) -> Decimal:
        """
        Validate transaction amounts before changing
        the shared balance
        """

        value = _to_money(amount)

        if value <= 0:
            raise ValueError(
                "Amount must be greater than zero"
            )

        return value

    def deposit(
        self,
        amount: Decimal | int | float | str,
    ) -> Decimal:
        """
        Add money to the account in a thread-safe way
        """

        # Validate before entering the critical section.
        value = self._validate_amount(amount)

        # Only one thread can update the balance at a time.
        with self._lock:
            self._balance += value
            return self._balance

    def withdraw(
        self,
        amount: Decimal | int | float | str,
    ) -> Decimal:
        """
        Withdraw money if sufficient funds are available.
        """

        value = self._validate_amount(amount)

        # The balance check and update are protected
        # by the same lock.
        with self._lock:
            if value > self._balance:
                raise ValueError(
                    "Insufficient funds."
                )

            self._balance -= value
            return self._balance

    def get_balance(self) -> Decimal:
        """
        Return the current balance while holding
        the account lock.
        """

        with self._lock:
            return self._balance

    def transfer_to(
        self,
        other: "BankAccount",
        amount: Decimal | int | float | str,
    ) -> None:
        """
        Transfer money to another account while
        preventing deadlock.
        """

        if not isinstance(other, BankAccount):
            raise TypeError(
                "other must be a BankAccount instance."
            )

        # Prevent transfer to the same account.
        if other is self:
            raise ValueError(
                "Cannot transfer to the same account."
            )

        value = self._validate_amount(amount)

        # Both account locks are always acquired in the
        # same global order. This removes circular wait.
        first, second = sorted(
            (self, other),
            key=lambda account: (
                account.account_number,
                id(account)
            ),
        )

        # Lock both accounts in the same order.
        with first._lock:
            with second._lock:
                if value > self._balance:
                    raise ValueError(
                        "Insufficient funds for transfer."
                    )

                # Both updates happen while both
                # accounts are protected.
                self._balance -= value
                other._balance += value
