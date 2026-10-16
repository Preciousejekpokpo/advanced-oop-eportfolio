# Strategy and the Cost of Interchangeable Transaction Behaviour

The original simulator fixed each user to alternating deposits and withdrawals, so examining a different workload required editing `_user_session()`. I introduced `TransactionStrategy` to separate transaction choice from thread management. `AlternatingTransactions` and `DepositOnlyTransactions` implement `apply()`, while `StrategySimulator` allows workloads to change between runs without modifying `BankAccount` (Gamma et al., 1994).

Seven tests passed, covering policy switching, invalid inputs, concurrent deposits and worker failures. Unlike the original simulator, worker exceptions now reach the caller. That makes interrupted runs visible but cannot reverse transactions completed before a failure. The simulator also takes a snapshot of the chosen strategy for each run. However, sharing a strategy with mutable internal state could introduce new concurrency risks, which I have not tested.

Prechelt et al. (2001) found maintenance benefits for patterns in most examined tasks, although simpler approaches sometimes performed better. With only two stateless policies, a callable might provide comparable flexibility with less complexity. I would retain Strategy for comparing workloads independently of threading, but reconsider the abstraction if policies remain simple. Investigating recovery after worker failures is more important than adding further strategies.

## Evidence

- [Strategy implementation](strategy_simulator.py)
- [Strategy tests](test_strategy_simulator.py)
- [Original simulator](transaction_simulator.py)

## References

Gamma, E., Helm, R., Johnson, R. and Vlissides, J. (1994) *Design Patterns: Elements of Reusable Object-Oriented Software*. 1st edn. Addison-Wesley Professional. Available at https://www.pearson.com/en-gb/subject-catalog/p/design-patterns-elements-of-reusable-object-oriented-software/P200000009480/9780201633610 (Accessed 13 October 2026).

Prechelt, L., Unger, B., Tichy, W.F., Brössler, P. and Votta, L.G. (2001) ‘A controlled experiment in maintenance: Comparing design patterns to simpler solutions’, *IEEE Transactions on Software Engineering*, 27(12), pp. 1134–1144. Available at https://doi.org/10.1109/32.988711 (Accessed 13 October 2026).
