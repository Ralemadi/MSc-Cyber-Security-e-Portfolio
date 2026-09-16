# Collaborative Discussion 4 – Refactoring and Code Smells

## Activity Overview

This collaborative discussion examined the supplied `calculate_total_price()` function and required the identification of code smells, comparison of refactoring options and discussion with peers.

I identified two main maintainability problems:

- **Magic Numbers:** `0.9` and `0.8` were embedded directly in the pricing calculation.
- **Expanding Conditional Logic:** the `if/elif/else` structure selected discount behaviour and would grow as new item types were added.

## Refactoring Approach 1 – Named Constants

For a small and stable system, I considered named constants to be the simplest improvement:

```python
BOOK_DISCOUNT = 0.9
ELECTRONICS_DISCOUNT = 0.8
```

This removes the unexplained literals from the calculation and makes discount changes easier to identify and maintain.

## Refactoring Approach 2 – Strategy Pattern

For a system in which discount behaviours are expected to grow or become more complex, I used the Strategy Pattern.

The final scalable version contains:

```text
DiscountStrategy
├── BookDiscount
├── ElectronicsDiscount
└── NoDiscount
```

Each strategy implements the same `apply()` operation, while a strategy mapping replaces the original conditional selection in `calculate_total_price()`.

This separates each discount behaviour and allows new strategies to be introduced without expanding the pricing function.

## My Response to Séba Daher’s Post

I replied to Séba’s initial post because we had identified the same two code smells. I agreed that Strategy offers a cleaner path for future extension, but I did not think it should automatically be the default when only two stable discount types exist.

My response focused on the expected rate of change. If the discount rules are simple and unlikely to change, the constants-based refactoring may be sufficient and easier to maintain. If the rules are expected to evolve independently, Strategy becomes more justified.

I also noted that keeping the discount value inside each strategy class keeps the value close to the behaviour it belongs to.

![My response to Séba Daher's post](images/my%20%20S%C3%A9ba%20Daher%20to%20S%C3%A9ba%20Daher%20post%20.png)

## Séba Daher’s Response to My Main Post

Séba responded to my main post and confirmed that we agreed on the location of the maintainability problem: magic numbers and the widening conditional.

His response then considered whether Strategy already earns its cost with only two item types. He argued that `BookDiscount` and `ElectronicsDiscount` are already active for the current system, and that only the abstract base class and mapping dictionary mainly anticipate future extension.

From that perspective, the additional structural cost is small enough for Strategy to provide value even if a third item type never appears.

This response helped me refine my position. The decision should not be based only on the number of current item types; it should also consider whether separating the behaviours already improves clarity, testability and maintainability in the present design.

![Séba Daher's response to my post](images/S%C3%A9ba%20Daher%20Response%20to%20my%20post%20.png)

## Discussion Reflection

The peer exchange helped me evaluate Strategy more critically rather than treating it as automatically better than a simple refactoring.

My final view is that:

- named constants are appropriate when the rules are small and stable;
- Strategy is more justified when behaviours are expected to evolve independently or when separating them already improves the design;
- the number of item types alone should not determine the refactoring choice.

This reflects the broader purpose of refactoring: improving the internal structure in a way that is proportionate to the real maintenance problem.

## Files

```text
Collaborative Discussion/
│   README.md
│   Unit 8 Collaborative Discussion 4 – Refactoring and Code Smells.pdf
│
├── code/
│   ├── Calculate_total_price.html
│   └── Scalable Alternative - Strategy Pattern.html
│
└── images/
    ├── my  Séba Daher to Séba Daher post .png
    └── Séba Daher Response to my post .png
```

## References

- Bergmann, D. (2026) *Code smells, explained*. IBM.
- Fowler, M. (2018) *Refactoring: Improving the Design of Existing Code*. 2nd edn. Boston, MA: Addison-Wesley.
- Refactoring.Guru (n.d.) *Strategy*. Available at: https://refactoring.guru/design-patterns/strategy
