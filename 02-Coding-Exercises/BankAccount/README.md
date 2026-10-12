# Thread-Safe Banking System

## Overview

The initial concurrency test produced the expected balance of 5,000 after ten threads completed 500 deposits each, although this result raised questions about how much of the account's behaviour had actually been tested. Deposits could reveal lost updates, but competing withdrawals presented a different concern, particularly when several threads attempted to access funds that could not satisfy every request. This shaped my approach to testing, placing greater emphasis on whether the account preserved its financial constraints under concurrent execution.

I separated account management, simulation and testing into three modules, keeping synchronisation within `BankAccount` through per-account locks. The withdrawal check and deduction share one critical section, while transfers acquire two account locks in a consistent order using account numbers and object identity to address circular waiting.

The twelve tests covered transaction validation, concurrent deposits, contested withdrawals and transfers, with all tests passing and the simulator returning £1,000 as expected. Although barriers increased contention, the results remain specific to the scenarios examined rather than establishing correctness under every possible thread schedule.

The [Part A report](Thread%20Safe%20Banking%20System%20Report-%20submission.docx) contains the original methodology, diagrams, design decisions and critical evaluation.

## Code and Supporting Evidence

| File | Contents |
|---|---|
| [bank_account.py](bank_account.py) | Account operations and synchronisation |
| [transaction_simulator.py](transaction_simulator.py) | Concurrent transaction simulation |
| [test_bank_account.py](test_bank_account.py) | Twelve unit and concurrency tests |
| [Part A report](Thread%20Safe%20Banking%20System%20Report-%20submission.docx) | Design, testing and evaluation |

## Running the Code

Run the tests from the project directory.

`python -m unittest -v test_bank_account.py`

Run the simulation.

`python transaction_simulator.py`

No external packages are required.

## Further Investigation

The lecturer's feedback brought the unresolved scalability question into sharper focus, particularly whether per-account locking remains efficient as contention increases. I intend to compare workloads concentrated on one account with those distributed across several, while examining how mutable account identifiers affect transfer ordering.

The simulator's fixed transaction sequence also provides a reason to investigate Strategy, although its value will depend on whether the added flexibility improves testing and maintainability enough to justify another abstraction.
