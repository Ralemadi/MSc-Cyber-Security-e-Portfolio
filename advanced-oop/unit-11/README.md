# Unit 11 – Dependency Injection and Inversion of Control (IoC)

**Programme:** MSc Cyber Security  
**Module:** Advanced Object-Oriented Design and Programming  
**Unit:** 11 – Dependency Injection and Inversion of Control (IoC)

## Unit Summary

During this unit, I explored Dependency Injection (DI) and Inversion of Control (IoC) as design principles for reducing coupling between software components. The unit focused on how dependencies can be supplied to objects rather than created internally, improving flexibility, modularity, maintainability and testability. I also examined the advantages and potential challenges of DI, including the risk of unnecessary complexity, excessive dependencies and poorly structured dependencies when the approach is overused or applied incorrectly (Fowler, 2004; Laigner et al., 2022).

The unit also introduced the role of DI frameworks such as Spring and Google Guice in managing dependencies in larger software systems. The practical exercise applied the same principles in Python through a small refactoring activity.

## Learning Outcomes

By the end of this unit, I was able to:

- Explain the principles of Dependency Injection and Inversion of Control.
- Recognise how dependency management can reduce tight coupling between software components.
- Recognise how DI frameworks can support flexible, modular and testable software.
- Apply Dependency Injection in a Python application.
- Evaluate the benefits and potential challenges of applying DI and IoC in software systems.
- Reflect on how DI and IoC can improve maintainability and scalability.

## Artefacts and Practical Exercises

The main practical activity involved refactoring a simple Python application to reduce tight coupling between UserManager and EmailService. The refactored design introduced a NotificationService abstraction and constructor injection, allowing different notification services to be supplied externally rather than created inside UserManager.

Unit testing then demonstrated the testability benefit of DI by injecting a mock notification service into UserManager, allowing its registration behaviour to be tested in isolation without sending a real email (Freeman and Pryce, 2009).

| Artefact | Purpose |
|---|---|
| [Case Study Activity](Case%20Study%20Activity/) | Original coupling problem, DI refactoring and testing approach |
| [Refactored Python Code](Case%20Study%20Activity/code/dependency_injection.html) | Notification abstraction, Email/SMS services and constructor injection |
| [Unit Tests](Case%20Study%20Activity/tests/test_dependency_injection.html) | Mock-based tests of UserManager in isolation |
| [Test Results](Case%20Study%20Activity/test_results.txt) | Successful execution of the four unit tests |

## Case Study Activity – Dependency Injection

The original implementation created an EmailService directly inside UserManager. This resulted in tight coupling because UserManager depended on one concrete notification service, making it difficult to replace email with another implementation such as SMS or push notifications. It also reduced testability because the notification service could not be easily substituted during unit testing (Fowler, 2004).

The refactored solution introduced a NotificationService abstraction, implemented by both EmailService and SMSService. UserManager was then modified to receive the required notification service through constructor injection rather than creating it internally. This reduced direct coupling and allowed different notification implementations to be supplied without changing the internal registration logic (Fowler, 2004; Martin, 2000).

## High-Level Architecture Design

The following high-level architecture design illustrates how dependency creation is separated from business logic in the refactored solution. UserManager depends on the NotificationService abstraction, while concrete services such as EmailService and SMSService are created externally and injected as required. During unit testing, a mock based on the NotificationService abstraction can be injected instead of a real notification service.

This structure demonstrates Dependency Injection and Inversion of Control by reducing direct coupling and improving testability.

![High-Level Architecture Design](Case%20Study%20Activity/images/High-level%20architecture.png)

## Testability

One of the main benefits of the refactoring is improved testability. Instead of using the real EmailService during a unit test, a mock notification service is injected into UserManager. This allows the test to verify that the welcome notification was requested without actually sending an email, keeping the test focused on UserManager in isolation (Freeman and Pryce, 2009).

![Unit 11 Test Results](Case%20Study%20Activity/images/test_results.png)

**Figure 2. Unit test results confirm successful execution of all four tests.**

## Further Improvements

The case study identified several possible extensions to the refactored design. A DI container, such as the dependency-injector library, could be introduced to automate dependency creation and wiring in a larger application. Additional notification services, such as push notifications, could also be added without changing the internal logic of UserManager, provided they implement the same NotificationService abstraction. The real EmailService could also be tested separately through integration testing to verify its behaviour independently from UserManager.

## Reflection

This unit helped me understand that coupling is influenced not only by how classes communicate, but also by who controls the creation of their dependencies. Fowler (2004) explains this distinction through Dependency Injection, where dependencies are supplied externally rather than created within the dependent class. This was reflected in the case study, where UserManager became easier to modify and test after EmailService was removed as an internal dependency.

The refactoring also reinforced the relationship between DI and the Dependency Inversion Principle. Martin (2000) argues that high-level modules should depend on abstractions rather than concrete implementations, which was demonstrated by introducing the NotificationService abstraction. Freeman and Pryce (2009) further support this design from a testing perspective, as substitutable dependencies allow components to be tested in isolation using mocks.

In a real-world scenario, these benefits can improve extensibility and testability, particularly when services need to be replaced or evolved independently. However, Laigner et al. (2022) show that poorly structured or excessive dependency injection can introduce anti-patterns and increase maintenance complexity. This highlighted the importance of applying DI selectively rather than treating it as a solution for every design problem.

## Professional Skills Development and Action Plan

This unit strengthened my ability to recognise tightly coupled designs and identify when dependencies should be supplied externally rather than created inside a class. It also improved my understanding of how constructor injection, abstractions and mocks can support more modular and testable software.

In future development work, I will consider the most suitable DI approach, including constructor, setter or interface injection, depending on the design context (Taelman et al., 2022). I will also use mocks where appropriate to support isolated testing and remain aware that excessive dependency injection can introduce unnecessary complexity in larger systems.

## References

- Fowler, M. (2004) Inversion of Control Containers and the Dependency Injection pattern. Available at: https://martinfowler.com/articles/injection.html (Accessed: 18 September 2026).
- Freeman, S. and Pryce, N. (2009) Growing Object-Oriented Software, Guided by Tests. Boston, MA: Addison-Wesley Professional.
- Laigner, R. et al. (2022) ‘Cataloging dependency injection anti-patterns in software systems’, Journal of Systems and Software, 184, 111125. https://doi.org/10.1016/j.jss.2021.111125
- Martin, R.C. (2000) Design Principles and Design Patterns. Object Mentor.
- Taelman, R. et al. (2022) ‘Components.js: Semantic dependency injection’, Semantic Web, 14(1), pp. 135–153.
