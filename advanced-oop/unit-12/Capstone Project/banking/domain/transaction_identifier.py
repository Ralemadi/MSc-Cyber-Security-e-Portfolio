from __future__ import annotations
from banking.config import (
    TRANSACTION_ID_DIGITS,
    TRANSACTION_PREFIX,
)


MAX_INTERNAL_TRANSACTION_ID = (10 ** TRANSACTION_ID_DIGITS) - 1


#Format the internal transaction id value for safe public presentation.
def format_transaction_id(transaction_id: int) -> str:
    #Convert an internal database transaction ID into a public reference.

    if not isinstance(transaction_id, int):
        raise TypeError("Internal transaction ID must be an integer.")

    if (
        transaction_id <= 0
        or transaction_id > MAX_INTERNAL_TRANSACTION_ID
    ):
        raise ValueError("Invalid internal transaction ID.")

    return (
        f"{TRANSACTION_PREFIX}"
        f"{transaction_id:0{TRANSACTION_ID_DIGITS}d}"
    )
