# Tests

This folder contains the automated verification suite for BankSecure.

The tests are separated by responsibility instead of being collected in one
large file.

The current verified suite contains:

```text
61 tests
```

Run the complete suite from the project root:

```bash
python -m unittest discover -s tests -v
```

Expected result:

```text
Ran 61 tests
OK
```

## Test Organisation

| File | Responsibility | Tests |
|---|---|---:|
| `test_domain.py` | Money, identifiers and transaction-domain behaviour | 7 |
| `test_security.py` | Roles, privileges, authentication, sessions, password policy and temporary lockout | 12 |
| `test_authorization.py` | RBAC, resource boundaries, audit access and unlock authorization | 13 |
| `test_user_administration.py` | User/customer administration, roles, account status, unlock and View Users status | 8 |
| `test_banking_services.py` | Deposit/withdraw results and frozen-account behaviour | 2 |
| `test_repository.py` | Repository and automatic database-path creation | 1 |
| `test_transfer.py` | Fraud, transfer policy, audit, Observer, AI factory and rollback behaviour | 10 |
| `test_concurrency.py` | Concurrent transfers and deadlock prevention | 1 |
| `test_seed.py` | Demo users, roles, credentials and account seeding | 1 |
| `test_mocking.py` | Mock Repository, dependency isolation and simulated provider failures | 5 |
| `test_integration.py` | End-to-end three-role workflow | 1 |
| **Total** |  | **61** |

## Shared Test Fixture

```text
base_test_case.py
```

This file is not a test module.

It creates the common temporary environment used by several test groups:

- Temporary SQLite database
- Temporary audit file
- CUSTOMER users
- BANK_STAFF user
- ADMINISTRATOR user
- Test accounts

Each test receives its own temporary environment to reduce interference between
tests.

## Domain Tests

`test_domain.py`

Checks:

- Money parsing
- Zero-value handling
- Negative-value rejection
- Positive-operation rules
- Public account identifiers
- Public transaction references
- Transaction enums

## Security Tests

`test_security.py`

Checks:

- Role privilege sets
- Session login and logout
- Disabled-user login prevention
- Password changes
- Administrator password reset
- Password policy
- Five failed logins trigger a five-minute lockout
- Correct password is rejected during active temporary lockout
- Expired temporary lockout clears automatically

## Authorization Tests

`test_authorization.py`

Checks security boundaries such as:

- CUSTOMER can access only owned accounts
- BANK_STAFF can access CUSTOMER banking accounts
- CUSTOMER cannot access another customer's account
- ADMINISTRATOR cannot perform normal customer banking operations
- CUSTOMER cannot use staff administration
- BANK_STAFF cannot create system users
- CUSTOMER and BANK_STAFF cannot view Administrator audit records
- BANK_STAFF cannot unlock temporarily locked users

## User Administration Tests

`test_user_administration.py`

Checks:

- BANK_STAFF customer creation
- ADMINISTRATOR user creation
- Role changes
- Role-change restrictions for customers with accounts
- Administrator self-disable protection
- Account freezing
- Administrator early temporary-lockout removal
- `View Users` displays `TEMP LOCKED` status

## Banking Service Tests

`test_banking_services.py`

Checks:

- Structured deposit result
- Structured withdrawal result
- Frozen account restrictions

## Repository Test

`test_repository.py`

Checks automatic creation of the database parent directory.

Repository behaviour is also exercised indirectly by the security, transfer,
integration and concurrency tests.

## Transfer Tests

`test_transfer.py`

Checks:

- Fraud boundary below threshold
- Fraud boundary exactly at threshold
- Fraud rejection above threshold
- Daily transfer limit
- Customer-safe error messages
- Internal audit risk details
- Simulated AI security-family switching
- Observer notification behaviour
- Rejected-transfer balance preservation

## Concurrency Test

`test_concurrency.py`

Runs simultaneous opposite-direction transfers.

It verifies that:

```text
No deadlock occurs
No transfer error occurs
Combined account balance is preserved
```

## Mocking Tests

`test_mocking.py`

Uses:

```python
from unittest.mock import Mock
```

Mocked dependencies include:

```text
BankRepository
TransferPolicy
FraudDetectionStrategy
RiskExplanationService
NotificationObserver
```

The tests prove that `TransferService` can be tested without a real SQLite
database or live AI/model provider.

Mock failure cases include:

- AI/provider timeout
- Provider unavailable
- Risk explanation failure
- Repository persistence failure

The tests verify that a provider failure occurs before the financial repository
operation.

## Integration Test

`test_integration.py`

Runs an end-to-end workflow across the three roles:

```text
ADMINISTRATOR
BANK_STAFF
CUSTOMER
```

This confirms that the main components operate correctly when integrated.

## Stress Test

The larger concurrency stress test is outside this folder:

```text
scripts/stress_test.py
```

Run:

```bash
python scripts/stress_test.py
```

Current workload:

```text
20 threads
100 transfers per thread
```

Important expected checks:

```text
Errors: 0
Final combined balance = Expected combined balance
```

## Scalability Test

The multi-level benchmark is:

```text
scripts/scalability_test.py
```

Run:

```bash
python scripts/scalability_test.py
```

It tests:

```text
1 thread
5 threads
10 threads
20 threads
40 threads
```

and automatically writes:

```text
results/scalability_results.csv
```

The important correctness checks are:

```text
errors = 0
balance_conserved = YES
```

Performance timings can vary between computers.

## Test Evidence

Evidence is stored as screenshots in the project-level `images/` folder rather than generated text-result files.

Complete automated test suite:

![61 Automated Tests Passing](../images/full_tests.png)

Stress test:

![Stress Test Result](../images/stress_test.png)

Scalability test:

![Scalability Test Results](../images/scalability_results.png)

Temporary login lockout shown in `View Users`:

![Temporary Login Lockout](../images/lockout_check.png)

Database lockout state:

![Temporary Lockout Database State](../images/lockout_database_check.png)

Authentication and lockout audit events:

![Authentication and Lockout Audit Events](../images/lockout_audit_logs_check.png)

Customer CLI:

![Customer CLI](../images/Customer_CLI.png)

Bank Staff CLI:

![Bank Staff CLI](../images/Staff_CLI.png)

Administrator CLI:

![Administrator CLI](../images/Administrator_CLI.png)

