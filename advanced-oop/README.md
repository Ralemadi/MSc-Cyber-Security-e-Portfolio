# Advanced Object-Oriented Design and Programming

**Programme:** MSc Cyber Security  
**Module:** Advanced Object-Oriented Design and Programming  

## Module Overview

This repository documents my work across the **Advanced Object-Oriented Design and Programming** module. The module progresses from the foundations of Object-Oriented Programming (OOP) into software design principles, design patterns, concurrency, secure coding, refactoring, software architecture, Test-Driven Development (TDD), Dependency Injection (DI) and Inversion of Control (IoC).

The module concludes with the **BankSecure Capstone Project**, which brings these areas together in a secure object-oriented banking application. The project applies design patterns, concurrency controls, persistent storage, role-based access control, automated testing, Dependency Injection and AI ready service abstractions within one integrated system.

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
| **Unit 12 – Capstone Project** | [Open Capstone Project](https://github.com/Ralemadi/MSc-Cyber-Security-e-Portfolio/tree/main/advanced-oop/unit-12/Capstone%20Project) |

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

The module learning outcomes were developed progressively across Units 1–11 and consolidated through the final BankSecure Capstone Project.

| **Module Learning Outcome** | **Evidence Across the Module** | **Capstone Evidence** |
|---|---|---|
| **Understand and implement secure coding practices in software development** | Unit 7 applies secure authentication controls including password hashing, validation, duplicate-user protection and account lockout. Unit 10 extends this through secure credential handling, PBKDF2-HMAC-SHA256, random salts and security focused unit tests. | BankSecure extends this through RBAC, privilege and resource scope checks, temporary login lockout, administrative disablement, controlled failure handling and security-focused negative testing. |
| **Apply advanced object-oriented principles to solve complex software problems** | Units 1 and 2 establish OOP and SOLID foundations. Unit 6 applies encapsulation and thread-safe object design, Units 9 and 10 apply modular services, layered architecture and testable object-oriented components, and Unit 11 applies Dependency Injection and Inversion of Control to reduce coupling between components. | BankSecure brings these principles together through domain models, service abstractions, Repository interfaces, Dependency Injection, an explicit Composition Root and thread-safe transfer processing. |
| **Utilise design patterns to create reusable, maintainable and flexible code** | Unit 3 applies Factory Method, Unit 4 applies structural patterns, Unit 5 applies Strategy, Unit 8 compares named constants with Strategy, and Unit 9 applies Strategy and Observer within the ShopEase architecture. | BankSecure applies Strategy, Abstract Factory, Decorator and Visitor, with each pattern used to address a specific design problem rather than simply increasing pattern use. |
| **Design software architectures suitable for large-scale systems, ensuring security and robustness** | Unit 9 designs a layered ShopEase architecture using Dependency Injection, Strategy and Observer patterns with security controls. Unit 10 applies layered architecture to an e-learning platform and links modularity, security, scalability and testability. Unit 11 further demonstrates loose coupling, constructor injection, abstraction based design and isolated unit testing. Unit 6 also demonstrates robustness through thread-safe shared state management and deadlock prevention. | BankSecure applies layered services, SQLite persistence, explicit transaction handling, rollback, deterministic account-lock ordering, RBAC and automated integration, concurrency, stress and scalability testing. |
| **Develop software solutions that are adaptable for AI models and efficient for data science tasks** | Units 9 and 11 establish relevant architectural foundations through modular services, abstractions, Dependency Injection and replaceable dependencies. The module also introduced conceptual awareness of AI-oriented architectural patterns including Model Registry for model lifecycle and version management (MLflow, no date), and Feature Store for reusable and consistent feature management (Feast, no date). | BankSecure introduces AI-ready fraud and risk-service abstractions, replaceable provider families and deterministic simulated AI behaviour, allowing AI-dependent components to be tested without requiring a live model or external API. |

---
# Module Practical Artefacts and Supporting Evidence

The table below summarises representative practical artefacts from Units 1–11 and provides direct access to the supporting README documentation and complete practical evidence.

| **Unit** | **Practical Artefact** | **Supporting Evidence** |
|---|---|---|
| **1** | Five OOP exercises | [Exercise README](https://github.com/Ralemadi/MSc-Cyber-Security-e-Portfolio/blob/main/advanced-oop/unit-1/Programming%20Exercise/README.md) |
| **2** | SOLID shopping refactoring | [Exercise README](https://github.com/Ralemadi/MSc-Cyber-Security-e-Portfolio/blob/main/advanced-oop/unit-2/Programming%20Exercises/README.md) |
| **3** | Factory Method | [Activity README](https://github.com/Ralemadi/MSc-Cyber-Security-e-Portfolio/blob/main/advanced-oop/unit-3/Practical%20Activity/README.md) |
| **4** | Structural patterns, including the Coffee Decorator seminar exercise | [Discussion README](https://github.com/Ralemadi/MSc-Cyber-Security-e-Portfolio/blob/main/advanced-oop/unit-4/Collaborative%20Discussion%20Structural%20Design%20Patterns/README.md) · [Coffee Decorator Seminar Exercise](https://github.com/Ralemadi/MSc-Cyber-Security-e-Portfolio/blob/main/advanced-oop/unit-4/Seminar%20Practical%20Activity%20Decorator%20Pattern/README.md) |
| **5** | Payment Strategy | [Discussion README](https://github.com/Ralemadi/MSc-Cyber-Security-e-Portfolio/blob/main/advanced-oop/unit-5/Collaborative%20Discussion%20Strategy%20Pattern/README.md) |
| **6** | Thread-safe banking | [Exercise README](https://github.com/Ralemadi/MSc-Cyber-Security-e-Portfolio/blob/main/advanced-oop/unit-6/Individual%20Coding%20Exercise/README.md) |
| **7** | Secure authentication | [Discussion README](https://github.com/Ralemadi/MSc-Cyber-Security-e-Portfolio/blob/main/advanced-oop/unit-7/Collaborative%20Discussion/README.md) |
| **8** | Discount refactoring | [Discussion README](https://github.com/Ralemadi/MSc-Cyber-Security-e-Portfolio/blob/main/advanced-oop/unit-8/Collaborative%20Discussion/README.md) |
| **9** | ShopEase architecture | [Case Study README](https://github.com/Ralemadi/MSc-Cyber-Security-e-Portfolio/blob/main/advanced-oop/unit-9/Case%20Study%20Activity/README.md) |
| **10** | User Management and TDD | [Case Study README](https://github.com/Ralemadi/MSc-Cyber-Security-e-Portfolio/blob/main/advanced-oop/unit-10/Case%20Study%20Activity/README.md) |
| **11** | Dependency Injection and mocking | [Case Study README](https://github.com/Ralemadi/MSc-Cyber-Security-e-Portfolio/blob/main/advanced-oop/unit-11/Case%20Study%20Activity/README.md) |
---

# Module Reflection

Across the module, my understanding of object-oriented programming developed from focusing mainly on whether code worked to considering whether a solution was maintainable, secure, testable and appropriate for future change.

Concurrency was one of the areas that changed my approach most. The thread-safe banking work showed that software can appear correct during normal execution while still fail under concurrent access. Working with shared state, lock ordering and deadlock prevention strengthened my understanding of robustness beyond simple functional correctness.

Secure coding also became more closely connected to software design. Authentication, password protection, validation, access control and failure handling showed me that security should be considered throughout implementation rather than added only at the end. This was later reinforced in BankSecure through RBAC, temporary login lockout, resource-level authorisation and negative-path testing.

My understanding of design patterns also became more selective. Earlier in the module, patterns mainly appeared to be reusable design solutions. Through the practical work and Capstone, I learned that their value depends on whether they solve a real design problem. Strategy, Abstract Factory, Decorator and Visitor were useful in BankSecure because they supported variation, separation of concerns and testability, while simpler concerns were kept as straightforward services or policies.

Testing became part of the design process rather than only a final verification step. TDD, mocking, integration testing, concurrency testing and stress testing helped me evaluate both expected behaviour and failure conditions. Dependency Injection and repository abstractions also showed how reducing coupling can make components easier to replace and test.

The BankSecure Capstone brought these areas together within one system. It also reinforced the importance of recognising limitations. The project demonstrates AI ready service abstractions and local concurrency behaviour, but it does not claim to implement a production AI model or a distributed production banking architecture. 

Overall, the module strengthened my ability to justify design choices based on the problem being solved and the evidence available from testing and implementation.

---

# Skills Development

The module supported the development of both academic and employability skills alongside the technical learning.

### Academic Skills

- **Critical thinking and problem-solving:** I moved from asking whether code simply works to evaluating whether a solution is maintainable, testable, secure and proportionate. Practical work with design patterns, concurrency and BankSecure strengthened my ability to compare alternatives and justify design decisions.
- **Research and independent learning:** When concepts were unclear, I learned to break them into smaller questions, consult academic sources and technical documentation, test examples and then apply the learning to the wider project.
- **Testing and engineering judgement:** My approach to testing developed from checking successful output to using tests as evidence of behaviour. TDD, mocking, integration, concurrency, stress and scalability testing helped me understand the strengths and limitations of different validation approaches.
- **Secure design awareness:** Authentication, password protection, validation, RBAC, resource-level authorisation and failure-path testing strengthened my understanding of security as part of software design rather than a final check.
- **Ethical and AI-aware design:** I developed greater awareness of transparency, explainability, testability, auditability and the risks of black-box coupling when designing software that may integrate AI components.

### Employability Skills

- **Communication:** Collaborative discussions, peer feedback and technical documentation improved my ability to explain design decisions, evidence and trade-offs clearly.
- **Independent working:** The practical exercises and Capstone required me to plan, implement, test, document and review work independently across multiple technical areas.
- **Resilience and adaptability:** Repeated testing, debugging and refinement helped me work through concurrency, security, integration and design challenges rather than treating the first working solution as final.
- **Time management:** I learned to divide practical work, testing, documentation and evidence preparation into manageable stages while progressing through the module and Capstone.
- **System-level thinking:** The module developed my ability to move beyond individual classes and methods towards architecture, dependency management, concurrency, persistence, security boundaries and integrated testing.

---

# Professional Development Plan

The Professional Development Plan summarises my current strengths and development priorities, together with practical actions, target timeframes and relevant professional benchmarks.

| **Skill Set** | **Current Status** | **Strength / Gap / Action Plan** | **Target Time** | **Professional Benchmark / Reference** |
|---|---|---|---|---|
| **Object-Oriented Design and Python** | Met | **Strength:** I can apply OOP, SOLID principles and design patterns to practical problems. Continue applying advanced OOP in larger projects and evaluating when additional abstraction is justified. | Ongoing | BCS CITP |
| **Secure Software Engineering** | Met | **Strength:** The module strengthened my ability to integrate secure coding, authentication controls, access control and security-focused testing into application design. Maintain these skills through secure coding and security-focused projects. | Ongoing | IEEE CS SWEBOK V4 / BCS CITP |
| **Software Architecture** | Partially Met | **Gap:** My experience is mainly with modular and layered applications rather than larger distributed architectures. Gain experience through an applied project and further architecture study. | 6 months | IEEE CS SWEBOK V4 |
| **Advanced Testing** | Partially Met | **Gap:** I developed experience with TDD, mocking, integration, concurrency, stress and scalability testing, but need broader experience with performance, failure-injection and AI-related testing. Review an appropriate ISTQB testing pathway. | 3–6 months | IEEE CS SWEBOK V4 / BCS-ISTQB |
| **AI-Aware Software Architecture** | Partially Met | **Gap:** BankSecure introduced replaceable AI-ready service abstractions, while Model Registry and model lifecycle concepts were explored at a conceptual level. Develop a project that applies these concepts more fully and consider the BCS Foundation Certificate in AI. | 6 months | BCS AI |
| **Ethical AI and Explainability** | Partially Met | **Gap:** I developed awareness of bias, explainability, auditability and black-box coupling in AI-enabled systems, areas also addressed within AI risk-management guidance (Tabassi, 2023) | 6–12 months | BCS AI / NIST AI RMF |
| **Technical Communication** | Met | **Strength:** Collaborative discussions, technical documentation and evidence presentation improved my ability to explain design decisions clearly. Continue improving concise technical documentation and evidence presentation. | Ongoing | BCS CITP |
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
