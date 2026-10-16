# Visitor and the Reliability of Financial Reporting

I used Visitor to analyse records without putting reporting inside `RecordingAccount`. `CashFlowVisitor` totals financial movements, while `FailedAttemptVisitor` gathers unsuccessful operations from the same snapshot (Gamma et al., 1994). Twelve tests passed, including checks of dispatch and snapshot behaviour.

One failure test raised a concern about how much those reports could tell me. After `_append()` failed following a £25 deposit, the balance increased while the report showed no movement. A £15 transfer also reached the destination account without appearing in its history. The calculations were correct, but the records were incomplete. Wang and Strong (1996) examine data quality in relation to its intended use. That distinction matters here because financial reports need to reflect transactions that actually occurred. Later model-review tests showed a further weakness when opposing missing movements cancelled out and reconciliation still passed.

Visitor also introduced more complexity than the two reports initially required. Since `TransactionRecord` has no `accept()` method, I needed adapters and explicit dispatch. Supporting refunds would require changes across several components, while ordinary functions might be easier to maintain at this scale. Using one snapshot allows both reports to examine the same entries, but cannot establish whether those entries fully reflect the account balance. I would retain Visitor if reporting requirements expanded, although I would first address the reliability of the records it depends on.

## Evidence

- [Visitor implementation](transaction_visitors.py)
- [Twelve Visitor tests](test_transaction_visitors.py)
- [Decorator failure-mode tests](test_recording_failure_modes.py)
- [Later model-review tests](test_model_review.py)

## References

Gamma, E., Helm, R., Johnson, R. and Vlissides, J. (1994) *Design Patterns: Elements of Reusable Object-Oriented Software*. 1st edn. Addison-Wesley Professional. Available at https://www.pearson.com/en-gb/subject-catalog/p/design-patterns-elements-of-reusable-object-oriented-software/P200000009480/9780201633610 (Accessed 14 October 2026).

Wang, R.Y. and Strong, D.M. (1996) ‘Beyond accuracy: What data quality means to data consumers’, *Journal of Management Information Systems*, 12(4), pp. 5–33. Available at https://doi.org/10.1080/07421222.1996.11518099 (Accessed 14 October 2026).
