"""Unit tests for the Unit 6 thread-safe banking system.

The tests validate normal account behaviour, concurrent access, the separate
TransactionSimulator component, and deadlock prevention.
"""

import threading
import unittest
from decimal import Decimal

from banking_system import BankAccount
from transaction_simulator import TransactionSimulator


class BankAccountTests(unittest.TestCase):

    # Test 1: Basic Deposit
    def test_01_deposit(self):
        """Deposit should update the balance correctly."""

        account = BankAccount("ACC-001", "100.00")
        account.deposit("50.00")

        expected = Decimal("150.00")
        actual = account.get_balance()

        print("\n--- Deposit Test ---")
        print(f"Expected balance: {expected:.2f}")
        print(f"Actual balance:   {actual:.2f}")

        self.assertEqual(actual, expected)

        # The account number is a unique identifier. Creating
        # another account with the same number must be rejected.
        with self.assertRaises(ValueError):
            BankAccount("ACC-001", "0.00")

    # Test 2: Basic Withdrawal

    def test_02_withdraw(self):
        """Withdrawal should update the balance correctly."""

        account = BankAccount("ACC-002", "100.00")
        account.withdraw("40.00")

        expected = Decimal("60.00")
        actual = account.get_balance()

        print("\n--- Withdrawal Test ---")
        print(f"Expected balance: {expected:.2f}")
        print(f"Actual balance:   {actual:.2f}")

        self.assertEqual(actual, expected)


    # Test 3: Concurrent Deposits
    def test_03_concurrent_deposits(self):
        """Concurrent deposits should not lose balance updates."""

        account = BankAccount("ACC-003", "0.00")

        def deposit_worker():
            for _ in range(100):
                account.deposit("1.00")

        # 20 users x 100 deposits x 1.00 = 2000.00
        threads = [
            threading.Thread(target=deposit_worker)
            for _ in range(20)
        ]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        expected = Decimal("2000.00")
        actual = account.get_balance()

        print("\n--- Concurrent Deposit Test ---")
        print("Concurrent users: 20")
        print("Deposits/user:     100")
        print("Deposit amount:    1.00")
        print(f"Expected balance:  {expected:.2f}")
        print(f"Actual balance:    {actual:.2f}")

        self.assertEqual(actual, expected)

    # Test 4: Concurrent Withdrawals

    def test_04_concurrent_withdrawals(self):
        """Concurrent withdrawals should never overdraw the account."""

        account = BankAccount("ACC-004", "100.00")

        def withdraw_worker():
            try:
                account.withdraw("10.00")
            except ValueError:
                # Once the balance reaches zero, further withdrawals
                # are expected to be rejected by BankAccount.
                pass

        # 20 users attempt to withdraw 10.00 from 100.00.
        # Only 10 withdrawals can succeed.
        threads = [
            threading.Thread(target=withdraw_worker)
            for _ in range(20)
        ]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        expected = Decimal("0.00")
        actual = account.get_balance()

        print("\n--- Concurrent Withdrawal Test ---")
        print("Concurrent users: 20")
        print("Opening balance:  100.00")
        print("Withdrawal/user:  10.00")
        print(f"Expected balance: {expected:.2f}")
        print(f"Actual balance:   {actual:.2f}")

        self.assertEqual(actual, expected)


    # Test 5: Transaction Simulator
    def test_05_transaction_simulator(self):
        """Multiple simulated users should produce the expected final balance."""

        account = BankAccount("ACC-005", "1000.00")
        simulator = TransactionSimulator(account, user_count=5)

        actual = simulator.run()

        # Default transaction plan per user:
        # +100 -30 +50 -20 = +100
        # Five users therefore add 500.00 to 1000.00.
        expected = Decimal("1500.00")

        print("\n--- Transaction Simulator Test ---")
        print("Concurrent users: 5")
        print("Opening balance:  1000.00")
        print("Net change/user:  +100.00")
        print(f"Expected balance: {expected:.2f}")
        print(f"Actual balance:   {actual:.2f}")

        self.assertEqual(actual, expected)


    # Test 6: Mixed Concurrent Transactions

    def test_06_mixed_concurrent_transactions(self):
        """Concurrent deposits and withdrawals should preserve the calculated result."""

        account = BankAccount("ACC-006", "1000.00")
        simulator = TransactionSimulator(
            account,
            user_count=10,
            transactions=[
                ("deposit", Decimal("20.00")),
                ("withdraw", Decimal("10.00")),
            ],
        )

        actual = simulator.run()

        # Each user adds a  10.00.
        # 10 users x 10.00 = +100.00.
        expected = Decimal("1100.00")

        print("\n--- Mixed Concurrent Transaction Test ---")
        print("Concurrent users: 10")
        print("Deposit/user:     20.00")
        print("Withdrawal/user:  10.00")
        print("Opening balance:  1000.00")
        print(f"Expected balance: {expected:.2f}")
        print(f"Actual balance:   {actual:.2f}")

        self.assertEqual(actual, expected)


    # Test 7: Deadlock Prevention
    def test_07_bidirectional_transfer(self):
        """Opposite transfers should finish without deadlock and conserve funds."""

        account_a = BankAccount("ACC-007-A", "500.00")
        account_b = BankAccount("ACC-007-B", "500.00")
        start = threading.Barrier(2)

        def a_to_b():
            start.wait()
            for _ in range(100):
                account_a.transfer_to(account_b, "1.00")

        def b_to_a():
            start.wait()
            for _ in range(100):
                account_b.transfer_to(account_a, "1.00")

        thread_a = threading.Thread(target=a_to_b, name="Transfer-A-to-B")
        thread_b = threading.Thread(target=b_to_a, name="Transfer-B-to-A")

        thread_a.start()
        thread_b.start()

        # If a circular-wait deadlock occurs, one or both threads
        # will still be alive after the timeout.
        thread_a.join(timeout=5)
        thread_b.join(timeout=5)

        self.assertFalse(
            thread_a.is_alive(),
            "Transfer A-to-B appears deadlocked",
        )
        self.assertFalse(
            thread_b.is_alive(),
            "Transfer B-to-A appears deadlocked",
        )

        expected_a = Decimal("500.00")
        expected_b = Decimal("500.00")
        actual_a = account_a.get_balance()
        actual_b = account_b.get_balance()

        print("\n--- Bidirectional Transfer Test ---")
        print(f"Expected Account A: {expected_a:.2f}")
        print(f"Actual Account A:   {actual_a:.2f}")
        print(f"Expected Account B: {expected_b:.2f}")
        print(f"Actual Account B:   {actual_b:.2f}")
        print("Deadlock:            No")

        self.assertEqual(actual_a, expected_a)
        self.assertEqual(actual_b, expected_b)
        self.assertEqual(
            actual_a + actual_b,
            Decimal("1000.00"),
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
