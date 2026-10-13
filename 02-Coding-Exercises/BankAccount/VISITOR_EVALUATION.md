# Visitor and the Reliability of Financial Reporting

The Decorator tests exposed a gap between what happened to an account and what its transaction history could explain. I wanted to examine that history in different ways without adding reporting responsibilities to `RecordingAccount`. Visitor offered this separation, following the approach described by Gamma et al. (1994). `CashFlowVisitor` calculates financial movements, while `FailedAttemptVisitor` identifies rejected transactions. Both analyse the records supplied to them, although neither can account for transactions that were never recorded.

All twelve Visitor tests passed, and the demonstration produced a £10 net increase consistent with the account balance. The more revealing result came from revisiting the Decorator failure. A £25 deposit reached the account but never entered its transaction history. `CashFlowVisitor` reported no movement because the available records contained none. Comparing that report with the actual balance exposed the discrepancy, but the visitor had no evidence from which to explain the missing deposit.

Wang and Strong (1996) examine data quality from the perspective of those who use the information. Their emphasis on data quality in the context of its intended use raises a more demanding question about my tests. A correct net total may be adequate for measuring balance movement, but it offers limited assurance when someone needs to investigate an individual transaction. The missing £25 deposit was detectable because the reported and actual figures differed. Two unrecorded movements of equal and opposite value could leave those figures matching, concealing both omissions. Although I did not test that scenario, the transfer test exposed a related weakness. The destination balance increased without a corresponding entry in its own history. Agreement between totals could therefore conceal gaps in the underlying evidence.

The design brings its own compromises. Adding another report would leave the existing transaction entries largely unchanged, but introducing a refund would require changes to the entry mapping, visitor interface and reporting classes. Rejecting unknown operations is useful because unsupported transaction types cannot silently enter the calculations. Yet that safeguard offers little protection when an operation leaves no record at all. With only two reports, the additional interfaces and entry classes are also harder to justify when simpler functions could perform the same calculations.

I would retain Visitor if reporting requirements expanded while transaction types remained relatively stable. For now, the more pressing issue is establishing whether the records represent every completed operation. I would prioritise tests that reconcile individual transactions against an independent source before extending the reporting functions. Another report built on the same incomplete history would offer a different calculation, but little additional confidence in what actually happened.

## Evidence

- [Visitor implementation](transaction_visitors.py)
- [Twelve Visitor tests](test_transaction_visitors.py)
- [Decorator failure-mode tests](test_recording_failure_modes.py)
- [Transaction recording implementation](recording_account.py)

## References

Gamma, E., Helm, R., Johnson, R. and Vlissides, J. (1994) *Design Patterns: Elements of Reusable Object-Oriented Software*. 1st edn. Addison-Wesley Professional. Available at: https://www.pearson.com/en-gb/subject-catalog/p/design-patterns-elements-of-reusable-object-oriented-software/P200000009480/9780201633610 (Accessed: 14 October 2026).

Wang, R.Y. and Strong, D.M. (1996) ‘Beyond accuracy: What data quality means to data consumers’, *Journal of Management Information Systems*, 12(4), pp. 5–33. Available at: https://doi.org/10.1080/07421222.1996.11518099 (Accessed: 14 October 2026).
