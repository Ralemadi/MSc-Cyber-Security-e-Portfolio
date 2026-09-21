# Advanced Object-Oriented Design and Programming

**Programme:** MSc Cyber Security  
**Module:** Advanced Object-Oriented Design and Programming  

## Module Overview

This repository documents my work across the **Advanced Object-Oriented Design and Programming** module. The module progresses from the foundations of Object-Oriented Programming (OOP) into software design principles, design patterns, concurrency, secure coding, refactoring, software architecture, Test-Driven Development (TDD), Dependency Injection (DI) and Inversion of Control (IoC).

The work currently covers:

- **Unit 1:** Introduction and Recap of Object-Oriented Programming
- **Unit 2:** SOLID Principles of Object-Oriented Design
- **Unit 3:** Design Patterns I – Creational Patterns
- **Unit 4:** Design Patterns II – Structural Patterns
- **Unit 5:** Design Patterns III – Behavioural Patterns
- **Unit 6:** Concurrency and Parallelism in Object-Oriented Design
- **Unit 7:** Secure Coding Practices in Object-Oriented Programming
- **Unit 8:** Refactoring and Code Smells
- **Unit 9:** Object-Oriented Software Architecture
- **Unit 10:** Test-Driven Development (TDD) and Behaviour Driven Development (BDD)
- **Unit 11:** Dependency Injection and Inversion of Control (IoC)

Each unit includes an e-Portfolio page together with practical exercises, code, evidence, reflections and supporting references where applicable.

## Module Links

