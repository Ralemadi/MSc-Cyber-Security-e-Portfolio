from __future__ import annotations
from banking.config import ALLOWED_ACCOUNT_TYPES
from banking.domain.money import Money
from banking.exceptions import ValidationError


#Validate account input before it reaches persistence or business logic
class AccountValidator:
    #Validation rules for account creation and account types

    #Validate and normalise the supplied account type value
    def account_type(self, value: str) -> str:
        normalised = value.strip().upper()

        if normalised not in ALLOWED_ACCOUNT_TYPES:
            allowed = ", ".join(sorted(ALLOWED_ACCOUNT_TYPES))
            raise ValidationError(
                f"Account type must be one of: {allowed}."
            )

        return normalised

    #Validate the supplied opening balance against account-creation rules
    def opening_balance(self, value: str | int | Money) -> Money:
        return Money.parse(value)
