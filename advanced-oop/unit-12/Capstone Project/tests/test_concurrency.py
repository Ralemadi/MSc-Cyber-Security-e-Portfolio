from __future__ import annotations
import threading
from banking.services.fraud import LocalSecurityFactory
from banking.services.transfer_policy import (
    DailyTransferLimitPolicy,
)
from banking.services.transfer_service import TransferService
from base_test_case import BankSecureTestCase





class ConcurrencyTests(BankSecureTestCase):
    #Verify that opposite-direction concurrent transfers complete without deadlock and conserve the combined balance
    def test_concurrent_bidirectional_transfers_do_not_deadlock(self) -> None:
            factory = LocalSecurityFactory()
            service = TransferService(
                repository=self.app.repository,
                transfer_policy=DailyTransferLimitPolicy(
                    self.app.repository,
                    daily_limit_cents=100_000_000,
                ),
                fraud_strategy=(
                    factory.create_fraud_strategy()
                ),
                explainer=(
                    factory.create_explainer()
                ),
                observers=[],
            )
            errors: list[Exception] = []

            #Execute one concurrent transfer workload and capture any error for the benchmark result
            def worker(
                source: int,
                destination: int,
            ) -> None:
                try:
                    for _ in range(20):
                        service.transfer(
                            source,
                            destination,
                            "1.00",
                        )
                except Exception as exc:
                    errors.append(exc)

            initial_total = (
                self.a.balance.cents
                + self.b.balance.cents
            )
            t1 = threading.Thread(
                target=worker,
                args=(
                    self.a.account_id,
                    self.b.account_id,
                ),
            )
            t2 = threading.Thread(
                target=worker,
                args=(
                    self.b.account_id,
                    self.a.account_id,
                ),
            )
            t1.start()
            t2.start()
            t1.join(timeout=10)
            t2.join(timeout=10)

            self.assertFalse(
                t1.is_alive()
            )
            self.assertFalse(
                t2.is_alive()
            )
            self.assertEqual(
                errors,
                [],
            )
            final_total = (
                self.app.account_service.get_account(
                    self.a.account_id
                ).balance.cents
                + self.app.account_service.get_account(
                    self.b.account_id
                ).balance.cents
            )
            self.assertEqual(
                final_total,
                initial_total,
            )

