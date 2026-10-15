# Abstract Factory and the Limits of Configuration Assurance

![Figure 3. Two related banking scenario configurations](abstract_factory_scenarios.png)

Figure 3 shows how `ScenarioFactory` assembles two banking scenarios. `BalanceScenarioFactory` checks movement against the scheduled alternating workload, while `RecordedScenarioFactory` compares it with movement reconstructed from `RecordingAccount` (Gamma et al., 1994). Both create compatible components, but their checks offer different assurance. The latter depends on the same records whose completeness remains uncertain.

All thirteen tests passed, with scenarios closing at £100 and £140, the latter producing eight records. More revealing were a failed record write after a £25 deposit and a deposit through a second wrapper. Both produced discrepancies, although the checks were called directly through `evaluate()`, so the tests establish detection under controlled conditions rather than reliable handling of a failed run.

Compatibility can also deteriorate after construction. Changing `StrategySimulator`'s strategy would leave `ScheduledBalanceCheck` using the original prediction, potentially rejecting a valid result, although this remains untested. `RecordedMovementCheck`, meanwhile, could accept opposing missing transactions because their net effect is zero. Both checks return `agrees`, despite drawing on evidence of different reliability. Even when it is false, `BankingScenario.run()` merely returns the result, while worker exceptions bypass verification altogether.

Naghdipour et al. (2023) examine the difficulty of selecting appropriate patterns, a trade-off visible here. With only two families, construction functions could offer similar consistency more simply. I would retain the factory to compare scenarios, but treat `agrees` as a diagnostic result until configuration changes and failure responses are tested.

## Evidence

- [Factory implementation](scenario_factories.py)
- [Thirteen factory tests](test_scenario_factories.py)

## References

Gamma, E., Helm, R., Johnson, R. and Vlissides, J. (1994) *Design Patterns: Elements of Reusable Object-Oriented Software*. 1st edn. Addison-Wesley Professional. Available at https://www.pearson.com/en-gb/subject-catalog/p/design-patterns-elements-of-reusable-object-oriented-software/P200000009480/9780201633610 (Accessed 14 October 2026).

Naghdipour, A., Hasheminejad, S.M.H. and Barmaki, R.L. (2023) ‘Software design pattern selection approaches: A systematic literature review’, *Software: Practice and Experience*, 53(4), pp. 1091–1122. Available at https://doi.org/10.1002/spe.3176 (Accessed 14 October 2026).
