# Decorator and the Integrity of Transaction Records

The account locks in Part A protected balances during concurrent transactions, but provided no way of tracing those operations afterwards. I introduced `RecordingAccount` using the Decorator approach described by Gamma et al. (1994), allowing transaction recording without changing the original account methods. Although this separated responsibilities, recording took place only after the account operation had completed.

The initial ten tests passed, including 2,000 deposits across eight threads. However, the failure tests raised a more difficult question about what those results established. When I forced `_append()` to fail after a £25 deposit, the balance increased from £100 to £125 without a corresponding record. More concerning was that the caller received an exception even though the deposit had succeeded. Featonby (2021) examines the risks of retrying operations when their outcome is uncertain. Here, retrying could duplicate the deposit, although my test established the uncertainty rather than demonstrating an actual retry.

Another test showed that two wrappers sharing one account maintained separate histories. Transfers exposed a related limitation because only the source wrapper recorded their outcome. These findings made me question the value of protecting the record list against concurrent updates when its completeness could not be established.

The difficulty lies in the boundary introduced by the design. Decorator allowed me to extend the account without altering its financial logic, but the balance and its record could succeed or fail independently. PostgreSQL's transaction model illustrates why related updates require a shared atomic boundary (PostgreSQL Global Development Group, n.d.). Transaction identifiers could help distinguish retries, but would not recover missing records, while persistent storage alone would leave the underlying inconsistency unresolved.

I would retain Decorator for optional extensions, but not rely on this implementation for financial reconciliation. Establishing coordinated, durable balance-and-record updates would take priority over expanding a reporting layer whose evidence may already be incomplete.

## Evidence

- [Decorator implementation](recording_account.py)
- [Functional tests](test_recording_account.py)
- [Failure-mode tests](test_recording_failure_modes.py)
- [Original account implementation](bank_account.py)

## References

Featonby, M. (2021) ‘Making retries safe with idempotent APIs’, *Amazon Builders’ Library*. Available at: https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/ (Accessed: 13 October 2026).

Gamma, E., Helm, R., Johnson, R. and Vlissides, J. (1994) *Design Patterns: Elements of Reusable Object-Oriented Software*. 1st edn. Addison-Wesley Professional. Available at: https://www.pearson.com/en-gb/subject-catalog/p/design-patterns-elements-of-reusable-object-oriented-software/P200000009480/9780201633610 (Accessed: 13 October 2026).

PostgreSQL Global Development Group (n.d.) ‘3.4 Transactions’, *PostgreSQL 17 Documentation*. Available at: https://www.postgresql.org/docs/17/tutorial-transactions.html (Accessed: 13 October 2026).
