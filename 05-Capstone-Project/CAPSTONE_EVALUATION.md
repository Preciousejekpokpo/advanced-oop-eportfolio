# Capstone – Evaluating AI-Aware Transaction Verification

The capstone brought the earlier design patterns together to examine whether additional checks could improve the reliability of transaction evidence before model review.The architecture diagram in the capstone README illustrates how CapstoneWorkflow coordinates these components without changing the original account logic. Their separation supports reuse, but each verification stage still depends on the accuracy of the records it receives.

Seven integration tests passed, bringing the local banking suite to 72 tests. The additional record-count check detected an unrecorded £25 deposit and withdrawal whose effects cancelled, withholding model advice where balance reconciliation alone had passed. However, replacing both £25 records with £10 records preserved their count and net movement, allowing the mocked model to be consulted. The improvement therefore detects some missing records without establishing that recorded amounts are accurate.

Barr et al. (2015) examine the difficulty of establishing adequate test oracles. The passing tests confirmed the workflow's expected responses while demonstrating that misleading evidence could satisfy its checks. This limits the assurance gained from integrating otherwise well-tested components.

An authoritative transaction history and coordinated balance-and-record updates would provide stronger foundations for verification (PostgreSQL Global Development Group, n.d.). Recovery, performance and live-model behaviour remain untested. Until those gaps are addressed, model output should remain advisory.

## Evidence

- [Capstone workflow](../02-Coding-Exercises/BankAccount/capstone_workflow.py)
- [Seven integration tests](../02-Coding-Exercises/BankAccount/test_capstone_workflow.py)

## References

Barr, E.T., Harman, M., McMinn, P., Shahbaz, M. and Yoo, S. (2015) ‘The oracle problem in software testing: A survey’, *IEEE Transactions on Software Engineering*, 41(5), pp. 507–525. Available at https://doi.org/10.1109/TSE.2014.2372785 (Accessed 14 October 2026).

PostgreSQL Global Development Group (n.d.) ‘3.4 Transactions’, *PostgreSQL 17 Documentation*. Available at https://www.postgresql.org/docs/17/tutorial-transactions.html (Accessed 14 October 2026).
