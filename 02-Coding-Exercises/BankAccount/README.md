# Thread-Safe Banking System

The original assignment separated account management, concurrent simulation and testing to make the locking decisions visible. `BankAccount` protects the withdrawal check and deduction in one critical section, while transfers acquire both account locks in a consistent order. Twelve tests passed, although no finite set of concurrent runs can establish correctness under every thread schedule.

The lecturer's feedback brought the unresolved scalability question into sharper focus, particularly how per-account locking would behave under contention. My later experiments found no sustained advantage for separate accounts, while the fixed transaction sequence prompted the Strategy extension. Both investigations grew from limitations in the original design, and the linked evaluations examine what the tests still cannot establish.

## Original Part A Artefacts

- [Previously submitted report, diagrams and evaluation](Thread%20Safe%20Banking%20System%20Report-%20submission.docx)
- [Account implementation](bank_account.py), [simulator](transaction_simulator.py) and [twelve tests](test_bank_account.py)

## Subsequent Investigations

- [Requirements and testing evidence](REQUIREMENTS_AND_TEST_EVIDENCE.md)
- [Contention evaluation](CONTENTION_EVALUATION.md)
- [Strategy](STRATEGY_EVALUATION.md), [Decorator](DECORATOR_EVALUATION.md), [Visitor](VISITOR_EVALUATION.md) and [Abstract Factory](ABSTRACT_FACTORY_EVALUATION.md)

Run the original tests using `python -m unittest -v test_bank_account.py`.
