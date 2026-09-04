# Unit 5: Design Patterns III – Behavioural Patterns

**Module:** Advanced Object-Oriented Design and Programming  
**Programme:** MSc Cyber Security  

## Unit Page

**[Open Unit 5 e-Portfolio Page](https://ralemadi.github.io/MSc-Cyber-Security-e-Portfolio/advanced-oop/unit-5/unit-5.html)**

## Unit Summary

During this unit, I explored **behavioural design patterns** and how they define the way objects interact, communicate and share responsibilities within object-oriented software.

The unit covered:

- Strategy
- Observer
- Chain of Responsibility
- Template Method
- Command
- State

The practical work focused on the **Strategy Pattern**, using a payment-processing example to demonstrate how changing behaviour can be separated from the main application logic.

## Learning Outcomes

After completing this unit, I was able to:

- Understand the purpose of behavioural design patterns in object-oriented software.
- Recognise the six behavioural patterns and the different interaction problems they address.
- Explain how behavioural patterns can improve flexibility, communication and maintainability.
- Apply the Strategy Pattern in a practical Python refactoring exercise.
- Recognise how behavioural patterns can be applied to software and cybersecurity scenarios.

## Artefacts and Practical Exercises

The main artefact for this unit was **Collaborative Discussion 2**, which involved analysing and refactoring a simple payment-processing system using the Strategy Pattern.

The original implementation relied on an `if/elif` structure to choose between payment methods. This created tight coupling and meant that the existing `PaymentProcessor` class would need to be modified whenever a new payment option was introduced.

The refactored implementation uses:

- a common `Payment_Strategy` abstraction
- separate concrete strategy classes for each payment method
- a `PaymentProcessor` context
- `change_payment_method()` to replace the selected strategy at runtime
- shared validation inside `PaymentProcessor`

This allows payment behaviour to change without modifying the processor itself.


**[Open the Collaborative Discussion README](Collaborative%20Discussion%20Strategy%20Pattern/README.md)**

## Collaborative Discussion – Peer Feedback

Two peer responses provided useful feedback on the Strategy Pattern implementation.

Séba’s feedback confirmed that using Payment_Strategy kept PaymentProcessor independent from the individual payment methods. I also appreciated his support for keeping the shared amount validation in PaymentProcessor, since it applies to every strategy. I also liked his additional point about method-specific rules. Although my example only required validation that applies to all payment methods, his suggestion showed how the same design could be extended if individual strategies later required their own validation.

![Séba Daher replied](images/S%C3%A9ba%20Daher%20replied.png)

I appreciated that Sali specifically highlighted change_payment_method(), as I included it to show how the strategy can be changed at runtime in a practical scenario. I was also pleased that she found the shared validation in PaymentProcessor useful for her own implementation. Her feedback confirmed that these small design choices made the solution more flexible and practical.

![Sali Alawabdi replied](images/Sali%20Alawabdi%20replied.png)

## Unit 5 Reflection

This unit helped me understand that design patterns are not limited to object creation or class structure. Behavioural patterns focus on how responsibilities and actions are distributed between objects.

The Strategy exercise was particularly useful because it demonstrated how a growing conditional structure can be replaced with interchangeable behaviours through a common interface.

The exercise also reinforced my understanding of the **Open/Closed Principle** from the earlier SOLID unit. New payment behaviours could be introduced without modifying the main processor. At the same time, I recognised that design patterns can introduce additional structure and classes, so they should be applied when the expected flexibility and maintainability justify this additional complexity.

The unit also introduced the Observer Pattern in the context of cybersecurity systems. This helped demonstrate how changes in monitored state can trigger alerts or other response actions.

## Professional Skills Development and Action Plan

The work in this unit improved my ability to identify behaviour that may change and separate it from stable application logic.

It also strengthened my understanding of how object-oriented design can support software that is easier to test, extend and maintain.

In future security-related development, I intend to consider behavioural patterns when designing components such as alert handling, monitoring workflows and response actions, while selecting patterns only when they address a clear design problem.

## References

**Gamma, E. et al. (1994).** *Design Patterns: Elements of Reusable Object-Oriented Software.* Reading, MA: Addison-Wesley.

**Hurst, W., Merabti, M. and Fergus, P. (2014).** ‘Behaviour analysis techniques for supporting critical infrastructure security’, *International Journal of Critical Infrastructures*, 10(3/4), pp. 267–287. Available at: https://doi.org/10.1504/IJCIS.2014.066358

**Sarcar, V. (2022).** *Java Design Patterns: A Hands-On Experience with Real-World Examples.* 3rd edn. New York: Apress.