| Resource | Link |
|---|---|
| **Module e-Portfolio Overview** | [Open e-Portfolio](https://ralemadi.github.io/MSc-Cyber-Security-e-Portfolio/advanced-oop.html) |
| **Module Repository** | [Browse Repository](./) |

---

# Units

The table below provides direct access to each unit's e-Portfolio page and repository folder.

| Unit | Topic | e-Portfolio | Repository |
|---|---|---|---|
| **Unit 1** | Introduction and Recap of Object-Oriented Programming | [View e-Portfolio](https://ralemadi.github.io/MSc-Cyber-Security-e-Portfolio/advanced-oop/unit-1/unit-1.html) | [Browse Unit 1](unit-1/) |
| **Unit 2** | SOLID Principles of Object-Oriented Design | [View e-Portfolio](https://ralemadi.github.io/MSc-Cyber-Security-e-Portfolio/advanced-oop/unit-2/unit-2.html) | [Browse Unit 2](unit-2/) |
| **Unit 3** | Design Patterns I – Creational Patterns | [View e-Portfolio](https://ralemadi.github.io/MSc-Cyber-Security-e-Portfolio/advanced-oop/unit-3/unit-3.html) | [Browse Unit 3](unit-3/) |
| **Unit 4** | Design Patterns II – Structural Patterns | [View e-Portfolio](https://ralemadi.github.io/MSc-Cyber-Security-e-Portfolio/advanced-oop/unit-4/unit-4.html) | [Browse Unit 4](unit-4/) |
| **Unit 5** | Design Patterns III – Behavioural Patterns | [View e-Portfolio](https://ralemadi.github.io/MSc-Cyber-Security-e-Portfolio/advanced-oop/unit-5/unit-5.html) | [Browse Unit 5](unit-5/) |
| **Unit 6** | Concurrency and Parallelism in Object-Oriented Design | [View e-Portfolio](https://ralemadi.github.io/MSc-Cyber-Security-e-Portfolio/advanced-oop/unit-6/unit-6.html) | [Browse Unit 6](unit-6/) |
| **Unit 7** | Secure Coding Practices in Object-Oriented Programming | [View e-Portfolio](https://ralemadi.github.io/MSc-Cyber-Security-e-Portfolio/advanced-oop/unit-7/unit-7.html) | [Browse Unit 7](unit-7/) |
| **Unit 8** | Refactoring and Code Smells | [View e-Portfolio](https://ralemadi.github.io/MSc-Cyber-Security-e-Portfolio/advanced-oop/unit-8/unit-8.html) | [Browse Unit 8](unit-8/) |
| **Unit 9** | Object-Oriented Software Architecture | [View e-Portfolio](https://ralemadi.github.io/MSc-Cyber-Security-e-Portfolio/advanced-oop/unit-9/unit-9.html) | [Browse Unit 9](unit-9/) |
| **Unit 10** | Test-Driven Development (TDD) and Behaviour Driven Development (BDD) | [View e-Portfolio](https://ralemadi.github.io/MSc-Cyber-Security-e-Portfolio/advanced-oop/unit-10/unit-10.html) | [Browse Unit 10](unit-10/) |
| **Unit 11** | Dependency Injection and Inversion of Control (IoC) | [View e-Portfolio](https://ralemadi.github.io/MSc-Cyber-Security-e-Portfolio/advanced-oop/unit-11/unit-11.html) | [Browse Unit 11](unit-11/) |

---

# Learning Outcomes and Evidence

The e-Portfolio demonstrates how the practical work completed across the module supports the module learning outcomes.

| Module Learning Outcome | Current Evidence | Progress |
|---|---|---|
| **Understand and implement secure coding practices in software development** | Unit 7 applies secure authentication controls including password hashing, validation, duplicate-user protection and account lockout. Unit 10 extends this through secure credential handling, PBKDF2-HMAC-SHA256, random salts and security-focused unit tests. | **Evidenced** |
| **Apply advanced object-oriented principles to solve complex software problems** | Units 1 and 2 establish OOP and SOLID foundations. Unit 6 applies encapsulation and thread-safe object design, Units 9 and 10 apply modular services, layered architecture and testable object-oriented components, and Unit 11 applies Dependency Injection and Inversion of Control to reduce coupling between components. | **Evidenced** |
| **Utilise design patterns to create reusable, maintainable and flexible code** | Unit 3 applies Factory Method, Unit 4 applies structural patterns, Unit 5 applies Strategy, Unit 8 compares named constants with Strategy, and Unit 9 applies Strategy and Observer within the ShopEase architecture. | **Evidenced** |
| **Design software architectures suitable for large-scale systems, ensuring security and robustness** | Unit 9 designs a layered ShopEase architecture using Dependency Injection, Strategy and Observer patterns with security controls. Unit 10 applies layered architecture to an e-learning platform and links modularity, security, scalability and testability. Unit 11 further demonstrates loose coupling, constructor injection, abstraction-based design and isolated unit testing. Unit 6 also demonstrates robustness through thread-safe shared-state management and deadlock prevention. | **Evidenced** |
| **Develop software solutions that are adaptable for AI models and efficient for data science tasks** | AI-oriented architectural concepts and related artefacts have not yet been developed in the completed evidence covered here. | **To be added** |

---

# Module Reflection

Across Units 1–11, my understanding progressed from individual object-oriented concepts to broader decisions involving concurrency, secure implementation, maintainability, software architecture, automated testing and dependency management.

**Unit 1** established the foundation by revisiting inheritance, polymorphism, abstraction and encapsulation.  

**Unit 2** moved from individual programming concepts to design quality through SOLID principles.  

**Unit 3** introduced creational patterns and demonstrated how object creation can be separated from application logic.  

**Unit 4** shifted the focus to structural relationships between objects and classes.  

**Unit 5** explored how responsibilities and behaviour can be distributed between interacting objects.

**Unit 6** introduced concurrency and parallelism. Building a thread-safe banking system showed me that software correctness must also hold when multiple execution paths interact with shared state. The work with locking, consistent lock ordering and repeatable concurrency tests strengthened my understanding of race-condition and deadlock prevention.

**Unit 7** moved the focus directly into secure coding. Refactoring the authentication system helped me connect password storage, input validation, repeated authentication attempts and application-logic issues with recognised CWE and OWASP guidance. The collaborative discussion also reinforced the value of peer review when evaluating security-sensitive code.

**Unit 8** developed my understanding of code smells and proportionate refactoring. Comparing named constants with the Strategy Pattern showed that a design pattern should be introduced because it solves a real maintenance problem, not simply because it is available. The peer discussion also helped me evaluate abstraction based on present value and expected change.

**Unit 9** shifted my thinking from individual classes to system-level architecture. The ShopEase case study used layered architecture, Dependency Injection, Strategy and Observer patterns to separate responsibilities while considering maintainability, scalability, security and extensibility.

**Unit 10** connected software design with testing through the Red–Green–Refactor cycle. Implementing and testing a secure User Management service showed how unit tests can define expected behaviour, validate failure conditions and provide a safety net when internal code is refactored.

**Unit 11** developed my understanding of Dependency Injection and Inversion of Control. Refactoring `UserManager` so that notification services are supplied from outside the class showed how constructor injection can reduce coupling and make dependencies explicit. Using a `NotificationService` abstraction, alternative implementations and mock-based unit tests also demonstrated how DI improves extensibility and test isolation.

A recurring theme across the module has been the importance of designing software that is not only functional but also **maintainable, extensible, secure, testable and understandable**.

The practical exercises also helped me relate object-oriented design to cybersecurity. Thread-safe shared state, secure authentication, input validation, password protection, controlled application logic, secure architectural boundaries and security-focused tests all demonstrated how software-design decisions can directly affect system security and robustness.

Another important lesson has been that abstraction, SOLID principles, design patterns, architectural layers and testing techniques should be applied proportionately. Additional classes, interfaces or architectural components create value when they solve a clear design problem, reduce coupling, support expected change or improve testability.

Going forward, I intend to continue applying these principles when developing security tools, automation scripts, monitoring components and larger software systems where maintainability, secure behaviour and controlled change are important.

---

# Skills Development

The module has supported the development of both academic and employability skills alongside the technical learning.

### Academic Skills

- **Critical thinking and analysis:** Comparing alternative refactoring and architectural approaches, evaluating when abstraction provides genuine value, and critically reviewing whether a stated vulnerability actually applies to the supplied code.
- **Problem-solving:** Refactoring insecure or tightly coupled code, protecting shared state in concurrent software, preventing deadlock, improving maintainability, applying Dependency Injection and designing testable object-oriented services.
- **Research and self-study:** Using academic and professional sources such as MITRE CWE, OWASP, software architecture literature and refactoring guidance to support technical decisions and reflections.
- **Testing and validation:** Designing repeatable concurrency tests, applying unit testing to public methods and failure conditions, using the Red–Green–Refactor cycle, and using mocks to isolate components from external dependencies.
- **Secure design awareness:** Considering credential protection, authentication controls, validation, application-logic abuse cases, architectural boundaries and regression risk as part of software design.

### Employability Skills

- **Communication:** Explaining technical design decisions through e-Portfolio writing, architecture descriptions and collaborative discussions.
- **Collaboration:** Engaging with peer feedback and using alternative perspectives to refine decisions about secure coding and refactoring.
- **Independent working:** Completing practical implementations, research, testing and supporting evidence independently.
- **Resilience and adaptability:** Revising implementations and explanations as my understanding of the design problem developed.
- **System-level thinking:** Moving from individual classes and methods toward concurrency, modular architecture, explicit dependency management, inversion of control and testable system design.

---

# Professional Development Plan

The Professional Development Plan will continue to develop as I apply the module concepts to larger and more complex software.

| Area | Current Position | Development Action |
|---|---|---|
| **Strength – Object-Oriented Design** | I can apply OOP, SOLID principles and design patterns to practical problems and increasingly relate class-level design to system-level architecture. | Continue applying these principles to larger applications where several modules, services and dependencies interact. |
| **Strength – Security Perspective** | Unit 7 and Unit 10 strengthened my ability to integrate password protection, validation, authentication controls and security-focused testing into application design. | Continue applying secure coding principles from the design stage and review application-logic abuse cases as well as conventional vulnerabilities. |
| **Strength – Concurrency and Robustness** | Unit 6 developed my understanding of shared state, critical sections, race conditions, locking and deadlock prevention. | Apply thread-safety considerations to future tools that use workers, shared queues, caches or other shared resources. |
| **Developing – Pattern and Refactoring Selection** | Unit 8 improved my ability to decide between a simple refactoring and a more structured design pattern based on expected change and present design value. | Continue comparing alternatives and document why additional abstraction is justified before introducing it. |
| **Developing – Software Architecture** | Unit 9 and Unit 10 provided practical experience with layered architecture, modular services, Dependency Injection and architecture-quality considerations. | Experiment with larger and hybrid architectures and evaluate their scalability, maintainability, security and integration trade-offs. |
| **Developing – Dependency Management** | Unit 11 provided practical experience with constructor injection, abstractions, alternative implementations and mock-based isolation. | Apply DI in larger systems and explore when a DI container is justified compared with explicit composition. |
| **Developing – Testing Practice** | Unit 6 introduced repeatable concurrency testing, Unit 10 applied TDD with nine unit tests and the Red–Green–Refactor cycle, and Unit 11 used mock-based testing to isolate `UserManager` from real notification services. | Extend this experience with more dependency isolation, integration testing and broader regression testing while retaining engineering judgement. |
| **Future Goal – AI-Aware Architecture** | AI-oriented OO architecture has not yet been explored in depth in the completed evidence. | Develop understanding of abstraction around AI services, model/API replacement, testability and maintainable integration of AI components. |
| **Future Goal – Ethical Software Engineering** | Security and robustness have been considered throughout the module, while AI-specific ethical considerations remain future work. | Consider explainability, auditability, bias propagation, testability and avoidance of unnecessary black-box coupling in future AI-related work. |

The final Professional Development Plan will link these actions to further reading, applied projects and relevant professional development opportunities.

---

# Practical Work Summary

| Unit | Main Topic | Main Practical Work |
|---|---|---|
| **Unit 1** | OOP Fundamentals | Inheritance, polymorphism, encapsulation, abstraction, constructors/destructors |
| **Unit 2** | SOLID Principles | Refactoring an online shopping system |
| **Unit 3** | Creational Patterns | Factory Method car manufacturing system |
| **Unit 4** | Structural Patterns | Adapter, Bridge, Composite and Decorator examples |
| **Unit 5** | Behavioural Patterns | Strategy Pattern payment processor |
| **Unit 6** | Concurrency and Parallelism | Thread-safe banking system, concurrent transaction simulation, locking and deadlock prevention |
| **Unit 7** | Secure Coding Practices | Secure authentication refactoring, bcrypt password protection, input validation, account lockout and CWE analysis |
| **Unit 8** | Refactoring and Code Smells | Magic-number and conditional-logic analysis, named constants and Strategy Pattern comparison |
| **Unit 9** | Software Architecture | ShopEase layered architecture, Dependency Injection, Strategy/Observer patterns and secure user handling |
| **Unit 10** | TDD and Unit Testing | E-learning User Management service, layered architecture, nine unit tests and Red–Green–Refactor evidence |
| **Unit 11** | Dependency Injection and IoC | Refactored notification system using `NotificationService`, constructor injection, Email/SMS implementations and four mock-based unit tests |

---

# References

**Bass, L., Clements, P. and Kazman, R. (2021).** *Software Architecture in Practice*. 4th edn. Boston, MA: Addison-Wesley Professional.  

**Beck, K. (2002).** *Test Driven Development: By Example*. Boston, MA: Addison-Wesley.  

**Coffman, E.G., Elphick, M.J. and Shoshani, A. (1971).** ‘System Deadlocks’, *ACM Computing Surveys*, 3(2), pp. 67–78.  

**Fowler, M. (2004).** ‘Inversion of Control Containers and the Dependency Injection pattern’. Available at: https://martinfowler.com/articles/injection.html  

**Fowler, M. (2018).** *Refactoring: Improving the Design of Existing Code*. 2nd edn. Boston, MA: Addison-Wesley Professional.  

**Freeman, S. and Pryce, N. (2009).** *Growing Object-Oriented Software, Guided by Tests*. Boston, MA: Addison-Wesley.  

**Gamma, E., Helm, R., Johnson, R. and Vlissides, J. (1994).** *Design Patterns: Elements of Reusable Object-Oriented Software*. Addison-Wesley.  

**Hunt, J. (2019).** *Advanced Guide to Python 3 Programming*. Cham: Springer.  

**Martin, R.C. (2000).** ‘Design Principles and Design Patterns’. Object Mentor.  

**Martin, R.C. (2017).** *Clean Architecture: A Craftsman's Guide to Software Structure and Design*. Prentice Hall.  

**Meszaros, G. (2007).** *xUnit Test Patterns: Refactoring Test Code*. Boston, MA: Addison-Wesley.  

**MITRE (2026).** *CWE – Common Weakness Enumeration*. Available at: https://cwe.mitre.org/  

**OWASP Foundation (n.d.).** *Authentication Cheat Sheet*. Available at: https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html  

**OWASP Foundation (n.d.).** *Password Storage Cheat Sheet*. Available at: https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html  

**Refactoring.Guru (n.d.).** *Strategy*. Available at: https://refactoring.guru/design-patterns/strategy
