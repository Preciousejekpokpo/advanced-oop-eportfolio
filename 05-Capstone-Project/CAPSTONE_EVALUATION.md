# Capstone – Evaluating AI-Aware Transaction Verification

The capstone followed a weakness exposed during model-review testing. An unrecorded deposit and withdrawal could cancel financially, allowing reconciliation to pass despite missing evidence. I brought the earlier patterns together in `CapstoneWorkflow` and added a record-count check before model advice, as shown in the [architecture diagram](README.md).

Seven integration tests passed, bringing the reported banking suite to 72. The new check detected two missing £25 records that balance reconciliation overlooked. Yet when £10 records replaced both £25 entries, the count and net movement still matched, allowing mocked model review. This exposed a harder problem than missing evidence. The workflow could count records, but could not establish whether they represented the operations performed.

Barr et al. (2015) examine the test oracle problem, relevant here because passing assertions confirmed the rules worked while exposing how little they verified. Failure handling remained uneven. Invalid model responses prompted manual review, but a recording exception stopped the workflow after a deposit had already changed the balance. Retrying might duplicate that deposit, although no recovery or retry was tested.

I would retain the count check as a diagnostic rather than treat it as reconciliation. Coordinated, durable balance-and-record updates (PostgreSQL Global Development Group, n.d.) and independent transaction-level verification should take priority, followed by recovery testing. Those measures and live-model behaviour remain untested.

## Evidence

- [Capstone workflow](../02-Coding-Exercises/BankAccount/capstone_workflow.py)
- [Seven integration tests](../02-Coding-Exercises/BankAccount/test_capstone_workflow.py)

## References

Barr, E.T., Harman, M., McMinn, P., Shahbaz, M. and Yoo, S. (2015) ‘The oracle problem in software testing: A survey’, *IEEE Transactions on Software Engineering*, 41(5), pp. 507–525. Available at https://doi.org/10.1109/TSE.2014.2372785 (Accessed 14 October 2026).

PostgreSQL Global Development Group (n.d.) ‘3.4 Transactions’, *PostgreSQL 17 Documentation*. Available at https://www.postgresql.org/docs/17/tutorial-transactions.html (Accessed 14 October 2026).
