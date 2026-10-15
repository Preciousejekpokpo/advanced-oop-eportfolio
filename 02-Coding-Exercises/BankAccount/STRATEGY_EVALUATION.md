# Strategy and the Cost of Interchangeable Transaction Behaviour

Part A used alternating deposits and withdrawals to make expected balances predictable, but testing different workloads required changes to `_user_session()`. The Strategy extension separated transaction selection from thread management. `AlternatingTransactions` and `DepositOnlyTransactions` implement a shared `apply()` interface, while `StrategySimulator` manages execution (Gamma et al., 1994). This allowed workloads to change between runs without altering the underlying account logic.

Seven additional tests passed, covering strategy switching, validation, concurrent deposits and worker failures. Unlike the original simulator, worker exceptions now reach the caller. However, reporting a failure cannot reverse transactions completed before it occurred. The improvement makes interrupted runs visible without establishing that their effects can be recovered.

Whether this design remains worthwhile depends on how the transaction policies develop. Prechelt et al. (2001) found that patterns could support maintenance, although simpler alternatives sometimes performed better. With only two workloads, a callable might achieve similar flexibility with less complexity. The interface becomes more useful if policies acquire distinct rules, although sharing one strategy instance across threads would require additional synchronisation if those policies maintained mutable state.

For now, I would retain Strategy because it allows workloads to be examined without repeatedly changing the simulator. Before extending it, I would investigate interrupted transactions and recovery, since reporting an error offers limited assurance about the state left behind.

## Evidence

- [Strategy implementation](strategy_simulator.py)
- [Strategy tests](test_strategy_simulator.py)
- [Original simulator](transaction_simulator.py)

## References

Gamma, E., Helm, R., Johnson, R. and Vlissides, J. (1994) *Design Patterns: Elements of Reusable Object-Oriented Software*. 1st edn. Addison-Wesley Professional. Available at https://www.pearson.com/en-gb/subject-catalog/p/design-patterns-elements-of-reusable-object-oriented-software/P200000009480/9780201633610 (Accessed 13 October 2026).

Prechelt, L., Unger, B., Tichy, W.F., Brössler, P. and Votta, L.G. (2001) ‘A controlled experiment in maintenance: Comparing design patterns to simpler solutions’, *IEEE Transactions on Software Engineering*, 27(12), pp. 1134–1144. Available at https://doi.org/10.1109/32.988711 (Accessed 13 October 2026).
