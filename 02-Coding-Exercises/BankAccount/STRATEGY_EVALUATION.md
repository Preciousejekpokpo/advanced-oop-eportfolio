# Strategy and the Cost of Interchangeable Transaction Behaviour

In Part A, the fixed sequence of deposits and withdrawals made the final balance easier to predict when several threads shared an account. This worked well for the original concurrency tests, but became restrictive when I wanted to examine different transaction workloads. Changing the sequence meant editing `_user_session()`, leaving transaction selection tied to the simulator's thread-management logic.

I introduced `TransactionStrategy` to separate these responsibilities, following the Strategy approach described by Gamma et al. (1994). `AlternatingTransactions` and `DepositOnlyTransactions` now provide different behaviours through a shared `apply()` interface, while `StrategySimulator` manages the threads. The selected strategy is captured at the beginning of each run, allowing workloads to change between runs without altering the worker logic. This addresses the original restriction, although it introduces an abstraction whose value still needs examining.

All seven additional tests passed, covering strategy switching, concurrent deposits, input validation and worker-error reporting. Propagating worker exceptions improves the visibility of failed simulations, but cannot undo transactions completed before an error occurs. A reported failure may therefore leave the account partially updated, which the current implementation does not attempt to recover.

The crucial question is whether this flexibility warrants the additional interface and classes. Prechelt et al. (2001) found maintenance benefits from design patterns in most of their experimental tasks, although simpler alternatives performed better in some cases. Here, a callable could support basic workload changes with less code, while an explicit strategy interface becomes more useful as transaction policies develop different rules and testing requirements. The current strategies share no mutable state, but future stateful policies would need synchronisation because one strategy instance serves multiple threads. For this implementation, Strategy makes workload comparisons easier without establishing any performance benefit.

## Evidence

- [Strategy implementation](strategy_simulator.py)
- [Strategy tests](test_strategy_simulator.py)
- [Original simulator](transaction_simulator.py)

## References

Gamma, E., Helm, R., Johnson, R. and Vlissides, J. (1994) *Design Patterns: Elements of Reusable Object-Oriented Software*. 1st edn. Addison-Wesley Professional. Available at: https://www.pearson.com/en-gb/subject-catalog/p/design-patterns-elements-of-reusable-object-oriented-software/P200000009480/9780201633610 (Accessed: 13 October 2026).

Prechelt, L., Unger, B., Tichy, W.F., Brössler, P. and Votta, L.G. (2001) ‘A controlled experiment in maintenance: comparing design patterns to simpler solutions’, *IEEE Transactions on Software Engineering*, 27(12), pp. 1134–1144. Available at: https://doi.org/10.1109/32.988711 (Accessed: 13 October 2026).
