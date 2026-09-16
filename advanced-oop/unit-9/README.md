# Unit 9 – Object-Oriented Software Architecture

**Programme:** MSc Cyber Security  
**Module:** Advanced Object-Oriented Design and Programming  
**Unit:** 9 – Object-Oriented Software Architecture

## Unit Overview

Unit 9 focuses on software architecture and the role of object-oriented design in creating scalable, maintainable and secure systems. It covers key architectural styles, including layered architecture, microservices and monolithic applications, together with their main strengths, limitations and areas of use.

The unit also introduces the use of object-oriented principles within software architecture and applies these concepts through the ShopEase case study. The practical activity uses layered architecture to separate presentation, business logic and data access responsibilities, while addressing modularity, security, scalability and extensibility.

## Learning Outcomes

By the end of this unit, I was able to:

- Understand and explain key software architecture styles, including layered architecture, microservices and monolithic applications.
- Recognise the role of object-oriented design in creating scalable, maintainable and secure architectures.
- Analyse a secure software architecture for a large-scale system.
- Apply architectural principles to design a simple object-oriented software architecture.

## Main Artefact

The ShopEase case study required the design of a layered object-oriented architecture for an e-commerce system. The Presentation Layer handles user interaction, the Business Logic Layer manages functions such as authentication, product catalogue and order processing, while the Data Access Layer is responsible for storing and retrieving system data.

The system was divided into separate User Management, Product Catalogue and Order Processing modules. This modular structure separates major responsibilities and supports maintainability and extensibility by reducing direct dependencies between different parts of the system.

### Scalability and Extensibility

The ShopEase design uses Dependency Injection to reduce coupling between the business logic and data access components. DataRepository is supplied to UserService, ProductCatalogService and OrderService from outside the classes rather than being created internally. This makes the data-access implementation easier to replace or extend without changing the main business logic.

Extensibility is also supported through the Strategy and Observer Patterns. Different payment methods implement the same PaymentStrategy interface, while OrderService notifies registered observers without depending on a specific notification method. This allows new payment or notification behaviours to be added with limited changes to existing code.

### Security

Security is a required quality of the ShopEase design, and the case study specifically identifies authentication as an important requirement. In the proposed architecture, authentication is handled within the Business Logic Layer through UserService.

In my implementation, I extended this requirement by protecting user passwords rather than storing them in plaintext. I used Python’s hashlib.pbkdf2_hmac() with SHA-256, together with a randomly generated salt, to derive the password hash. I also used hmac.compare_digest() for secure password verification, added input validation during registration, and required successful authentication before checkout can proceed.

It is worth noting that the implementation is intended to demonstrate how security controls can be incorporated into the architecture, rather than represent a complete production authentication or payment system.

## Evidence

| File | Purpose |
|---|---|
| [unit-9.html](https://ralemadi.github.io/MSc-Cyber-Security-e-Portfolio/advanced-oop/unit-9/unit-9.html) | Unit 9 e-Portfolio HTML page |
| [Case Study Activity ](https://github.com/Ralemadi/MSc-Cyber-Security-e-Portfolio/tree/main/advanced-oop/unit-9/Case%20Study%20Activity/) | Case Study Activity README |
| [ShopEase Architecture](https://ralemadi.github.io/MSc-Cyber-Security-e-Portfolio/advanced-oop/unit-9/Case%20Study%20Activity/code/ShopEase_Architecture.html) | Case Study Activity ShopEase_Architecture |
| [ShopEase User Activity](https://ralemadi.github.io/MSc-Cyber-Security-e-Portfolio/advanced-oop/unit-9/Case%20Study%20Activity/code/User_Activity.html) | Case Study Activity ShopEase User_Activity |

### Implementation Output

The ShopEase prototype was executed to demonstrate the interaction between the main architectural components. The output shows successful user registration, product listing, payment processing, order completion and Email/SMS notifications.

![User Activity Output](images/User%20Activity%20Output.png)


## Reflection

This unit shifted my focus from designing individual classes to considering the structure of an entire software system. I learned that software architecture defines boundaries between major responsibilities, and that these boundaries affect how easily a system can be maintained, extended and secured. This is consistent with Bass, Clements and Kazman (2021), who explain that architectural decisions influence key system quality attributes and the system’s ability to accommodate change.

The ShopEase activity helped me see how object-oriented concepts can support architecture in practice. Using separate services, Dependency Injection, polymorphic payment strategies and notification observers showed how components can remain loosely coupled while still working together as one system.

I also recognised that architectural decisions should be proportionate to the needs of the system. The aim is not to introduce layers, patterns or abstractions simply because they are available, but to use them where they improve scalability, maintainability, security or extensibility.

## Professional Skills Development and Action Plan

This unit marked a more advanced stage in my development because I applied earlier principles and design patterns based on the needs of the system rather than using them automatically. Bringing these areas together increased my confidence that I had built a strong foundation for progressing to system-level software design.

As part of my wider reading, I explored whether architectural styles need to be used independently or can be combined within the same system. Chow (2024) discusses combining different architectural styles to create solutions suited to specific requirements. This helped me understand that a hybrid architecture may be appropriate for complex systems where different components have different architectural needs, provided that the additional design and integration complexity is justified. In future work, I would like to experiment with designing a hybrid architecture and evaluate when combining architectural styles provides more value than using a single approach.

## References

- Bass, L., Clements, P. and Kazman, R. (2021) *Software Architecture in Practice*. 4th edn. Boston, MA: Addison-Wesley Professional.
- Chow, J. (2024) *Software Architecture with Kotlin: Combine Various Architectural Styles to Create Sustainable and Scalable Software Solutions*. 1st edn. Birmingham: Packt Publishing Limited.
