# Capstone Evaluation of AI-Aware Transaction Verification

The capstone followed a weakness exposed during model-review testing, where an unrecorded deposit and withdrawal could cancel each other out, allowing reconciliation to pass despite the incomplete history. I brought Strategy, Decorator, Visitor and Abstract Factory together in `CapstoneWorkflow`, adding a record-count check before model advice, as illustrated in the [architecture diagram](README.md). While the patterns made it easier to separate and test individual responsibilities, their integration raised a more difficult question about whether those components could collectively provide reliable transaction evidence.

Seven integration tests passed, bringing the reported banking suite to 72. The additional check detected two missing £25 records that reconciliation had overlooked, but when both amounts were replaced with £10, the count and net movement still matched, allowing mocked model review to proceed. The system could establish how many records existed without confirming that they represented the transactions performed. Barr et al. (2015) examine the test-oracle problem, which helped me understand why passing assertions did not necessarily provide sufficient evidence of correctness. 

Recording failures remained more difficult because an exception could stop the workflow after a deposit had already changed the balance, leaving recovery unresolved. Although I would retain the record-count check as an additional safeguard, its usefulness depends on the reliability of the underlying records. Bringing balance changes and transaction records into the same database transaction, supported by failure and recovery testing, would provide a stronger basis for financial verification (PostgreSQL Global Development Group, n.d.). These improvements remain untested.

## Evidence

- [Capstone workflow](../02-Coding-Exercises/BankAccount/capstone_workflow.py)
- [Seven integration tests](../02-Coding-Exercises/BankAccount/test_capstone_workflow.py)

## References

Barr, E.T., Harman, M., McMinn, P., Shahbaz, M. and Yoo, S. (2015) ‘The oracle problem in software testing: A survey’, *IEEE Transactions on Software Engineering*, 41(5), pp. 507–525. Available at https://doi.org/10.1109/TSE.2014.2372785 (Accessed 14 October 2026).

PostgreSQL Global Development Group (n.d.) ‘3.4 Transactions’, *PostgreSQL 17 Documentation*. Available at https://www.postgresql.org/docs/17/tutorial-transactions.html (Accessed 14 October 2026).
