# Visitor and the Reliability of Financial Reporting

The recording failures uncovered during Decorator testing made me question how much confidence could be placed in reports generated from incomplete transaction histories. I introduced Visitor to separate cash-flow calculations and failed-attempt analysis from `RecordingAccount`, adapting existing records into transaction-specific entries without modifying the banking logic.

All twelve Visitor tests passed. The demonstration reported a £10 net increase consistent with the account balance, but the failure-injection test exposed a less reassuring outcome. A completed £25 deposit was absent from the records, leaving `CashFlowVisitor` reporting no movement. Its calculation was accurate, although its account of the transaction was incomplete.

A balance can reconcile even when the transaction history is incomplete. For example, an unrecorded £25 deposit and an equally unrecorded withdrawal would leave the net movement unchanged, although neither transaction could be traced during a customer dispute or investigation. `FailedAttemptVisitor` faces a similar limitation because rejected operations missing from the records cannot appear in its report. I would therefore treat balance reconciliation as a useful check for discrepancies, without assuming that matching figures establish a complete transaction history.

Visitor also introduces costs that deserve scrutiny. Adding a refund would require extending the entry types, visitor interface and reporting implementations. The current design rejects unknown operations, preventing them from being silently included in misleading totals, although it also makes extension more demanding.

I would retain Visitor where independent reporting requirements justify these dependencies, but strengthen transaction capture before expanding the reports. Unique transaction identifiers, coordinated recording and reconciliation against authoritative records would offer greater assurance than adding further analytical visitors to an incomplete history.

## Evidence

- [Visitor implementation](transaction_visitors.py)
- [Twelve Visitor tests](test_transaction_visitors.py)
- [Decorator failure-mode tests](test_recording_failure_modes.py)
- [Transaction recording implementation](recording_account.py)
