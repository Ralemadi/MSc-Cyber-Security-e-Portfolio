# Unit 8 – Refactoring and Code Smells

**Programme:** MSc Cyber Security  
**Module:** Advanced Object-Oriented Design and Programming  
**Unit:** 8 – Refactoring and Code Smells

## Unit Summary

During this unit, I explored code smells and refactoring as important concepts for improving the readability, maintainability and long-term sustainability of object-oriented software. Code smells do not necessarily mean that a program is incorrect, but they can indicate design decisions that make future changes more difficult. Refactoring addresses these issues by improving the internal structure of the code while preserving its intended behaviour (Fowler, 2018).

## Learning Outcomes

After completing this unit, I was able to:

- Understand what code smells are and how they can be detected in a codebase.
- Identify maintainability and readability problems in existing code.
- Apply refactoring techniques without changing the intended behaviour of the program.
- Compare simple refactoring techniques with more scalable object-oriented approaches.
- Recognise how refactoring can reduce technical debt and improve software sustainability.

## Main Artefact

The main artefact for this unit was Collaborative Discussion 4, which involved analysing a pricing function containing two clear code smells. The first was the use of magic numbers, where the discount factors 0.9 and 0.8 were embedded directly in the calculation. The second was an expanding if/elif/else structure that selected discount behaviour according to the item type.

I compared two refactoring approaches. The first replaced the hardcoded discount values with named constants, providing a simple improvement to readability and maintainability. The second used the Strategy Pattern to place each discount behaviour behind a common interface. Bergmann (2026) discusses code smells as indicators of design issues that can reduce maintainability, while the Strategy Pattern separates varying behaviours into individual strategies behind a common interface (Refactoring.Guru, n.d.). I concluded that both approaches are valid, but the appropriate choice depends on the complexity of the system and how likely the pricing rules are to change.

I concluded that both approaches are valid, but the appropriate choice depends on the complexity of the system and how likely the pricing rules are to change.

## Collaborative Discussion – Peer Feedback

As part of the collaborative discussion, I responded to Séba Daher’s initial post. We identified the same two maintainability issues which are the use of magic numbers and the widening if/elif/else conditional. In my response, I agreed that the Strategy Pattern provides a cleaner route for future extension, but I argued that it should not automatically be introduced when only two stable discount types exist. I suggested that the decision should depend on whether the discount behaviours are realistically expected to grow or change independently. For a small and stable system, the constants-based solution may remain the clearer and simpler refactoring.

![My response to Séba Daher's post](images/my%20Response%20to%20S%C3%A9ba%20Daher%20post%20.png)

Séba then responded to my main post and agreed that the two code smells were correctly identified. He focused on the trade-off between adopting Strategy now and waiting until a third item type appears. His response argued that BookDiscount and ElectronicsDiscount are already active behaviours, so the main additional structural cost is the abstract base class and the strategy mapping. He therefore considered the remaining cost small enough for Strategy to provide value even with only two current item types. This reply helped refine my view: the decision is not only about the number of item types, but also about whether the extra abstraction provides a useful separation of behaviour in the present design.

![Séba Daher's response to my post](images/S%C3%A9ba%20Daher%20Response%20to%20my%20post%20.png)

In my follow-up response, I agreed that Strategy can therefore provide a present benefit even with only two item types because each discount rule is separated and can be tested independently. However, I maintained that the choice should still depend on how likely those behaviours are to change independently. This led me to view the number of item types as only one consideration rather than the main criterion for deciding whether Strategy is justified.

## Artefacts

| Artefact | Description |
|---|---|
| [unit-8.html](https://ralemadi.github.io/MSc-Cyber-Security-e-Portfolio/advanced-oop/unit-8/unit-8.html) | Unit 8 e-Portfolio page |
| [Collaborative Discussion ](https://github.com/Ralemadi/MSc-Cyber-Security-e-Portfolio/tree/main/advanced-oop/unit-8/Collaborative%20Discussion/) | Detailed discussion, peer feedback and evidence |
| [Collaborative Discussion PDF](https://ralemadi.github.io/MSc-Cyber-Security-e-Portfolio/advanced-oop/unit-8/Collaborative%20Discussion/Unit%208%20Collaborative%20Discussion%204%20%E2%80%93%20Refactoring%20and%20Code%20Smells.pdf) | Final written discussion |



## Reflection Summary

This unit helped me understand that code can be functionally correct while still being difficult to maintain. The pricing example demonstrated how small issues such as hardcoded values and growing conditional logic can become more significant as requirements change.

The comparison between named constants and the Strategy Pattern was particularly useful because it showed that refactoring should be proportionate to the problem. A small and stable rule set may only need a simple change, while a system with growing or frequently changing behaviours may justify a more structured object-oriented solution. This reinforced the importance of choosing patterns because they solve a real design problem rather than using them automatically.

The peer discussion also refined my judgement about abstraction. I realised that the number of existing behaviours alone is not enough to justify or reject a design pattern. The current benefit of separating those behaviours, together with how likely they are to evolve independently, should also be considered.

The work in this unit improved my ability to identify maintainability problems in existing code and select an appropriate refactoring technique. It also strengthened my understanding of the relationship between code smells, technical debt and long-term software quality.

In future development work, I intend to review hardcoded configuration values, repeated conditional logic and methods that accumulate unrelated responsibilities. I will first consider a simple refactoring and introduce additional abstractions or design patterns only when the expected change and complexity justify them. I will also use appropriate tests before and after refactoring to confirm that structural changes have not altered the intended behaviour.

## References

- Bergmann, D. (2026) *Code smells, explained*. IBM Think, 13 July. Available at: https://www.ibm.com/think/topics/code-smells
- Fowler, M. (2018) *Refactoring: Improving the Design of Existing Code*. 2nd edn. Boston, MA: Addison-Wesley Professional.
- Refactoring.Guru (n.d.) *Strategy*. Available at: https://refactoring.guru/design-patterns/strategy (Accessed: 7 September 2026).
