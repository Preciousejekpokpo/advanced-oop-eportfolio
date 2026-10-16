# Abstract Factory and the Limits of Configuration Assurance

![Figure 3. Two related banking scenario configurations](abstract_factory_scenarios.png)

Figure 3 illustrates how `ScenarioFactory` assembles two related banking configurations. `BalanceScenarioFactory` compares results with the scheduled workload, while `RecordedScenarioFactory` reconstructs movement from `RecordingAccount` (Gamma et al., 1994). Although both configurations assemble compatible components, they depend on evidence of different reliability. The diagram illustrates this architectural distinction, while subsequent tests examine its consequences.

Thirteen tests passed. Scenarios ended at £100 and £140, the latter with eight records. Controlled failures involving a missing £25 record and a second wrapper produced discrepancies, but the tests called `evaluate()` directly. They demonstrate detection under controlled conditions, not dependable recovery when a running scenario fails.

Further limitations remain. Changing the simulator strategy after construction could invalidate the scheduled prediction, although I did not test that change. The recorded check could accept opposing missing transactions because their net effect is zero. Both checks return `agrees`, without indicating these differences in assurance. `BankingScenario.run()` also returns failed comparisons without resolving them, while worker exceptions bypass verification.

Naghdipour et al. (2023) examine the difficulty of choosing appropriate patterns. With only two configurations, simpler construction functions might suffice. I retain Abstract Factory to compare related scenarios, but would treat `agrees` as diagnostic until configuration changes and failure handling are tested.

## Evidence

- [Factory implementation](scenario_factories.py)
- [Thirteen factory tests](test_scenario_factories.py)

## References

Gamma, E., Helm, R., Johnson, R. and Vlissides, J. (1994) *Design Patterns: Elements of Reusable Object-Oriented Software*. 1st edn. Addison-Wesley Professional. Available at https://www.pearson.com/en-gb/subject-catalog/p/design-patterns-elements-of-reusable-object-oriented-software/P200000009480/9780201633610 (Accessed 14 October 2026).

Naghdipour, A., Hasheminejad, S.M.H. and Barmaki, R.L. (2023) ‘Software design pattern selection approaches: A systematic literature review’, *Software: Practice and Experience*, 53(4), pp. 1091–1122. Available at https://doi.org/10.1002/spe.3176 (Accessed 14 October 2026).
