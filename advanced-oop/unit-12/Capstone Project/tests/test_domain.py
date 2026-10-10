from __future__ import annotations
import unittest

from banking.domain.account_identifier import (
    format_account_id,
    parse_account_id,
)
from banking.domain.models import (
    TransactionStatus,
    TransactionType,
)
from banking.domain.money import Money
from banking.domain.transaction_identifier import (
    format_transaction_id,
)
from banking.exceptions import InvalidAmountError
from base_test_case import BankSecureTestCase


class MoneyTests(unittest.TestCase):
    #Verify that Money parses a two-decimal financial amount into exact integer cents
    def test_money_parses_two_decimal_places(self) -> None:
        self.assertEqual(
            Money.parse("125.50").cents,
            12_550,
        )
        self.assertEqual(
            str(Money.parse("125.5")),
            "125.50",
        )

    #Verify that zero is valid when Money represents a stored balance
    def test_money_allows_zero_for_balances(self) -> None:
        self.assertEqual(
            Money.parse("0.00"),
            Money.zero(),
        )

    #Verify that the Money Value Object rejects negative stored values.
    def test_money_rejects_negative_values(self) -> None:
        with self.assertRaises(
            InvalidAmountError
        ):
            Money.parse("-0.01")

    #Verify that operations requiring a positive amount reject zero
    def test_positive_operation_rejects_zero(self) -> None:
        with self.assertRaises(
            InvalidAmountError
        ):
            Money.zero().require_positive(
                "Transfer amount"
            )


#Group automated checks for domain model behaviour.
class DomainModelTests(BankSecureTestCase):
    #Verify that internal account IDs round-trip through the public QTR identifier format.
    def test_public_account_identifier(self) -> None:
            self.assertEqual(
                format_account_id(12),
                "QTR00000012",
            )
            self.assertEqual(
                parse_account_id("QTR00000012"),
                12,
            )

    #Verify that internal transaction IDs are exposed through the public TXN reference format
    def test_public_transaction_reference(self) -> None:
            self.assertEqual(
                format_transaction_id(125),
                "TXN00000125",
            )

    #Verify that transaction type and status use the defined Enum values
    def test_transaction_model_uses_enums(self) -> None:
            history = self.app.account_service.history(
                self.a.account_id
            )
            opening = history[0]
            self.assertIs(
                opening.transaction_type,
                TransactionType.OPENING_BALANCE,
            )
            self.assertIs(
                opening.status,
                TransactionStatus.COMPLETED,
            )

