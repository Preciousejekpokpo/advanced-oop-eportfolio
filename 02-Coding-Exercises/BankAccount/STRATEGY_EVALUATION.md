# Visitor and the Reliability of Financial Reporting

Decorator made transaction records available, but reporting still risked becoming coupled to recording. I used `CashFlowVisitor` and `FailedAttemptVisitor` to analyse the same snapshot without changing account operations (Gamma et al., 1994). Twelve tests passed, covering withdrawals, dispatch and snapshot behaviour.

After `_append()` failed following a £25 deposit, the cash-flow report showed no movement although the balance increased. The test exposed a discrepancy, not the missing event. A £15 transfer also increased the destination balance without appearing in its report. Wang and Strong (1996) examine data quality in relation to its use. These reports calculated available records correctly without establishing completeness. Later model-review tests showed that opposing missing movements could cancel and pass reconciliation.

`TransactionRecord` lacks `accept()`, requiring entry adapters and dispatch. A new operation such as a refund would need changes across visitors, and ordinary functions might suffice for only two reports. Using one record snapshot supports consistent reporting between visitors, but the snapshot is not atomic with account balances. I would retain Visitor for expanding report types while treating its results as dependent on unverified transaction evidence.

## Evidence

- [Visitor implementation](transaction_visitors.py)
- [Twelve Visitor tests](test_transaction_visitors.py)
- [Decorator failure-mode tests](test_recording_failure_modes.py)
- [Later model-review tests](test_model_review.py)

## References

Gamma, E., Helm, R., Johnson, R. and Vlissides, J. (1994) *Design Patterns: Elements of Reusable Object-Oriented Software*. 1st edn. Addison-Wesley Professional. Available at https://www.pearson.com/en-gb/subject-catalog/p/design-patterns-elements-of-reusable-object-oriented-software/P200000009480/9780201633610 (Accessed 14 October 2026).

Wang, R.Y. and Strong, D.M. (1996) ‘Beyond accuracy: What data quality means to data consumers’, *Journal of Management Information Systems*, 12(4), pp. 5–33. Available at https://doi.org/10.1080/07421222.1996.11518099 (Accessed 14 October 2026).
