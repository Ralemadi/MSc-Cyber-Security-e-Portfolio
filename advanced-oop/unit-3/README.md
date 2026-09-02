# Unit 3: Design Patterns I – Creational Patterns

**Module:** Advanced Object-Oriented Design and Programming  
**Programme:** MSc Cyber Security

## Unit Page

**[Open Unit 3 e-Portfolio Page](https://ralemadi.github.io/MSc-Cyber-Security-e-Portfolio/advanced-oop/unit-3/unit-3.html)**


## Unit Summary

During this unit, I explored **creational design patterns** and how they provide structured approaches to object creation in object-oriented software. The unit covered **Singleton, Factory Method, Builder, Prototype and Abstract Factory**, with practical application focused on the **Factory Method** pattern.

The practical activity focused on applying the Factory Method pattern through the development of a simple car manufacturing system.

## Learning Outcomes

After completing this unit, I was able to:

- Understand the purpose of design patterns in object-oriented software.
- Recognise the main creational patterns and the different object-creation problems they address.
- Understand the difference between direct object creation and using a structured creation pattern.
- Apply the Factory Method pattern in a practical Python program.
- Recognise when a design pattern may provide a more suitable solution to an object-creation problem.

## Artefacts and Practical Exercises

The practical activity involved implementing the **Factory Method pattern** through a car manufacturing system capable of creating `Sedan`, `SUV` and `Hatchback` objects.

The implementation uses:

- an abstract `Car` class
- concrete `Sedan`, `SUV` and `Hatchback` classes
- an abstract `CarFactory`
- `SedanFactory`, `SUVFactory` and `HatchbackFactory`
- a `demonstrate_factory()` function that works through the factory abstraction

The main program interacts with factory objects rather than directly creating the concrete car objects. This demonstrates how object creation can be separated from application logic.



**[Open the Practical Activity README](Practical%20Activity/README.md)**



## Unit 3 Reflection

Through implementing the Factory Method pattern and reviewing additional material, I developed a clearer understanding of why object creation should be considered as part of software design rather than simply writing code that works.

Comparing the pattern with a direct object-creation approach helped me recognise how design choices can affect the flexibility of a program as it grows. It also strengthened my understanding of the connection between design patterns and SOLID principles, particularly the **Open/Closed Principle** and **Dependency Inversion Principle**.

## Professional Skills Development and Action Plan

The practical work in this unit improved my ability to think about software design beyond simply making the code work. I became more aware that different design problems may require different patterns and that selecting an appropriate approach is an important part of object-oriented design.

The following units extend this learning into structural and behavioural design patterns and provide a broader understanding of when different patterns are most appropriate.

## References

**Microsoft (2017).** *Design Patterns – Factories.* Available at: https://learn.microsoft.com/en-us/shows/visual-studio-toolbox/design-patterns-factories (Accessed: 14 August 2026).
