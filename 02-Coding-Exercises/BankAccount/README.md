# Thread-Safe Banking System

The original banking assignment examined how concurrent transactions could preserve account balances without lost updates, overspending or deadlocks. I separated account management, simulation and testing, keeping synchronisation within `BankAccount`. The withdrawal check and deduction share one critical section, while transfers acquire both account locks in a consistent order to reduce circular waiting.

Twelve tests passed, including 5,000 concurrent deposits, twenty competing £10 withdrawals from a £100 balance and opposing transfers. Exactly ten withdrawals succeeded, while both transfer threads completed within five seconds. These results supported the locking decisions, although the barriers used to increase contention could not reproduce every possible thread schedule.

## Further Investigation

The lecturer's feedback brought the unresolved scalability question into sharper focus, particularly whether per-account locking would remain effective as contention increased. I explored this through comparisons of shared and separate accounts, finding no consistent performance advantage. The simulator's fixed transaction sequence also prompted the Strategy extension, although its flexibility came with additional abstraction. Mutable account identifiers and incomplete worker-error reporting remain concerns. I want to examine these weaknesses more closely before judging how reliably the design could support less controlled workloads.

## Original Part A Artefacts

- [Previously submitted technical report, including diagrams and evaluation](Thread%20Safe%20Banking%20System%20Report-%20submission.docx)
- [Bank account implementation](bank_account.py)
- [Transaction simulator](transaction_simulator.py)
- [Original twelve tests](test_bank_account.py)

## Subsequent Investigations

- [Requirements and testing evidence](REQUIREMENTS_AND_TEST_EVIDENCE.md)
- [Contention evaluation](CONTENTION_EVALUATION.md)
- [Strategy](STRATEGY_EVALUATION.md), [Decorator](DECORATOR_EVALUATION.md), [Visitor](VISITOR_EVALUATION.md) and [Abstract Factory](ABSTRACT_FACTORY_EVALUATION.md)

Run the original tests from this folder using `python -m unittest -v test_bank_account.py`.
