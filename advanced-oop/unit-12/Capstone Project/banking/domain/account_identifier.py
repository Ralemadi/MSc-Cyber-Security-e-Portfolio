from __future__ import annotations
from banking.config import ACCOUNT_ID_DIGITS, ACCOUNT_PREFIX


MAX_INTERNAL_ACCOUNT_ID = (10 ** ACCOUNT_ID_DIGITS) - 1


#Format the internal account id value for safe public presentation
def format_account_id(account_id: int) -> str:
    #Convert internal integer ID => public QTRxxxxxxxx identifier.
    if not isinstance(account_id, int):
        raise TypeError("Internal account ID must be an integer.")

    if account_id <= 0 or account_id > MAX_INTERNAL_ACCOUNT_ID:
        raise ValueError("Invalid internal account ID.")

    return f"{ACCOUNT_PREFIX}{account_id:0{ACCOUNT_ID_DIGITS}d}"


#Validate and parse the supplied account id into its internal representation
def parse_account_id(public_account_id: str) -> int:
    #Convert public QTRxxxxxxxx identifier => internal integer ID
    if not isinstance(public_account_id, str):
        raise TypeError("Account ID must be provided as text.")

    value = public_account_id.strip().upper()
    expected_length = len(ACCOUNT_PREFIX) + ACCOUNT_ID_DIGITS

    if (
        len(value) != expected_length
        or not value.startswith(ACCOUNT_PREFIX)
    ):
        raise ValueError(
            f"Invalid Account ID. Expected format: "
            f"{ACCOUNT_PREFIX}{'0' * (ACCOUNT_ID_DIGITS - 2)}12"
        )

    numeric_part = value[len(ACCOUNT_PREFIX):]

    if not numeric_part.isdigit():
        raise ValueError(
            f"{ACCOUNT_PREFIX} must be followed by "
            f"{ACCOUNT_ID_DIGITS} digits."
        )

    internal_id = int(numeric_part)

    if internal_id <= 0:
        raise ValueError("Invalid Account ID.")

    return internal_id
