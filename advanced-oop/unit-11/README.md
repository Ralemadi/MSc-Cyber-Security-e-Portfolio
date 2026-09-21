# Unit 11 – Dependency Injection and Inversion of Control (IoC)

**Programme:** MSc Cyber Security  
**Module:** Advanced Object-Oriented Design and Programming  
**Unit:** 11 – Dependency Injection and Inversion of Control (IoC)

## Unit Summary

During this unit, I explored **Dependency Injection (DI)** and **Inversion of Control (IoC)** as design principles for reducing coupling between software components. The unit focused on how dependencies can be supplied to objects rather than created internally, making code more flexible, modular and easier to test (Fowler, M. (2004)).

The unit also introduced the role of DI frameworks such as **Spring** and **Google Guice** in managing dependencies in larger systems. The practical exercise applies the same principles in Python through a small refactoring activity.

## Learning Outcomes

By the end of this unit, I was able to:

- Explain the principles of Dependency Injection and Inversion of Control.
- Recognise how dependency management can reduce tight coupling between components.
- Understand how DI frameworks can support flexible, modular and testable software.
- Apply Dependency Injection in a Python application.
- Reflect on how DI and IoC can improve maintainability and scalability.

## Artefacts and Practical Exercises

The main practical activity required refactoring a simple Python application in which `UserManager` directly created an `EmailService`. This design created tight coupling because the notification dependency was fixed inside `UserManager`, and it also reduced testability because testing the manager depended on the real email service (Pryce, N. (2010)).

The refactoring introduces a common notification abstraction and changes `UserManager` so that the required notification service is supplied from outside. This applies Dependency Injection and shifts control over dependency creation away from the class that uses the dependency (Martin, R.C. (2000)).

| Artefact | Purpose |
|---|---|
| [Unit 11 Portfolio Page](https://ralemadi.github.io/MSc-Cyber-Security-e-Portfolio/advanced-oop/unit-11/unit-11.html) | Main e-Portfolio page for Unit 11 |
| [Case Study Activity](https://github.com/Ralemadi/MSc-Cyber-Security-e-Portfolio/tree/main/advanced-oop/unit-11/Case%20Study%20Activity/) | Original coupling problem, DI refactoring and testing approach |
| [Refactored Python Code](https://ralemadi.github.io/MSc-Cyber-Security-e-Portfolio/advanced-oop/unit-11/Case%20Study%20Activity/code/dependency_injection.html) | Notification abstraction, Email/SMS services and constructor injection |
| [Unit Tests](https://ralemadi.github.io/MSc-Cyber-Security-e-Portfolio/advanced-oop/unit-11/Case%20Study%20Activity/tests/test_dependency_injection.html) | Mock-based tests of `UserManager` in isolation |
| [Test Results](https://ralemadi.github.io/MSc-Cyber-Security-e-Portfolio/advanced-oop/unit-11//Case%20Study%20Activity/test_results.txt) | Successful execution of the four unit tests |
| [High-Level Architecture](https://ralemadi.github.io/MSc-Cyber-Security-e-Portfolio/advanced-oop/unit-11/Case%20Study%20Activity/images/High-level%20architecture.png) | Architecture of the refactored DI/IoC design |
| [Test Results Screenshot](https://ralemadi.github.io/MSc-Cyber-Security-e-Portfolio/advanced-oop/unit-11/Case%20Study%20Activity/images/test_results.png) | Visual evidence of successful test execution |

## Case Study Activity – Dependency Injection

The original implementation creates an `EmailService` directly inside `UserManager`. This makes the class depend on one concrete notification mechanism and makes it harder to replace email with another service such as SMS or push notifications (Martin, R.C. (2000)).

The proposed refactoring introduces a `NotificationService` abstraction, implements that abstraction with `EmailService`, and modifies `UserManager` so that the notification dependency is passed into the constructor. This allows the same manager to work with different notification implementations without changing its internal registration logic (Gamma, E. et al. (1995)).

## High-Level Architecture Design

The following high-level architecture design illustrates how dependency creation is separated from business logic in the refactored solution. The `UserManager` depends on the `NotificationService` abstraction, while concrete services such as `EmailService` and `SMSService` are created externally and injected as required. During unit testing, a mock based on the `NotificationService` abstraction can be injected instead of a real notification service. This structure demonstrates Dependency Injection and Inversion of Control by reducing coupling and improving testability (Fowler, M. (2004)).

![High-Level Architecture Design](Case%20Study%20Activity/images/high-level_architecture.png)

**Figure 1.** High-level architecture of the notification system using Dependency Injection and Inversion of Control.

## Testability

One of the main benefits of the refactoring is improved testability. Instead of using the real email service during a unit test, a mock notification service can be injected into `UserManager`. The test can then verify that the welcome notification was requested without actually sending an email (Fowler, M. (2004) ; Freeman, S. and Pryce, N. (2010)).

This keeps the unit test focused on `UserManager` and demonstrates how Dependency Injection supports testing components in isolation.

The final suite contains four tests covering:

- successful welcome-notification behaviour,
- whitespace normalisation,
- empty-user rejection,
- non-string input rejection.

![Unit 11 Test Results](Case%20Study%20Activity/images/test_results.png)

**Figure 2.** Unit-test execution showing all four tests passing successfully.

## Further Improvements

The case study also identifies possible extensions such as adding an `SMSService`, using a DI container to automate dependency wiring, and testing the real `EmailService` separately through integration testing (Fowler, M. (2004) ; Freeman, S. and Pryce, N. (2010)).

## Reflection

This unit helped me understand that coupling is not only about whether classes can communicate, but also about who controls the creation of their dependencies. When `UserManager` creates `EmailService` internally, changing or testing that dependency becomes more difficult (Fowler, M. (2004)).

Injecting the dependency makes the relationship explicit and allows different notification services to be supplied without changing the main user-management logic. I also recognised the connection between DI and earlier topics such as SOLID principles, software architecture and unit testing, because reducing direct dependencies can improve both extensibility and test isolation (Martin, R.C. (2000)).

## Professional Skills Development and Action Plan

In future development work, I intend to identify classes that create or tightly control their own external dependencies and consider whether those dependencies should instead be provided through constructor injection or another suitable DI approach. I will also use mocks where appropriate to keep unit tests focused and independent from external services  (Fowler, M. (2004) ; Freeman, S. and Pryce, N. (2010)).

## Repository Structure

```text
Unit-11/
│   README.md
│   unit-11.html
│
└── Case Study Activity/
    │   README.md
    │   test_results.txt
    │
    ├── code/
    │   └── dependency_injection.html
    │
    ├── images/
    │   ├── high-level_architecture.png
    │   └── test_results.png
    │
    └── tests/
        └── test_dependency_injection.html
```

## References

- Fowler, M. (2004) ‘Inversion of Control Containers and the Dependency Injection pattern’. Available at: https://martinfowler.com/articles/injection.html
- Martin, R.C. (2000) ‘Design Principles and Design Patterns’. Object Mentor.
- Freeman, S. and Pryce, N. (2010) *Growing Object-Oriented Software, Guided by Tests*. Addison-Wesley.
- Gamma, E., Helm, R., Johnson, R. and Vlissides, J. (1995) *Design Patterns: Elements of Reusable Object-Oriented Software*. Addison-Wesley.
