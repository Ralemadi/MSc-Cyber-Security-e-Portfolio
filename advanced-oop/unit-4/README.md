# Unit 4: Design Patterns II – Structural Patterns

**Module:** Advanced Object-Oriented Design and Programming  
**Programme:** MSc Cyber Security

## Unit Page

**[Open Unit 4 e-Portfolio Page](https://ralemadi.github.io/MSc-Cyber-Security-e-Portfolio/advanced-oop/unit-4/unit-4.html)**

## Unit Summary

Unit 4 focuses on **structural design patterns** and how classes and objects can be organised into larger, flexible structures. The unit covers **Adapter, Bridge, Composite, Decorator, Facade, Proxy and Flyweight**.

The main practical work applies Adapter, Bridge and Composite to cybersecurity-oriented examples, while the seminar practical activity demonstrates the Decorator Pattern using a simple coffee-shop application.

## Learning Outcomes

After completing this unit, I was able to:

- Understand the purpose of structural design patterns in object-oriented software.
- Recognise the seven main structural patterns and the design problems they address.
- Explain how structural patterns can improve modularity, flexibility and maintainability.
- Apply Adapter, Bridge, Composite and Decorator through practical Python examples.
- Recognise that a pattern should be selected according to the design problem rather than applied unnecessarily.
- Recognise how good software design can improve maintainability, flexibility, scalability and reliability.



## Collaborative Discussion: Structural Design Patterns

The collaborative discussion is the main practical artefact for the unit and applies three structural patterns to cybersecurity scenarios.

### Adapter – Security Log Collector

A legacy collector returns string-based records through `read_old_logs()`, while a modern collector already exposes structured events through `get_events()`. `LogAdapter` converts the legacy records into the same dictionary structure as the modern records, allowing both sources to be processed through one interface and merged into one event list.

### Bridge – Security Alerts

The Bridge example separates alert types from delivery channels. `SecurityAlert` and `CriticalAlert` define alert behaviour, while `ConsoleChannel`, `EmailChannel` and `SMSChannel` provide independent delivery mechanisms. This avoids creating a separate alert class for every alert/channel combination.

### Composite – Network Asset Inventory

The Composite example uses `AssetComponent` as a common interface for both individual `Device` objects and `AssetGroup` containers. Groups can contain devices or other groups, allowing the complete office network to be represented and displayed as one hierarchy.

**[Open the Collaborative Discussion README](Collaborative%20Discussion%20Structural%20Design%20Patterns/README.md)**

## Peer Feedback

Two peer responses provided useful feedback on the structural-pattern examples. I appreciated Donald’s feedback because he understood why I used the Adapter Pattern for the security log example. I was already aware that a real logging system would need more details such as timestamps and severity. Still, I was glad he mentioned this because it showed that he was thinking about how the example could work beyond the simple demonstration.

<img src="images/Donald%20Herbert%20Kofi%20Appeatsi%20Duodu%20replied.png" alt="Peer feedback on Adapter" width="900">

A second peer positively highlighted the Composite example and its use for representing employee access and grouped assets.

<img src="images/Nawaz%20Khan%20replied.png" alt="Peer feedback on Composite" width="900">

## Seminar Practical Activity: Decorator Pattern

The seminar practical activity demonstrates how the **Decorator Pattern** can add functionality dynamically without modifying the original object. A `SimpleCoffee` component is wrapped by `Milk`, `Sugar` and `Whip` decorators. Each decorator adds to the existing cost and description while keeping the same `Coffee` interface.

This provides a concise example of extending behaviour through object composition rather than creating many subclasses for every possible coffee combination.

**[Open the Seminar Practical Activity README](Seminar%20Practical%20Activity%20Decorator%20Pattern/README.md)**

## Reflection

This unit extended the design-pattern work from creational patterns into structural design. The cybersecurity examples made it easier to distinguish between different structural problems: Adapter addresses incompatible interfaces, Bridge separates dimensions that should vary independently, and Composite supports hierarchical object structures.

The work also reinforced that patterns introduce additional structure and should therefore be justified by a clear design problem. The collaborative discussion and peer feedback provided additional perspectives on how these designs might evolve in more realistic systems.

## Professional Skills Development and Action Plan

The practical work developed my ability to identify structural design problems and select patterns that suit different system requirements. These ideas are relevant to cybersecurity environments where integration with legacy systems, multiple communication mechanisms and hierarchical infrastructure are common.

## References

**Gamma, E., Helm, R., Johnson, R. and Vlissides, J. (1994).** *Design Patterns: Elements of Reusable Object-Oriented Software.* Reading, MA: Addison-Wesley.

**Sarcar, V. (2022).** *Java Design Patterns: A Hands-On Experience with Real-World Examples.* 3rd edn. New York: Apress.
