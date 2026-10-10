from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import Self
from banking.exceptions import InvalidAmountError


#Value Object that stores money as integer cents and validates monetary operations.
@dataclass(frozen=True, order=True)
class Money:
    #Immutable money value object stored internally as integer cents.

    cents: int

    #Reject invalid Money state immediately after dataclass construction.
    def __post_init__(self) -> None:
        if not isinstance(self.cents, int):
            raise TypeError("Money cents must be an integer.")

        if self.cents < 0:
            raise InvalidAmountError("Money cannot be negative.")

    #Create a zero-value Money instance for account-balance calculations.
    @classmethod
    def zero(cls) -> Self:
        return cls(0)

    #Create Money directly from a validated integer-cent value.
    @classmethod
    def from_cents(cls, cents: int) -> Self:
        return cls(cents)

    #Parse user-facing decimal money input into exact integer cents.
    @classmethod
    def parse(cls, value: str | int | Decimal | "Money") -> Self:
        if isinstance(value, Money):
            return cls(value.cents)

        try:
            amount = Decimal(str(value)).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )
        except (InvalidOperation, ValueError) as exc:
            raise InvalidAmountError("Invalid monetary amount.") from exc

        if amount < 0:
            raise InvalidAmountError("Money cannot be negative.")

        return cls(int(amount * 100))

    #Enforce the required positive before returning control to the caller.
    def require_positive(self, label: str = "Amount") -> Self:
        if self.cents <= 0:
            raise InvalidAmountError(
                f"{label} must be greater than zero."
            )

        return self

    #Format Money with two decimal places for user-facing display.
    def __str__(self) -> str:
        return f"{Decimal(self.cents) / Decimal(100):.2f}"

    #Add two Money values while preserving the integer-cent representation.
    def __add__(self, other: "Money") -> "Money":
        if not isinstance(other, Money):
            raise TypeError("Money can only be added to Money.")

        return Money.from_cents(self.cents + other.cents)

    #Subtract two Money values while preserving validation rules.
    def __sub__(self, other: "Money") -> "Money":
        if not isinstance(other, Money):
            raise TypeError("Money can only subtract Money.")

        result = self.cents - other.cents

        if result < 0:
            raise InvalidAmountError(
                "Money subtraction cannot produce a negative result."
            )

        return Money.from_cents(result)
