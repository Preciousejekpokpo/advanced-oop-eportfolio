# BankAccount: Requirements and Test Evidence

![Figure 1. Requirements mapped to twelve original unit tests](bankaccount_test_traceability.png)

Figure 1 connects the banking requirements to their implementation and test evidence, revealing both the strengths of the locking strategy and the limits of the assurance obtained. The 5,000 concurrent deposits preserved the expected balance, while the contested-withdrawal test offered a more demanding examination of atomicity. With twenty threads requesting £10 from an account containing £100, exactly ten succeeded without overdrawing. These findings support the locking decisions, although `threading.Barrier` coordinates thread starts rather than controlling subsequent execution. Similarly, opposing transfers completed within five seconds, supporting the lock-ordering approach without establishing freedom from deadlocks under all conditions.

The mapping also exposes weaknesses that successful balance assertions cannot resolve. Account identifiers remain mutable despite determining transfer lock order, while currency precision is unrestricted. More significantly, the original simulator does not propagate worker-thread exceptions, allowing interrupted operations to escape the main test assertions. The later Strategy implementation improves error reporting but cannot reverse completed transactions. Further assurance therefore depends on varied execution schedules, explicit failure injection and recovery testing rather than additional passing tests alone.

## Evidence

- [Original account implementation](bank_account.py) and [simulator](transaction_simulator.py)
- [Twelve original unit tests](test_bank_account.py)
- [Strategy extension and error handling](STRATEGY_EVALUATION.md)
