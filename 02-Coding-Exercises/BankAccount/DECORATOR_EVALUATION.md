# Decorator and the Integrity of Transaction Records

The original banking tests supported balance protection under the schedules examined, but did not show which operations produced those balances. I introduced `RecordingAccount` through Decorator to capture outcomes without changing `BankAccount` (Gamma et al., 1994). Recording happens after the financial update, however, so the account lock and record-list lock do not make the two actions atomic.

Ten functional tests passed, including 2,000 deposits across eight threads. They confirmed expected balances and record counts in those runs. When I forced `_append()` to fail after a £25 deposit, the balance increased from £100 to £125 without a record, while the caller received an exception. Retrying could duplicate the credit, although I did not test this. Featonby (2021) discusses why uncertain outcomes make retries difficult to handle safely.

Two wrappers around the same account also maintained separate, incomplete histories, while transfers appeared only in the source wrapper. The record-list lock protected each list against concurrent modification, not the completeness of the underlying financial history. Adding further locking around the list would not address this separation.

PostgreSQL's transaction model shows how related changes can be committed together (PostgreSQL Global Development Group, n.d.), but my implementation has no durable or coordinated recording mechanism. A persisted transaction identifier could help identify retries without restoring missing evidence. I would retain Decorator for supplementary diagnostics, not an authoritative audit trail, until coordinated updates and failure-recovery tests establish stronger assurance.

## Evidence

- [Decorator implementation](recording_account.py)
- [Functional tests](test_recording_account.py)
- [Failure-mode tests](test_recording_failure_modes.py)
- [Original account implementation](bank_account.py)

## References

Featonby, M. (2021) ‘Making retries safe with idempotent APIs’, *Amazon Builders’ Library*. Available at https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/ (Accessed 13 October 2026).

Gamma, E., Helm, R., Johnson, R. and Vlissides, J. (1994) *Design Patterns: Elements of Reusable Object-Oriented Software*. 1st edn. Addison-Wesley Professional. Available at https://www.pearson.com/en-gb/subject-catalog/p/design-patterns-elements-of-reusable-object-oriented-software/P200000009480/9780201633610 (Accessed 13 October 2026).

PostgreSQL Global Development Group (n.d.) ‘3.4 Transactions’, *PostgreSQL 17 Documentation*. Available at https://www.postgresql.org/docs/17/tutorial-transactions.html (Accessed 13 October 2026).
