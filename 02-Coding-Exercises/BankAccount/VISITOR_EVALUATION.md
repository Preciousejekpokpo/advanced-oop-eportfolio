# Visitor and the Reliability of Financial Reporting

The Decorator tests exposed a gap between what happened to an account and what its transaction history could explain. I wanted to examine that history in different ways without adding reporting responsibilities to `RecordingAccount`. Visitor provided this separation (Gamma et al., 1994). `CashFlowVisitor` calculates financial movement and `FailedAttemptVisitor` identifies recorded rejections, but both depend on the history available.

All twelve Visitor tests passed, and the demonstration produced a £10 net increase matching the account balance. Revisiting the Decorator failure was more revealing: a £25 deposit reached the account without entering its history, so `CashFlowVisitor` reported no movement. Comparing the report with the balance exposed the discrepancy without explaining the missing transaction.

Wang and Strong (1996) examine data quality in relation to its intended use, prompting me to question what an accurate total establishes. Net movement may summarise recorded activity, but cannot reliably explain individual transactions. Two missing movements of equal and opposite value could also leave the totals matching. I had not tested this at the Visitor stage, although later model-review tests confirmed it. The transfer test revealed another gap: the destination balance increased without an entry in its history.

Visitor also brings a maintenance cost. New reports leave existing entry types largely unchanged, but a refund would require changes to the entry mapping, visitor interface and reporting classes. Rejecting unknown operations prevents unsupported records entering calculations, not absent transactions. Since `TransactionRecord` lacks `accept()`, separate entry classes are needed for dispatch. With only two reports, the additional abstraction is difficult to justify when simpler functions could achieve the same results. Both visitors can analyse one record snapshot, but it is not captured atomically with the account balance.

I would retain Visitor if reporting requirements expanded while transaction types remained stable. I would prioritise transaction-level reconciliation against an independent source before extending reporting, since additional calculations cannot establish the completeness of the underlying records.

## Evidence

- [Visitor implementation](transaction_visitors.py)
- [Twelve Visitor tests](test_transaction_visitors.py)
- [Decorator failure-mode tests](test_recording_failure_modes.py)
- [Later model-review tests](test_model_review.py)

## References

Gamma, E., Helm, R., Johnson, R. and Vlissides, J. (1994) *Design Patterns: Elements of Reusable Object-Oriented Software*. 1st edn. Addison-Wesley Professional. Available at: https://www.pearson.com/en-gb/subject-catalog/p/design-patterns-elements-of-reusable-object-oriented-software/P200000009480/9780201633610 (Accessed: 14 October 2026).

Wang, R.Y. and Strong, D.M. (1996) ‘Beyond accuracy: What data quality means to data consumers’, *Journal of Management Information Systems*, 12(4), pp. 5–33. Available at: https://doi.org/10.1080/07421222.1996.11518099 (Accessed: 14 October 2026).
