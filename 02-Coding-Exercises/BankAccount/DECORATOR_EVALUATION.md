# Decorator and the Integrity of Transaction Records

Although the account locks in Part A protected balances during concurrent transactions, the system had no mechanism for recording those transactions. I introduced `RecordingAccount` to address this limitation without modifying `BankAccount`, keeping transaction recording separate from the underlying financial operations.

The initial ten tests passed, including 2,000 deposits across eight threads. However, matching balances and record counts only established consistency under the conditions tested. I extended the investigation to examine what happens when the financial operation succeeds but its record does not.

By forcing `_append()` to fail after a £25 deposit, I reproduced a discrepancy where the balance increased from £100 to £125 despite no record being saved. The caller received an exception, which could prompt a retry and potentially duplicate the payment. A second test showed that two wrappers sharing one `BankAccount` maintained separate histories. Although both tests passed, they exposed weaknesses in the design rather than demonstrating their resolution.

These findings have wider implications for reconciliation and disputed transactions. A customer might be charged without a corresponding record, while separate record collections could give different accounts of the same activity. Transfers introduce further uncertainty because recording the source outcome alone cannot establish a complete transaction history.

Decorator preserves the original balance logic, but its separate recording lock cannot guarantee that balance changes and records remain consistent. I would retain the wrapper as a design prototype while requiring durable, coordinated recording, unique transaction identifiers and controls against duplicate retries before considering real banking use. The additional tests strengthened my confidence in identifying the system's limitations, not in its readiness for deployment.

## Evidence

- [Decorator implementation](recording_account.py)
- [Functional tests](test_recording_account.py)
- [Failure-mode tests](test_recording_failure_modes.py)
- [Original account implementation](bank_account.py)
