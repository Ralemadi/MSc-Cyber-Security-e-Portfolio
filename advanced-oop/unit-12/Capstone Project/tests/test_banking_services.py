from __future__ import annotations
from banking.domain.models import AccountStatus
from banking.exceptions import AccountStatusError
from banking.services.results import (
    DepositResult,
    WithdrawalResult,
)
from base_test_case import BankSecureTestCase


#Group automated checks for banking service behaviour
class BankingServiceTests(BankSecureTestCase):
    #Verify that a FROZEN account rejects deposit operations
    def test_frozen_account_blocks_deposit(self) -> None:
            self.app.user_admin_service.set_account_status(
                actor=self.admin,
                account_id=self.a.account_id,
                status=AccountStatus.FROZEN,
            )

            with self.assertRaises(
                AccountStatusError
            ):
                self.app.banking_service.deposit(
                    actor=self.customer1,
                    account_id=self.a.account_id,
                    amount="10.00",
                )

    #Verify that deposit and withdrawal operations return typed structured result objects
    def test_deposit_and_withdraw_return_structured_results(self) -> None:
            deposit = self.app.banking_service.deposit(
                actor=self.customer1,
                account_id=self.a.account_id,
                amount="100.00",
            )
            withdraw = self.app.banking_service.withdraw(
                actor=self.customer1,
                account_id=self.a.account_id,
                amount="50.00",
            )
            self.assertIsInstance(
                deposit,
                DepositResult,
            )
            self.assertIsInstance(
                withdraw,
                WithdrawalResult,
            )

