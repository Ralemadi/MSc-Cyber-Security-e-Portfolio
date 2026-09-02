# Unit 2 – Programming Exercises

## Applying SOLID Principles to a Python Shopping System

The Unit 2 programming exercise applies the **SOLID principles** to a Python shopping system.

The exercise is divided into two stages:

1. Review the initial design.
2. Refactor the system to separate responsibilities, reduce unnecessary dependencies and improve extensibility.

```text
Programming Exercises/
├── README.md
├── code/
│   ├── initial_shopping_system.py
│   └── refactored_solid_shopping_system.py
└── images/
```

---

## Stage 1 – Initial Shopping System

The initial design contains an `Item` class and an `Order` class.

`Order` is responsible for:

- storing items
- calculating the order total
- selecting and processing the payment method

Although the program works correctly, the design mixes several responsibilities inside the same class.

**Source code:** [`initial_shopping_system.py`](code/initial_shopping_system.py)

![Initial Code](images/Initial%20Code.png)

### Execution Result

The example creates an order containing:

```text
Keyboard: $25.00
Mouse:    $16.00
----------------
Total:    $41.00
```

The program then processes a credit card payment.

![Initial Code Execution Result](images/Initial%20Code%20Execution%20Result.png)

### Design Issues

The initial design demonstrates several issues:

- **SRP:** `Order` handles both order management and payment processing.
- **OCP:** adding another payment method requires modifying `Order.pay()`.
- **DIP:** the order logic directly contains payment-processing logic rather than depending on an abstraction.

These issues make the design more difficult to extend as additional payment methods or other checkout behaviour are introduced.

---

## Stage 2 – Refactored SOLID Design

The refactored design separates the original responsibilities into focused classes and abstractions.

Main components include:

- `Product`
- `Order`
- `Discount`
- `NoDiscount`
- `PercentageDiscount`
- `PaymentMethod`
- `CreditCardPayment`
- `PayPalPayment`
- `CryptoPayment`
- `CheckoutService`

`CheckoutService` coordinates the checkout process while depending on the `PaymentMethod` and `Discount` abstractions instead of specific implementations.

**Source code:** [`refactored_solid_shopping_system.py`](code/refactored_solid_shopping_system.py)

### Execution Result

The order subtotal remains:

```text
$41.00
```

A 10% discount produces:

```text
$36.90
```

The same order can then be processed using:

- Credit Card
- PayPal
- Crypto

without modifying the checkout logic.

![Refactored SOLID Design Execution Result](images/Refactored%20SOLID%20Design%20Execution%20Result.png)

---

## How the SOLID Principles Are Applied

| Principle | Application in the Refactored Design |
|---|---|
| **SRP** | `Order` manages products and totals, payment classes handle payments, and discount classes handle discounts |
| **OCP** | New payment methods or discount strategies can be added through new subclasses without modifying `Order` or `CheckoutService` |
| **LSP** | `CreditCardPayment`, `PayPalPayment` and `CryptoPayment` can all be used wherever `PaymentMethod` is expected |
| **ISP** | `PaymentMethod` contains only the `pay()` operation required by payment classes, while discount behaviour is kept separate |
| **DIP** | `CheckoutService` depends on the `PaymentMethod` and `Discount` abstractions rather than concrete implementations |

---

## How to Run the Exercises

Open a terminal in the `Programming Exercises/code` directory.

### Initial version

```bash
python initial_shopping_system.py
```

Expected output:

```text
Order total: $41.00
Processing credit card payment...
```

### Refactored version

```bash
python refactored_solid_shopping_system.py
```

Expected behaviour:

```text
Credit Card Checkout
Subtotal: $41.00
Final total: $36.90
Processing credit card payment of $36.90...

PayPal Checkout
Subtotal: $41.00
Final total: $36.90
Processing PayPal payment of $36.90...

Crypto Checkout
Subtotal: $41.00
Final total: $36.90
Processing crypto payment of $36.90...
```

---

## Summary

The exercise demonstrates how refactoring with SOLID principles can move a program from a working but tightly coupled design to a more modular structure.

The initial program produces the correct result, but adding new behaviour requires modifying existing code. The refactored version separates order management, discount calculation and payment processing, allowing the system to be extended with fewer changes to established components.
