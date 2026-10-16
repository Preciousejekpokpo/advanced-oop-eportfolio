# BankAccount Requirements and Test Evidence

![Figure 1. Requirements mapped to twelve original unit tests](bankaccount_test_traceability.png)

Figure 1 links the banking requirements to twelve tests, while exposing what those tests cannot establish. Ten threads made 5,000 deposits without losing an update. Of twenty competing £10 withdrawals against £100, exactly ten succeeded, preventing an overdraft. Opposing transfers also completed within five seconds without changing the combined balance. These results supported per-account locking, but `threading.Barrier` synchronises only the start. It cannot reproduce every thread schedule or rule out failures under different conditions.

Mapping the requirements against the tests showed that a correct final balance could conceal a worker failure. I addressed this gap in the later [Strategy extension](STRATEGY_EVALUATION.md) by collecting exceptions from worker threads and reporting them to the caller, supported by tests that deliberately triggered failures. The [contention investigation](CONTENTION_EVALUATION.md) also allowed me to examine the performance assumptions behind the original locking approach. Other weaknesses remain. Account identifiers can still change despite determining transfer lock order, and monetary amounts are not restricted to two decimal places. These require further changes and testing, while recovery from interrupted transactions remains unproven. The improvement was making failures easier to detect, rather than establishing that the banking system could recover from them.

## Evidence

- [Original account implementation](bank_account.py) and [simulator](transaction_simulator.py)
- [Twelve original unit tests](test_bank_account.py)
- [Strategy extension and error handling](STRATEGY_EVALUATION.md)
- [Contention benchmark and evaluation](CONTENTION_EVALUATION.md)
