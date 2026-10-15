# Capstone – Evaluating AI-Aware Transaction Verification

The capstone followed a weakness exposed during model-review testing. An unrecorded deposit and withdrawal could cancel financially, allowing reconciliation to pass despite missing evidence. `CapstoneWorkflow` integrated the earlier patterns and added a record-count check before requesting model advice, as shown in the [architecture diagram](README.md).

Seven integration tests passed, bringing the reported banking suite to 72. The check detected an unrecorded £25 deposit and withdrawal that reconciliation had missed. Yet replacing both £25 records with £10 entries preserved their count and net movement, allowing mocked model review. Counting entries establishes their quantity, not whether they represent the transactions performed. The workflow still relies on records produced by the mechanism whose reliability was in question.

Barr et al. (2015) examine the difficulty of establishing adequate test oracles. Here, passing tests confirmed the workflow's specified responses while showing that inaccurate evidence could satisfy its checks. Recording exceptions stopped the workflow without reversing completed balance updates. Invalid model responses required manual review, although no operational review process was tested. These safeguards restrict access to model advice without resolving the underlying inconsistency.

An authoritative transaction history with coordinated, durable balance-and-record updates would address that failure boundary (PostgreSQL Global Development Group, n.d.). Recovery, performance and live-model behaviour remain untested. Until transaction evidence can be independently verified, model recommendations should remain advisory.

## Evidence

- [Capstone workflow](../02-Coding-Exercises/BankAccount/capstone_workflow.py)
- [Seven integration tests](../02-Coding-Exercises/BankAccount/test_capstone_workflow.py)

## References

Barr, E.T., Harman, M., McMinn, P., Shahbaz, M. and Yoo, S. (2015) ‘The oracle problem in software testing: A survey’, *IEEE Transactions on Software Engineering*, 41(5), pp. 507–525. Available at https://doi.org/10.1109/TSE.2014.2372785 (Accessed 14 October 2026).

PostgreSQL Global Development Group (n.d.) ‘3.4 Transactions’, *PostgreSQL 17 Documentation*. Available at https://www.postgresql.org/docs/17/tutorial-transactions.html (Accessed 14 October 2026).
