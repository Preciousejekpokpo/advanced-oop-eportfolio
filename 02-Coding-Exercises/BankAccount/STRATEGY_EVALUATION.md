# Strategy and the Cost of Interchangeable Transaction Behaviour

In Part A, I kept the simulator's transaction sequence fixed, which made the expected balance predictable and helped isolate concurrency errors. However, that simplicity became restrictive when I needed to examine alternative workloads, since changing the sequence required modifying `_user_session()`. This exposed a weakness in the original Open/Closed design, although I questioned whether introducing another abstraction would improve the simulator enough to justify its complexity.

I used `TransactionStrategy` to define a shared `apply()` interface, allowing `AlternatingTransactions` and `DepositOnlyTransactions` to supply different behaviours while `StrategySimulator` retained responsibility for thread execution. The simulator captures the selected strategy at the beginning of each run, so changing policies between runs does not require altering the account logic.

All seven additional tests passed, including strategy switching, concurrent deposits and worker-error reporting. Switching policies produced the expected balances, while propagating worker exceptions addressed a weakness in the original simulation approach. However, reporting a failed operation does not reverse transactions already completed, which limits the assurance these tests provide.

The trade-off lies in the additional interface and classes required to replace a short conditional statement. A simpler callable could support limited variation, although the explicit strategy interface becomes more defensible as policies acquire distinct rules and tests. The current strategies also contain no mutable state, whereas future stateful policies could introduce new synchronisation concerns.

I would retain Strategy for testing alternative workloads, but its contribution is behavioural flexibility rather than demonstrated scalability. Further extensions should be judged by whether they reduce changes to existing code without making concurrent behaviour harder to reason about.

## Evidence

- [Strategy implementation](strategy_simulator.py)
- [Strategy tests](test_strategy_simulator.py)
- [Original simulator](transaction_simulator.py)
