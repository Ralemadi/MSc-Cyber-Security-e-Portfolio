# Unit 6 – Concurrency and Parallelism in Object-Oriented Design

**Programme:** MSc Cyber Security  
**Module:** Advanced Object-Oriented Design and Programming  
**Unit:** 6 – Concurrency and Parallelism in Object-Oriented Design

## Unit Summary

During this unit, I explored concurrency and parallelism in object-oriented software, focusing on threads, processes, synchronisation and thread-safe design. The unit showed how shared mutable state can lead to race conditions and deadlocks, and how synchronisation can maintain consistent behaviour in multi-threaded applications (Hunt, 2019; Python Software Foundation, 2026b).

The practical work focused on a thread-safe banking system in Python. `banking_system.py` contains the `BankAccount` class with validation and locking logic, while `transaction_simulator.py` contains the `TransactionSimulator` used to create concurrent user threads. Keeping these components separate helped preserve clear responsibilities and reduced coupling.

## Learning Outcomes

After completing this unit, I was able to:

- Understand the difference between concurrency and parallelism and the roles of threads, processes and synchronisation.
- Recognise race conditions, deadlocks and risks associated with shared mutable state.
- Apply object-oriented principles to write thread-safe Python classes.
- Use locking to protect critical sections and preserve data consistency.
- Separate banking logic from transaction simulation while allowing the simulator to use the public interface.
- Test concurrent software using repeatable scenarios and verify the expected final state.

## Artefacts and Practical Exercises

The main artefact was a thread-safe `BankAccount` implementation with `deposit()`, `withdraw()`, `get_balance()` and `transfer_to()`. A per-account `threading.Lock` protects shared balance state, while transfers use consistent lock ordering to reduce the risk of circular wait and deadlock (Coffman, Elphick and Shoshani, 1971).

Monetary values are represented with `Decimal`, and account identifiers and transaction values are validated before state changes. `Decimal` supports controlled decimal precision and rounding, making it suitable for monetary values (Python Software Foundation, 2026a).

`TransactionSimulator` was implemented separately and creates multiple threads that perform deterministic deposits and withdrawals through the public `BankAccount` interface. This separation supports lower coupling and clearer responsibilities (Martin, 2003).

Seven `unittest` cases covered normal transactions, concurrent deposits and withdrawals, multi-user simulation, mixed workloads and bidirectional transfers for deadlock prevention. All seven tests passed.

| Artefact | Purpose |
|---|---|
| [Unit 6 Portfolio Page](https://ralemadi.github.io/MSc-Cyber-Security-e-Portfolio/advanced-oop/unit-6/unit-6.html) | Main e-Portfolio page for Unit 6 |
| [Individual Coding Exercise](Individual%20Coding%20Exercise/README.md) | Detailed implementation and testing evidence |
| [BankAccount](https://ralemadi.github.io/MSc-Cyber-Security-e-Portfolio/advanced-oop/unit-6/Individual%20Coding%20Exercise/banking-system/banking_system.html) | Thread-safe banking core |
| [TransactionSimulator](https://ralemadi.github.io/MSc-Cyber-Security-e-Portfolio/advanced-oop/unit-6/Individual%20Coding%20Exercise/banking-system/transaction_simulator.html) | Concurrent-user simulation |
| [Unit Tests](https://ralemadi.github.io/MSc-Cyber-Security-e-Portfolio/advanced-oop/unit-6/Individual%20Coding%20Exercise/banking-system/test_banking_system.html) | Seven functional and concurrency tests |

## Architecture and Execution Flow

The architecture separates concurrent-user simulation from banking state management. `TransactionSimulator` creates user threads and calls the public `BankAccount` operations. `BankAccount` validates requests and controls protected balance updates. Deposit and withdrawal operations use per-account locking, while transfers use fixed lock ordering when two account locks are required.

![Architecture and Execution Flow](images/Architecture%20and%20Execution%20Flow.png)

**Figure 1.** Thread-Safe Banking System – Architecture and Execution Flow.

## Testing and Validation

The unit-test suite validates both functional and concurrent behaviour, including deposit and withdrawal operations, concurrent deposits, concurrent withdrawals with overdraft protection, multi-user simulation, mixed concurrent transactions and bidirectional transfers.

![The Unit Testing Result](images/The%20Unit%20Testing%20Result.png)

**Figure 2.** Unit-test execution showing all seven tests completing successfully.

## Unit 6 Reflection

This unit changed the way I think about software correctness. A method is not only required to produce the correct result when executed once but must also remain correct when several execution paths interact with shared state. This made the placement of shared state and the protection of critical sections more important.

Separating `TransactionSimulator` from the banking system also helped me distinguish application behaviour from test and simulation behaviour. `BankAccount` remains responsible for its own integrity regardless of who calls it, while the simulator is free to change its workload without changing the banking class. This combines encapsulation with lower coupling and makes each component easier to explain and test.

## Professional Skills Development and Action Plan

The unit improved my ability to identify shared state, define critical sections and design repeatable tests that create real concurrent behaviour. It also strengthened my understanding of modular design by separating the transaction simulation harness from the banking core.

Going forward, I will consider thread safety when designing tools that use worker threads or shared resources, document lock-ordering rules when multiple locks are required, and use deterministic tests to confirm that shared state remains consistent.

## Repository Structure

```text
Unit-6/
│   README.md
│   unit-6.html
│
├── images/
│   ├── Architecture and Execution Flow.png
│   └── The Unit Testing Result.png
│
└── Individual Coding Exercise/
    │   README.md
    │
    ├── banking-system/
    │   ├── banking_system.html
    │   ├── test_banking_system.html
    │   └── transaction_simulator.html
    │
    └── images/
        ├── Architecture and Execution Flow.png
        └── The Unit Testing Result.png
```

## References

- Coffman, E.G., Elphick, M.J. and Shoshani, A. (1971) ‘System Deadlocks’, *ACM Computing Surveys*, 3(2), pp. 67–78.
- Hunt, J. (2019) *Advanced Guide to Python 3 Programming*. Cham: Springer.
- Martin, R.C. (2003) *Agile Software Development: Principles, Patterns, and Practices*. Prentice Hall.
- Python Software Foundation (2026a) *decimal — Decimal fixed-point and floating-point arithmetic*.
- Python Software Foundation (2026b) *threading — Thread-based parallelism*.
