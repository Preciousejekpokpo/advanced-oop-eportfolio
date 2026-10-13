# Strategy and the Cost of Interchangeable Transaction Behaviour

In Part A, the fixed sequence of deposits and withdrawals made the final balance easier to predict when several threads shared an account. This worked well for the original concurrency tests, but became restrictive when I wanted to examine different transaction workloads. Changing the sequence meant editing `_user_session()`, leaving transaction selection tied to the simulator's thread-management logic.

I introduced `TransactionStrategy` to separate these responsibilities, following the Strategy approach described by Gamma et al. (1994). `AlternatingTransactions` and `DepositOnlyTransactions` now provide different behaviours through a shared `apply()` interface, while `StrategySimulator` continues to manage the threads. The selected strategy is captured at the beginning of each run, allowing workloads to change between runs without modifying the account or worker logic. This addresses the extensibility limitation identified in Part A, although the additional abstraction needs to justify its place in the design.

All seven additional tests passed, covering strategy switching, concurrent deposits, input validation and worker-error reporting. Propagating worker exceptions improves the visibility of failed simulations, but it does not undo transactions completed before an error occurs. A reported failure may therefore leave the account in a partially updated state, which the current implementation does not attempt to recover.

The crucial question is whether this flexibility warrants the additional interface and classes. Prechelt et al. (2001) found benefits from design patterns in most of their nine maintenance tasks, although simpler alternatives performed better in some cases. Their findings reinforce the need to assess the pattern against the problem being solved. Here, a callable could support basic workload changes with less code, while an explicit strategy interface becomes more useful as transaction policies develop different rules and testing requirements. The current strategies share no mutable internal state, but future stateful policies would also need careful synchronisation because the same strategy instance is used by multiple threads.

The clearest benefit of Strategy in this implementation is the ability to compare different transaction workloads without changing the simulator's worker logic. The tests support that flexibility, although they provide no evidence of improved performance. I would also need to reconsider the concurrency risks if future strategies maintained shared state, since the same strategy instance is used across multiple threads.
## Evidence

- [Strategy implementation](strategy_simulator.py)
- [Strategy tests](test_strategy_simulator.py)
- [Original simulator](transaction_simulator.py)

## References

Gamma, E., Helm, R., Johnson, R. and Vlissides, J. (1994) *Design Patterns: Elements of Reusable Object-Oriented Software*. 1st edn. Addison-Wesley Professional. Available at: https://www.pearson.com/en-gb/subject-catalog/p/design-patterns-elements-of-reusable-object-oriented-software/P200000009480/9780201633610 (Accessed: 13 October 2026).

Prechelt, L., Unger, B., Tichy, W.F., Brössler, P. and Votta, L.G. (2001) ‘A controlled experiment in maintenance: comparing design patterns to simpler solutions’, *IEEE Transactions on Software Engineering*, 27(12), pp. 1134–1144. Available at: https://doi.org/10.1109/32.988711 (Accessed: 13 October 2026).
