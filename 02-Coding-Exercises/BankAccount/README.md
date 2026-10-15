# Thread-Safe Banking System

The original banking system used per-account locks to protect balances and consistent lock ordering to prevent circular waits during transfers. Twelve tests passed, supporting correctness under the tested conditions without establishing reliability across every possible thread schedule.

Lecturer feedback prompted further investigation into [requirements traceability](REQUIREMENTS_AND_TEST_EVIDENCE.md) and [lock contention](CONTENTION_EVALUATION.md). The benchmark found no sustained performance advantage for separate accounts, while the fixed simulation workload motivated the Strategy extension. These investigations informed the later design-pattern exercises.

## Original Part A Artefacts

- [Previously submitted report and diagrams](Thread%20Safe%20Banking%20System%20Report-%20submission.docx)
- [Account implementation](bank_account.py), [simulator](transaction_simulator.py) and [twelve tests](test_bank_account.py)

## Subsequent Investigations

- [Strategy](STRATEGY_EVALUATION.md), [Decorator](DECORATOR_EVALUATION.md), [Visitor](VISITOR_EVALUATION.md) and [Abstract Factory](ABSTRACT_FACTORY_EVALUATION.md)

Run the original tests using `python -m unittest -v test_bank_account.py`.
