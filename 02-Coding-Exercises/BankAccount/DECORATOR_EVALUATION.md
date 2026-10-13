# Decorator and the Integrity of Transaction Records

The account locks in Part A protected balances during concurrent transactions, but provided no way of tracing those operations afterwards. I introduced `RecordingAccount` using the Decorator approach described by Gamma et al. (1994), allowing transaction recording to be added without changing the original account methods. Although this separated responsibilities, it also left balance updates and their records dependent on two separate operations.

The initial ten tests passed, including 2,000 deposits across eight threads. However, the failure tests revealed a problem that successful record counts had concealed. When I forced `_append()` to fail after a £25 deposit, the balance increased from £100 to £125 without a corresponding record. Featonby (2021) examines the danger of retrying operations when their outcome is uncertain and argues for identifying repeated requests. His analysis is relevant here because the caller receives an exception despite the completed deposit. Without a way to recognise the original request, retrying could repeat the transaction. My test established the inconsistent outcome, although it did not simulate a retry.

The second failure test showed that two wrappers sharing one account maintained separate transaction histories. Transfers created a similar concern because only the source wrapper recorded their outcome. These findings suggest that protecting the record list from concurrent changes does little to establish whether the history is complete. PostgreSQL's transaction model illustrates why related updates need to succeed or fail together (PostgreSQL Global Development Group, n.d.). However, introducing persistent storage alone would not resolve the problem while balance changes remained outside the same transactional boundary.

Decorator remains useful for separating recording from the original account logic, but I would not rely on this implementation for financial reconciliation. The evidence points towards coordinated, durable updates and transaction identifiers that can distinguish retries from new requests. Until those controls are established, improving the wrapper's recording functionality would do little to address the uncertainty exposed by the tests.

## Evidence

- [Decorator implementation](recording_account.py)
- [Functional tests](test_recording_account.py)
- [Failure-mode tests](test_recording_failure_modes.py)
- [Original account implementation](bank_account.py)

## References

Featonby, M. (2021) ‘Making retries safe with idempotent APIs’, *Amazon Builders’ Library*. Available at: https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/ (Accessed: 13 October 2026).

Gamma, E., Helm, R., Johnson, R. and Vlissides, J. (1994) *Design Patterns: Elements of Reusable Object-Oriented Software*. 1st edn. Addison-Wesley Professional. Available at: https://www.pearson.com/en-gb/subject-catalog/p/design-patterns-elements-of-reusable-object-oriented-software/P200000009480/9780201633610 (Accessed: 13 October 2026).

PostgreSQL Global Development Group (n.d.) ‘3.4 Transactions’, *PostgreSQL 17 Documentation*. Available at: https://www.postgresql.org/docs/17/tutorial-transactions.html (Accessed: 13 October 2026).
