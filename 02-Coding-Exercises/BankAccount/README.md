
# Thread-Safe Banking System

## Project Overview

This project examines how object-oriented programming and concurrency control can be used to maintain account integrity when multiple users perform banking transactions simultaneously.

The implementation consists of three Python files:

- `bank_account.py` – manages deposits, withdrawals, transfers and account balances.
- `transaction_simulator.py` – simulates concurrent banking operations using Python threads.
- `test_bank_account.py` – tests account operations, input validation and concurrent behaviour.

## Design Approach

The project applies encapsulation, input validation and thread synchronisation to protect shared account state. A consistent lock acquisition order is used for transfers to reduce the risk of deadlock.

## Running the Project

From the project directory, run:

```bash
python -m unittest test_bank_account.py -v
```

## Critical Evaluation

Thread synchronisation supports correctness but may introduce contention when many users access the same account. The implementation is an educational simulation rather than a production banking system. Further evaluation will consider scalability, transaction persistence and recovery from failures.
  