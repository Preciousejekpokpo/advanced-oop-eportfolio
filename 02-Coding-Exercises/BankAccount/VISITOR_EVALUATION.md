# Visitor and the Reliability of Financial Reporting

Decorator made it possible to record transactions without changing account logic, but its failure tests left a more troubling question. How reliable are reports built from records that may be incomplete? I introduced Visitor so `CashFlowVisitor` and `FailedAttemptVisitor` could analyse the same snapshot without moving reporting into `RecordingAccount` (Gamma et al., 1994).

All twelve tests passed, yet the failure cases exposed the limits of that success. When a £25 deposit completed but recording failed, the visitor reported no movement, while the balance had increased. The comparison detected a discrepancy without revealing the missing operation. A transfer created a similar blind spot, increasing the destination balance by £15 without adding a destination record. Wang and Strong (1996) examine data quality in relation to its intended use, which matters here because correct arithmetic cannot establish that a record set is complete. Two missing movements that cancel could even make reconciliation appear successful, a limitation confirmed in later model-review tests rather than the Visitor tests themselves.

The design also introduces a maintenance trade-off. Because `TransactionRecord` lacks `accept()`, I needed entry adapters and explicit dispatch, while supporting refunds would require changes across the visitor interface and implementations. With only two reports, functions would have been simpler, and the shared snapshot is still not atomic with the account balance. I would retain Visitor if reporting requirements expanded, but its calculations cannot substitute for independently verified records.

## Evidence

- [Visitor implementation](transaction_visitors.py)
- [Twelve Visitor tests](test_transaction_visitors.py)
- [Decorator failure-mode tests](test_recording_failure_modes.py)
- [Later model-review tests](test_model_review.py)

## References

Gamma, E., Helm, R., Johnson, R. and Vlissides, J. (1994) *Design Patterns: Elements of Reusable Object-Oriented Software*. 1st edn. Addison-Wesley Professional. Available at https://www.pearson.com/en-gb/subject-catalog/p/design-patterns-elements-of-reusable-object-oriented-software/P200000009480/9780201633610 (Accessed 14 October 2026).

Wang, R.Y. and Strong, D.M. (1996) ‘Beyond accuracy: What data quality means to data consumers’, *Journal of Management Information Systems*, 12(4), pp. 5–33. Available at https://doi.org/10.1080/07421222.1996.11518099 (Accessed 14 October 2026).
