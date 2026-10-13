# Abstract Factory and the Limits of Configuration Assurance

The earlier exercises left me with different ways of running and checking account simulations. Alternating transactions could be assessed against an expected balance, while recorded deposits needed comparison with their transaction history. I introduced `ScenarioFactory` to bring the account, transaction strategy and evidence check together. This follows Gamma et al. (1994), who describe Abstract Factory as a way of creating related objects intended to work together. Here, its immediate benefit was making those relationships explicit instead of relying on the caller to assemble each configuration correctly.

All thirteen factory tests passed. `BalanceScenarioFactory` produced the expected £100, while `RecordedScenarioFactory` returned £140 with eight recorded deposits. These results support the intended component pairings, but the failure tests exposed how little correct assembly could establish about the transactions themselves. When a £25 deposit went unrecorded, the evidence check detected the difference between the balance and recorded movement. A separate wrapper also left activity outside the configured account's history. Both discrepancies were identified by calling the check directly, without running the full scenario.

The design therefore offers some protection against unsuitable configurations, although that protection has limits. `RecordedMovementCheck` compares net movements, so agreement cannot establish that every transaction was captured. The factory establishes the initial configuration but does not preserve it once the scenario has been created. `StrategySimulator` permits its strategy to be replaced, potentially invalidating the expected balance calculated for the original workload. I have not tested that modification, but the implementation leaves it possible. When the simulator completes and verification identifies a discrepancy, `BankingScenario.run()` returns the comparison result without enforcing a response. A worker exception follows a different path, interrupting the scenario before that verification occurs.

Gamma et al. (1994) also recognise that adding new kinds of products can make Abstract Factory harder to extend. That cost is worth considering alongside Naghdipour, Hasheminejad and Barmaki's (2023) review of the difficulties involved in selecting suitable design patterns. With only two configurations, the additional interfaces and classes are difficult to justify when simpler construction functions could establish the same initial pairings. Additional scenarios with different dependencies might strengthen the case for keeping the pattern, but that benefit remains prospective.

I would retain Abstract Factory if the number and complexity of configurations increased. For the present implementation, its clearest contribution is organising how the experiments begin. The remaining weaknesses lie in what can change afterwards and how verification failures are handled. Addressing those weaknesses would offer stronger grounds for trusting the scenarios than adding further factories.

## Evidence

- [Abstract Factory implementation](scenario_factories.py)
- [Thirteen factory tests](test_scenario_factories.py)
- [Decorator failure-mode tests](test_recording_failure_modes.py)
- [Visitor implementation](transaction_visitors.py)

## References

Gamma, E., Helm, R., Johnson, R. and Vlissides, J. (1994) *Design Patterns: Elements of Reusable Object-Oriented Software*. 1st edn. Addison-Wesley Professional. Available at: https://www.pearson.com/en-gb/subject-catalog/p/design-patterns-elements-of-reusable-object-oriented-software/P200000009480/9780201633610 (Accessed: 14 October 2026).

Naghdipour, A., Hasheminejad, S.M.H. and Barmaki, R.L. (2023) ‘Software design pattern selection approaches: A systematic literature review’, *Software: Practice and Experience*, 53(4), pp. 1091–1122. Available at: https://doi.org/10.1002/spe.3176 (Accessed: 14 October 2026).
