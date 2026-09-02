# Collaborative Discussion: Structural Design Patterns

This collaborative discussion applies **Adapter, Bridge and Composite** patterns to Python-based cybersecurity scenarios. The examples focus on integration, separation of responsibilities and hierarchical organisation.


## 1. Adapter Pattern – Security Log Collector

The Adapter example addresses an interface mismatch between a legacy log collector and a modern monitoring interface.

- `SecurityEventSource` defines the target `get_events()` interface.
- `LegacyLogCollector` returns older string-based records through `read_old_logs()`.
- `LogAdapter` wraps the legacy collector and converts each `EVENT|SOURCE` string into a dictionary containing `event`, `source` and `system`.
- `ModernLogCollector` already returns events through `get_events()`.
- Both sources can therefore be stored together and merged through the same interface.

**Source code:** [`log_collector.html`](code/log_collector.html)

The execution result shows legacy and modern events combined into a single event list:

![Adapter execution result](images/log_collector_Execution%20Result.png)

### Peer Feedback on the Adapter Example

Donald Herbert Kofi Appeatsi Duodu highlighted the relevance of using a cybersecurity example and specifically noted that adapting legacy collectors into a common event structure is a sensible integration approach. The feedback also raised an important extension point: a production security pipeline may need additional fields such as timestamps or severity as the event schema grows.

![Donald Herbert Kofi Appeatsi Duodu replied](images/Donald%20Herbert%20Kofi%20Appeatsi%20Duodu%20replied.png)

## 2. Bridge Pattern – Security Alerts

The Bridge example separates **alert behaviour** from **delivery channels** so that both can vary independently.

- `AlertChannel` defines the `send()` interface.
- `ConsoleChannel`, `EmailChannel` and `SMSChannel` provide different delivery mechanisms.
- `SecurityAlert` stores a selected channel and delegates delivery through `channel.send()`.
- `CriticalAlert` refines the alert behaviour by adding a `CRITICAL` label without changing the delivery-channel classes.

This prevents an expanding class hierarchy such as `CriticalEmailAlert`, `CriticalSMSAlert`, `NormalEmailAlert`, and similar combinations.

**Source code:** [`security_alerts.html`](code/security_alerts.html)

The result demonstrates one normal console alert and critical alerts delivered through email and SMS:

![Bridge execution result](images/Security_Alerts_Execution%20Result.png)

## 3. Composite Pattern – Network Asset Inventory

The Composite example models individual network assets and groups through one common interface.

- `AssetComponent` defines the common `show()` operation.
- `Device` is the leaf component and represents a single asset.
- `AssetGroup` is the composite and can contain both devices and other groups.
- `Office Network` is the top-level composite containing `Security Perimeter`, `Server Network`, `Security Team` and `Employee Network`.

Because both leaves and composites implement `show()`, the complete asset inventory can be traversed and displayed through the same operation.

**Source code:** [`network_asset_inventory.html`](code/network_asset_inventory.html)

The execution result shows the complete office network as a hierarchy of groups and individual devices:

![Composite execution result](images/Network_Asset_Inventory_Execution%20Result.png)

### Peer Feedback on the Composite Example

Instructor Nawaz Khan positively highlighted the Composite example as a clear use of the pattern for representing employee access and grouped assets.

![Instructor Nawaz Khan replied](images/Nawaz%20Khan%20replied.png)

## Design Comparison

| Pattern | Problem Addressed | Example in this Activity |
|---|---|---|
| Adapter | Incompatible interfaces | Legacy and modern security logs |
| Bridge | Two dimensions that should vary independently | Alert type and delivery channel |
| Composite | Individual objects and groups should be treated uniformly | Devices and network asset groups |

## Full Discussion Document

**[Open Collaborative Discussion 1 Structural Patterns.pdf](Collaborative%20Discussion%201%20Structural%20Patterns.pdf)**

## References

**Gamma, E., Helm, R., Johnson, R. and Vlissides, J. (1994).** *Design Patterns: Elements of Reusable Object-Oriented Software.* Reading, MA: Addison-Wesley.

**Sarcar, V. (2022).** *Java Design Patterns: A Hands-On Experience with Real-World Examples.* 3rd edn. New York: Apress.
