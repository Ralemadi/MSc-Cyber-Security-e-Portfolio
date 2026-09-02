# Unit 3 – Practical Activity

## Implementing the Factory Method Pattern

This practical activity implements the **Factory Method pattern** in a simple car manufacturing system.

The system produces `Sedan`, `SUV` and `Hatchback` objects without directly instantiating the concrete car classes in the main program. The implementation contains an abstract product, concrete products, an abstract creator and concrete factory classes.

```text
Practical Activity/
├── README.md
├── code/
│   └── Factory_Method.html
└── images/
    ├── Abstract Car Class.png
    ├── Concrete Car Class.png
    ├── Factory Classes.png
    ├── Using the Factory.png
    ├── The main program.png
    └── Program Output.png
```

## Python Implementation

### 1. Abstract Car Class

The abstract `Car` class defines the common `drive()` behaviour that every concrete car type must implement.

![Abstract Car Class](images/Abstract%20Car%20Class.png)

---

### 2. Concrete Car Classes

`Sedan`, `SUV` and `Hatchback` inherit from `Car` and each provides its own implementation of `drive()`.

![Concrete Car Class](images/Concrete%20Car%20Class.png)

This demonstrates that all concrete car types follow the same common interface while providing their own behaviour.

---

### 3. Factory Classes

`CarFactory` defines the abstract `create_car()` factory method.

The concrete factories are:

- `SedanFactory`
- `SUVFactory`
- `HatchbackFactory`

Each factory overrides `create_car()` and returns the corresponding `Car` object.

![Factory Classes](images/Factory%20Classes.png)

---

### 4. Using the Factory

The `demonstrate_factory()` function receives a `CarFactory` object.

It does not need to know whether the supplied factory creates a `Sedan`, `SUV` or `Hatchback`. It only asks the factory to create a car and then calls the common `drive()` method.

```python
def demonstrate_factory(factory: CarFactory) -> None:
    car = factory.create_car()
    car.drive()
```

![Using the Factory](images/Using%20the%20Factory.png)

---

### 5. Main Program

The main program creates the three factory objects and passes each one to `demonstrate_factory()`.

The concrete car classes are therefore not instantiated directly by the main program.

![The main program](images/The%20main%20program.png)

---

### 6. Program Output

The program creates one car through each factory and calls its `drive()` method.

Expected output:

```text
Driving a Sedan
Driving an SUV
Driving a Hatchback
```

![Program Output](images/Program%20Output.png)

## Source Code

The complete implementation is available here:

**[Open Factory_Method.html](code/Factory_Method.html)**

## Factory Method Structure

| Role | Implementation |
|---|---|
| Abstract Product | `Car` |
| Concrete Products | `Sedan`, `SUV`, `Hatchback` |
| Abstract Creator | `CarFactory` |
| Concrete Creators | `SedanFactory`, `SUVFactory`, `HatchbackFactory` |
| Client / Demonstration | `demonstrate_factory()` and the main program |

## Program Workflow

1. `Car` defines the common `drive()` behaviour.
2. `Sedan`, `SUV` and `Hatchback` implement that behaviour.
3. `CarFactory` declares the `create_car()` factory method.
4. Each concrete factory creates one specific car type.
5. `demonstrate_factory()` requests a car through the factory abstraction.
6. The main program works through the factories instead of directly instantiating the concrete car classes.

## Summary

The practical activity demonstrates how the Factory Method pattern separates **object creation** from the code that uses the objects.

Instead of the client deciding which concrete class to instantiate, that responsibility is delegated to factory classes. This makes the object-creation process more structured and allows additional car types and factories to be introduced without changing the existing factory-client interaction.
