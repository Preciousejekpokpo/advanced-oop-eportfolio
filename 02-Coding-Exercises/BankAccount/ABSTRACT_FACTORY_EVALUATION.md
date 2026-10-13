# Abstract Factory and the Limits of Configuration Assurance

The earlier exercises introduced different requirements for account simulation. Alternating transactions needed predictable balance checks, while recorded deposits required comparison with the account's transaction history. I introduced `ScenarioFactory` to create the account, strategy and verification method together, reducing the risk of combining unsuitable components.

All thirteen additional tests passed. `BalanceScenarioFactory` produced the expected £100, while `RecordedScenarioFactory` returned £140 with eight recorded deposits. However, the failure tests exposed limitations in this approach. When recording failed after a £25 deposit, the balance changed despite the missing record, although verification detected the discrepancy. Another test showed that transactions processed through a separate wrapper could be missing from the configured account's history. The components were correctly assembled, but their records could still be incomplete.

This raises concerns about the reliability of verification. `RecordedMovementCheck` compares net changes, meaning an unrecorded deposit and withdrawal of equal value could leave the figures matching despite missing transactions. Even when a discrepancy is detected, `BankingScenario.run()` returns `False` without requiring further action. Unless the caller responds, the problem could remain unresolved while subsequent decisions rely on those records.

Abstract Factory helped organise the scenarios, although two configurations may not justify the additional interfaces and classes. Simpler construction functions could achieve similar results with less complexity. I would retain the pattern if future requirements introduced more demanding configurations, but the tests suggest that reliable transaction recording and clear responses to verification failures deserve greater attention before expanding the architecture.

## Evidence

- [Abstract Factory implementation](scenario_factories.py)
- [Thirteen factory tests](test_scenario_factories.py)
- [Decorator failure-mode tests](test_recording_failure_modes.py)
- [Visitor implementation](transaction_visitors.py)
