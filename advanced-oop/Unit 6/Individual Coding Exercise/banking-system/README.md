# Thread-Safe Banking System

A small Python banking system designed to demonstrate safe concurrent access to shared account balances.

The project provides a `BankAccount` class for deposits, withdrawals, balance checks, and account-to-account transfers. A separate `TransactionSimulator` can create multiple user threads that operate on the same account concurrently. The included unit tests verify normal operations, concurrent workloads, balance consistency, and deadlock prevention.

## Features

- Thread-safe deposits, withdrawals, and balance reads
- Account-to-account transfers
- Per-account locking with `threading.Lock`
- Consistent lock ordering for transfer deadlock prevention
- Monetary values handled with `Decimal`
- Values quantised to two decimal places
- Validation for invalid transaction amounts
- Insufficient-funds protection
- Self-transfer protection
- Unique account-number enforcement within the running application
- Concurrent transaction simulation
- Custom deposit/withdraw transaction sequences
- Unit tests for normal and concurrent behaviour

## Project Structure

```text
banking-system/
├── banking_system.py
├── transaction_simulator.py
└── test_banking_system.py
```

### `banking_system.py`

Contains the core `BankAccount` class.

Main operations:

```python
deposit(amount)
withdraw(amount)
get_balance()
transfer_to(other, amount)
```

Each account owns its balance and its own lock. Balance updates and reads are protected so that multiple threads cannot modify the same account state at the same time.

Account numbers are registered when an account is created. Creating a second `BankAccount` with the same account number raises `ValueError`, keeping the identifier unique within the running application.

Transfers lock both participating accounts in a consistent order before changing either balance. This avoids circular lock waiting during opposite-direction transfers.

### `transaction_simulator.py`

Contains `TransactionSimulator`, which simulates multiple users operating on one shared `BankAccount`.

The simulator:

- creates one thread per simulated user
- runs the same transaction sequence for each user
- waits for all threads to complete
- returns the final account balance
- supports a custom transaction sequence

The default transaction plan for each user is:

```text
Deposit   100.00
Withdraw   30.00
Deposit    50.00
Withdraw   20.00
-----------------
Net change +100.00
```

### `test_banking_system.py`

Contains seven unit tests covering:

1. Basic deposit
2. Basic withdrawal
3. Concurrent deposits
4. Concurrent withdrawals with overdraft protection
5. Multi-user `TransactionSimulator`
6. Mixed concurrent deposits and withdrawals
7. Bidirectional transfers and deadlock prevention

## Requirements

- Python 3.10 or later
- No external Python packages are required

The project uses only Python standard-library modules such as:

```text
threading
decimal
unittest
typing
```

## Basic Usage

```python
from banking_system import BankAccount

account = BankAccount("ACC-001", "1000.00")

account.deposit("250.00")
account.withdraw("100.00")

print(account.get_balance())
```

Expected balance:

```text
1150.00
```

## Transfer Between Accounts

```python
from banking_system import BankAccount

account_a = BankAccount("ACC-A", "500.00")
account_b = BankAccount("ACC-B", "200.00")

account_a.transfer_to(account_b, "100.00")

print(account_a.get_balance())  # 400.00
print(account_b.get_balance())  # 300.00
```

## Concurrent Transaction Simulation

```python
from banking_system import BankAccount
from transaction_simulator import TransactionSimulator

account = BankAccount("ACC-001", "1000.00")

simulator = TransactionSimulator(
    account,
    user_count=5,
)

final_balance = simulator.run()

print(final_balance)
```

With the default transaction plan, each user adds a net `100.00`. Five users therefore change an opening balance of `1000.00` to:

```text
1500.00
```

## Custom Transaction Sequence

A custom deposit/withdraw workload can be supplied without changing the banking logic:

```python
from decimal import Decimal

from banking_system import BankAccount
from transaction_simulator import TransactionSimulator

account = BankAccount("ACC-002", "1000.00")

simulator = TransactionSimulator(
    account,
    user_count=10,
    transactions=[
        ("deposit", Decimal("20.00")),
        ("withdraw", Decimal("10.00")),
    ],
)

print(simulator.run())
```

Each user adds a net `10.00`, so the expected final balance is:

```text
1100.00
```

## Thread Safety

Each `BankAccount` instance contains its own `threading.Lock`.

Operations that read or modify the shared balance are protected by the lock:

```text
deposit()     → validate → acquire lock → update balance
withdraw()    → validate → acquire lock → check funds → update balance
get_balance() → acquire lock → read balance
```

This prevents multiple threads from changing the same balance simultaneously.

## Deadlock Prevention

Transfers require access to two account locks. Before a transfer is performed, the two accounts are sorted into a consistent locking order.

Conceptually:

```text
Account A ─┐
           ├─ determine lock order ─> lock first ─> lock second ─> transfer
Account B ─┘
```

Using the same ordering rule prevents opposite-direction transfers from acquiring the two locks in conflicting order.

## Validation

The banking core rejects:

- empty account identifiers
- duplicate account identifiers
- negative opening balances
- zero or negative transaction amounts
- withdrawals greater than the available balance
- transfers greater than the available balance
- transfers to the same account
- transfer targets that are not `BankAccount` instances

## Running the Tests

From the project directory:

```bash
python -m unittest -v test_banking_system.py
```

You can also run the test file directly:

```bash
python test_banking_system.py
```

Expected result:

```text
Ran 7 tests

OK
```

The test suite validates both expected and observed balances for normal and concurrent scenarios.

## Example Test Coverage

| Test | Scenario | Expected Result |
|---|---|---:|
| T1 | Deposit `50.00` into `100.00` | `150.00` |
| T2 | Withdraw `40.00` from `100.00` | `60.00` |
| T3 | 20 threads × 100 deposits × `1.00` | `2000.00` |
| T4 | 20 threads attempt to withdraw `10.00` from `100.00` | `0.00`, no overdraft |
| T5 | 5-user default simulation starting at `1000.00` | `1500.00` |
| T6 | 10-user mixed deposit `20.00` / withdraw `10.00` | `1100.00` |
| T7 | 100 × `1.00` opposite transfers in each direction | No deadlock; balances preserved |


## References

**Coffman, E.G., Elphick, M.J. and Shoshani, A. (1971)** 'System deadlocks', *ACM Computing Surveys*, 3(2), pp. 67-78.

**Python Software Foundation (2026)** *threading - Thread-based parallelism*. Python 3.14 documentation. Available at: https://docs.python.org/3/library/threading.html .

**Scarfone, K., Souppaya, M. and Dodson, D. (2022)** *Secure Software Development Framework (SSDF) Version 1.1: Recommendations for Mitigating the Risk of Software Vulnerabilities*. NIST SP 800-218. Available at: https://doi.org/10.6028/NIST.SP.800-218 .

