# Unit 9 Case Study Activity – ShopEase E-Commerce Architecture

## Overview

The ShopEase case study required the design of a layered object-oriented architecture for an e-commerce system. The Presentation Layer handles user interaction, the Business Logic Layer manages functions such as authentication, product catalogue and order processing, while the Data Access Layer is responsible for storing and retrieving system data.

The system was divided into separate User Management, Product Catalogue and Order Processing modules. This modular structure separates major responsibilities and supports maintainability and extensibility by reducing direct dependencies between different parts of the system.

---

### `ShopEase_Architecture.py`

Contains the actual architecture and reusable application components:

- domain models,
- Data Access Layer,
- User Management,
- Product Catalog,
- Payment Strategy,
- notification observers,
- Order Processing, and
- Presentation Layer.


---


## 1. Presentation Layer

The Presentation Layer handles user interaction. It is implemented through `ShopEaseApp`, which manages registration, product display and checkout requests.

---

## 2. Business Logic Layer

The Business Logic Layer implements core application behaviour and business rules. It includes `UserService`, `ProductCatalogService` and `OrderService` for authentication, catalogue operations and order processing.

---

## 3. Data Access Layer

`DataRepository` represents the Data Access Layer, which manages data storage and retrieval. In the prototype, it stores and retrieves user, product and order data.

---

## Object-Oriented Principles

### Encapsulation

Each class contains a focused responsibility, such as user authentication, product management or order processing.

### Abstraction

Abstract base classes define common interfaces for:

- payment methods, and
- notification observers.

### Polymorphism

`CardPayment` and `PayPalPayment` both implement the same `pay()` operation.

The order service can therefore work with different payment methods through the same abstraction.

### Dependency Injection

The ShopEase design uses Dependency Injection to reduce coupling between the business logic and data access components. DataRepository is supplied to UserService, ProductCatalogService and OrderService from outside the classes rather than being created internally. This makes the data-access implementation easier to replace or extend without changing the main business logic.

---

## Design Patterns

### Strategy Pattern

Different payment methods implement the same `PaymentStrategy` interface. This allows new payment behaviours to be added with limited changes to existing code.


### Observer Pattern

`OrderService` notifies registered observers without depending on a specific notification method. This allows new notification behaviours to be added with limited changes to existing code.

---

## Security Considerations

Security is a required quality of the ShopEase design, and the case study specifically identifies authentication as an important requirement. In the proposed architecture, authentication is handled within the Business Logic Layer through UserService.

In my implementation, I extended this requirement by protecting user passwords rather than storing them in plaintext. I used Python’s hashlib.pbkdf2_hmac() with SHA-256, together with a randomly generated salt, to derive the password hash. I also used hmac.compare_digest() for secure password verification, added input validation during registration, and required successful authentication before checkout can proceed.

It is worth noting that the implementation is intended to demonstrate how security controls can be incorporated into the architecture, rather than represent a complete production authentication or payment system.

---

## User Activity

The ShopEase prototype was executed to demonstrate the interaction between the main architectural components. The output shows successful user registration, product listing, payment processing, order completion and Email/SMS notifications.

The screenshot below shows the execution result of the ShopEase prototype.

![User Activity Output](images/User%20Activity%20Output.png)

---

## Running the Activity

Open a terminal inside the `code` folder and run:

```bash
python User_Activity.py
```



---

## Limitations

This is an architectural demonstration rather than a production e-commerce system.

The following are outside the scope of the activity:

- a real database,
- web/mobile interfaces,
- real payment gateways,
- role-based access control,
- session management,
- asynchronous message queues,
- microservice deployment, and
- database transaction/rollback handling.

---

## References

- Bass, L., Clements, P. and Kazman, R. (2021) *Software Architecture in Practice*. 4th edn. Boston, MA: Addison-Wesley Professional.
- Chow, J. (2024) *Software Architecture with Kotlin: Combine Various Architectural Styles to Create Sustainable and Scalable Software Solutions*. 1st edn. Birmingham: Packt Publishing Limited.
