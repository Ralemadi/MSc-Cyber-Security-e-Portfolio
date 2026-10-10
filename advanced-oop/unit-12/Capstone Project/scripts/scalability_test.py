from __future__ import annotations
import csv
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


THREAD_LEVELS = (1, 5, 10, 20, 40)
TRANSFERS_PER_THREAD = 100
CSV_PATH = PROJECT_ROOT / "results" / "scalability_results.csv"


#Run one isolated scalability level and calculate correctness and throughput metrics.
def run_level(
    thread_count: int,
    transfers_per_thread: int,
) -> dict[str, str | int | float]:
    #Each level uses a fresh temporary database so results are independent.
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)

        app = ApplicationContainer(
            db_path=base / "scalability.db",
            audit_path=base / "audit.jsonl",
            security_factory=LocalSecurityFactory(),
            console_notifications=False,
            seed_demo_data=False,
        )

        customer = app.customer_service.register_customer(
            username=f"scaleuser{thread_count}",
            full_name="Scalability Test User",
            email=f"scale{thread_count}@example.com",
            password="ScaleTEST!@#",
        )

        account_a = app.account_service.create_account(
            customer.customer_id,
            "CURRENT",
            "10000.00",
        )
        account_b = app.account_service.create_account(
            customer.customer_id,
            "SAVINGS",
            "10000.00",
        )

        factory = LocalSecurityFactory()

        transfer_service = TransferService(
            repository=app.repository,
            transfer_policy=DailyTransferLimitPolicy(
                app.repository,
                daily_limit_cents=1_000_000_000,
            ),
            fraud_strategy=factory.create_fraud_strategy(),
            explainer=factory.create_explainer(),
            observers=[],
        )

        errors: list[Exception] = []
        error_lock = threading.Lock()

        #Execute one concurrent transfer workload and capture any error for the benchmark result.
        def worker(
            source_id: int,
            destination_id: int,
        ) -> None:
            try:
                for _ in range(transfers_per_thread):
                    transfer_service.transfer(
                        source_id,
                        destination_id,
                        "1.00",
                    )
            except Exception as exc:
                with error_lock:
                    errors.append(exc)

        threads: list[threading.Thread] = []

        for index in range(thread_count):
            if index % 2 == 0:
                source_id = account_a.account_id
                destination_id = account_b.account_id
            else:
                source_id = account_b.account_id
                destination_id = account_a.account_id

            threads.append(
                threading.Thread(
                    target=worker,
                    args=(
                        source_id,
                        destination_id,
                    ),
                )
            )

        start = time.perf_counter()

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        elapsed = time.perf_counter() - start
        total_operations = (
            thread_count
            * transfers_per_thread
        )
        operations_per_second = (
            total_operations / elapsed
            if elapsed > 0
            else 0.0
        )

        final_a = app.account_service.get_account(
            account_a.account_id
        )
        final_b = app.account_service.get_account(
            account_b.account_id
        )

        final_balance = (
            final_a.balance_cents
            + final_b.balance_cents
        )
        expected_balance = 2_000_000

        return {
            "threads": thread_count,
            "transfers_per_thread": transfers_per_thread,
            "total_operations": total_operations,
            "elapsed_seconds": round(elapsed, 4),
            "operations_per_second": round(
                operations_per_second,
                2,
            ),
            "errors": len(errors),
            "final_balance_cents": final_balance,
            "expected_balance_cents": expected_balance,
            "balance_conserved": (
                "YES"
                if final_balance == expected_balance
                else "NO"
            ),
        }


#Persist the benchmark measurements as reproducible CSV evidence.
def write_csv(
    rows: list[dict[str, str | int | float]],
) -> None:
    CSV_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fieldnames = [
        "threads",
        "transfers_per_thread",
        "total_operations",
        "elapsed_seconds",
        "operations_per_second",
        "errors",
        "final_balance_cents",
        "expected_balance_cents",
        "balance_conserved",
    ]

    with CSV_PATH.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
        )
        writer.writeheader()
        writer.writerows(rows)


#Build the application and start the requested BankSecure workflow.
def main() -> None:
    results = [
        run_level(
            thread_count=level,
            transfers_per_thread=TRANSFERS_PER_THREAD,
        )
        for level in THREAD_LEVELS
    ]

    write_csv(results)

    print("=== Scalability Test Results ===")
    print(
        f"{'Threads':>7} "
        f"{'Operations':>10} "
        f"{'Seconds':>10} "
        f"{'Ops/sec':>12} "
        f"{'Errors':>7} "
        f"{'Balance':>9}"
    )

    for row in results:
        print(
            f"{row['threads']:>7} "
            f"{row['total_operations']:>10} "
            f"{row['elapsed_seconds']:>10} "
            f"{row['operations_per_second']:>12} "
            f"{row['errors']:>7} "
            f"{row['balance_conserved']:>9}"
        )

    print(
        f"\nCSV results: "
        f"{CSV_PATH.relative_to(PROJECT_ROOT)}"
    )

    if any(
        int(row["errors"]) != 0
        or row["balance_conserved"] != "YES"
        for row in results
    ):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
