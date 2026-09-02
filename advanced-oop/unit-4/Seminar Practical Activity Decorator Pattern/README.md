# Seminar Practical Activity: Decorator Pattern

This practical activity demonstrates the **Decorator Pattern** through a simple coffee-shop application. The pattern adds new behaviour to an existing object dynamically without modifying the original component.

## Structure

The implementation contains:

- `Coffee` – abstract component defining `cost()` and `description()`.
- `SimpleCoffee` – concrete component providing the basic coffee behaviour.
- `CoffeeDecorator` – base decorator that stores and delegates to a wrapped `Coffee` object.
- `Milk`, `Sugar` and `Whip` – concrete decorators that extend the cost and description.

### Abstract Coffee Class

![Abstract Coffee Class](images/Abstract%20Coffee%20Class.png)

### Concrete Component

![Concrete Component - Simple Coffee](images/Concrete%20Component-Simple%20Coffee.png)

### Base Decorator

![Base Decorator - CoffeeDecorator](images/Base%20Decorator%20%E2%80%93%20CoffeeDecorator.png)

### Concrete Decorators

![Concrete Decorators](images/Concrete%20Decorators.png)

## Applying the Decorators

The program starts with `SimpleCoffee` and wraps it successively with `Milk`, `Sugar` and `Whip`. Each wrapper preserves the common `Coffee` interface while extending the existing behaviour.

![Applying the Decorators](images/Applying%20the%20Decorators.png)

The resulting coffee configurations are stored together and processed through the same `description()` and `cost()` operations.

![Storing and Displaying the Coffee Objects](images/Storing%20and%20Displaying%20the%20Coffee%20Objects.png)

## Program Output

The output demonstrates the accumulated description and cost as decorators are added.

![Program Output](images/Program%20Output.png)

## Source Code and Full Document

**[Open decorator.html](code/decorator.html)**  
**[Open Seminar Practical Activity Decorator Pattern.pdf](Seminar%20Practical%20Activity%20Decorator%20Pattern.pdf)**

## Summary

The Decorator Pattern provides a flexible alternative to creating a large number of subclasses for every possible combination of features. Behaviour is extended by wrapping an existing component, allowing decorators to be combined dynamically while retaining the same interface.
