from __future__ import annotations
import sys
import tempfile
import threading
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from banking.app.container import ApplicationContainer
from banking.services.fraud import LocalSecurityFactory
from banking.services.transfer_policy import DailyTransferLimitPolicy
from banking.services.transfer_service import TransferService


#Run the configured concurrent transfer stress workload and return its correctness metrics.
def run_stress_test(
    thread_pairs: int = 10,
    transfers_per_thread: int = 100,
) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)

        app = ApplicationContainer(
            db_path=base / "stress.db",
            audit_path=base / "audit.jsonl",
            security_factory=LocalSecurityFactory(),
            console_notifications=False,
            seed_demo_data=False,
        )

        customer = app.customer_service.register_customer(
            "stressuser",
            "Stress User",
            "stress@example.com",
            "StressTEST!@#",
        )

        a = app.account_service.create_account(
            customer.customer_id,
            "CURRENT",
            "10000.00",
        )

        b = app.account_service.create_account(
            customer.customer_id,
            "SAVINGS",
            "10000.00",
        )

        factory = LocalSecurityFactory()

        service = TransferService(
            repository=app.repository,
            transfer_policy=DailyTransferLimitPolicy(
                app.repository,
                daily_limit_cents=1_000_000_000,
            ),
            fraud_strategy=factory.create_fraud_strategy(),
            explainer=factory.create_explainer(),
            observers=[],
        )

        errors = []

        #Execute one concurrent transfer workload and capture any error for the benchmark result.
        def worker(source, destination):
            try:
                for _ in range(
                    transfers_per_thread
                ):
                    service.transfer(
                        source,
                        destination,
                        "1.00",
                    )
            except Exception as exc:
                errors.append(exc)

        threads = []

        for _ in range(thread_pairs):
            threads.append(
                threading.Thread(
                    target=worker,
                    args=(
                        a.account_id,
                        b.account_id,
                    ),
                )
            )
            threads.append(
                threading.Thread(
                    target=worker,
                    args=(
                        b.account_id,
                        a.account_id,
                    ),
                )
            )

        start = time.perf_counter()

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        elapsed = time.perf_counter() - start

        final_a = app.account_service.get_account(
            a.account_id
        )
        final_b = app.account_service.get_account(
            b.account_id
        )

        print("=== Stress Test Result ===")
        print(f"Threads: {len(threads)}")
        print(
            f"Transfers per thread: "
            f"{transfers_per_thread}"
        )
        print(
            f"Elapsed seconds: {elapsed:.3f}"
        )
        print(
            f"Errors: {len(errors)}"
        )
        print(
            "Final combined balance cents: "
            f"{final_a.balance_cents + final_b.balance_cents}"
        )
        print(
            "Expected combined balance cents: 2000000"
        )


if __name__ == "__main__":
    run_stress_test()
