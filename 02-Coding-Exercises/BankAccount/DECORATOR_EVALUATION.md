# Decorator and the Integrity of Transaction Records

The original banking tests showed that concurrent balance updates were protected under the tested conditions, but left individual operations difficult to trace. I introduced `RecordingAccount` through Decorator, extending the account without changing its financial logic (Gamma et al., 1994). Yet recording followed the balance update, placing the operation and its evidence on separate failure paths.

Ten functional tests passed, including 2,000 deposits across eight threads. These demonstrated successful recording under the tested conditions, but failure injection revealed a different outcome. When `_append()` failed after a £25 deposit, the balance rose from £100 to £125 without a record, while the caller received an exception. Featonby (2021) examines retry risks when outcomes are uncertain. Repeating the deposit could duplicate its effect, although the test did not attempt a retry.

Further tests showed that separate wrappers around one account held incomplete individual histories, while transfers appeared only in the source wrapper. Protecting each record list against concurrent modification did not make either history authoritative. The weakness lay in the relationship between the financial operation and its evidence, rather than simply in thread safety.

PostgreSQL's transaction model illustrates the value of committing related updates atomically (PostgreSQL Global Development Group, n.d.). Persistent storage alone would not resolve this inconsistency, while transaction identifiers could help identify retries without recovering missing records. I would retain Decorator for supplementary recording, but not treat this wrapper as a reliable audit trail. Coordinated, durable balance-and-record updates, supported by failure and recovery testing, would be needed before its records could support financial reconciliation.

## Evidence

- [Decorator implementation](recording_account.py)
- [Functional tests](test_recording_account.py)
- [Failure-mode tests](test_recording_failure_modes.py)
- [Original account implementation](bank_account.py)

## References

Featonby, M. (2021) ‘Making retries safe with idempotent APIs’, *Amazon Builders’ Library*. Available at https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/ (Accessed 13 October 2026).

Gamma, E., Helm, R., Johnson, R. and Vlissides, J. (1994) *Design Patterns: Elements of Reusable Object-Oriented Software*. 1st edn. Addison-Wesley Professional. Available at https://www.pearson.com/en-gb/subject-catalog/p/design-patterns-elements-of-reusable-object-oriented-software/P200000009480/9780201633610 (Accessed 13 October 2026).

PostgreSQL Global Development Group (n.d.) ‘3.4 Transactions’, *PostgreSQL 17 Documentation*. Available at https://www.postgresql.org/docs/17/tutorial-transactions.html (Accessed 13 October 2026).
