# Mocking AI Dependencies and the Limits of Test Assurance

The recording failures identified in the earlier exercises raised a difficult question about introducing AI into an application whose transaction evidence was already imperfect. I developed `ModelReviewService` to explore how model advice could be accommodated without giving it authority over financial verification. The service reuses the existing Visitor reports, while `ReviewModel` provides an interface that can be replaced with a mock. This allowed me to test the surrounding software without connecting to a trained model or external API.

All nine new tests passed, followed by a full regression run of 65 tests in 0.037 seconds, with no reported failures. Using `unittest.mock`, I controlled the model's responses, simulated recording and dependency failures, and checked when the model was consulted. An unrecorded £25 deposit triggered manual review without a model call. Invalid responses and a defined model failure also led to manual review, while unexpected exceptions remained visible. These results support the behaviour tested, although the regression run cannot establish correctness beyond the scenarios covered.

The strongest finding emerged when I forced recording to fail after a £25 deposit and a £25 withdrawal. Both balance operations completed, but neither transaction entered the history. The account returned to its opening balance of £100, allowing the reconciliation check to pass. The service then returned the mocked `no_flag` suggestion as advisory output. This exposed a limitation more significant than an incorrectly classified transaction. An account with no activity could produce the same summary figures as one containing two unrecorded, opposing movements. The model could not distinguish those histories from the supplied inputs.

Barr et al. (2015) examine the difficulty of establishing appropriate test oracles. Their analysis gives this result a wider significance. My assertions passed because the software behaved as expected, including when the test was designed to expose a weakness. Success therefore confirmed the predicted limitation rather than establishing the reliability of the review process. The experiment also changed where I would concentrate further testing. Improving the model's responses would offer limited assurance while different transaction histories remained indistinguishable in the evidence reaching it.

AI assistance contributed to generating and refining the test scenarios, particularly the offsetting-transactions case. Shang et al. (2025) demonstrate the potential of LLMs across several unit-testing tasks while examining concerns around benchmark leakage and defect detection. Their findings make it difficult to equate generated tests with reliable verification. In my exercise, the proposed scenarios still needed to be checked against the actual implementation and expressed through meaningful assertions. The completed suite can be rerun for regression testing, but I have not measured coverage or its effectiveness in detecting newly introduced defects.

The design remains limited in several ways. `Mock(spec=ReviewModel)` restricts access to the expected interface without fully checking method signatures. The service assumes that its balances and records describe a completed workload, although it does not enforce how those snapshots are collected. Its `manual_review` result also stops at signalling a problem, with no operational review process behind it. Tabassi (2023) places AI evaluation within a wider context of reliability, accountability and risk management. That is relevant here because testing an interface cannot establish whether a future model would be accurate, fair or explainable. I would prioritise transaction-level recording and independent verification before introducing such a model. Until the evidence improves, a more capable model would still be working within the same informational limits.

## Evidence

- [Model review implementation](../02-Coding-Exercises/BankAccount/model_review.py)
- [Nine mocking tests](../02-Coding-Exercises/BankAccount/test_model_review.py)
- [Visitor implementation](../02-Coding-Exercises/BankAccount/transaction_visitors.py)
- [Decorator failure-mode tests](../02-Coding-Exercises/BankAccount/test_recording_failure_modes.py)

## Testing results

- Model review tests completed with 9 tests passing.
- Full banking regression suite completed with 65 tests passing in 0.037 seconds.
- Both results were reported from local execution on 14 October 2026.
- No live AI model or external API was evaluated.

## References

Barr, E.T., Harman, M., McMinn, P., Shahbaz, M. and Yoo, S. (2015) ‘The oracle problem in software testing: A survey’, *IEEE Transactions on Software Engineering*, 41(5), pp. 507–525. Available at: https://doi.org/10.1109/TSE.2014.2372785 (Accessed: 14 October 2026).

Shang, Y., Zhang, Q., Fang, C., Gu, S., Zhou, J. and Chen, Z. (2025) ‘A large-scale empirical study on fine-tuning large language models for unit testing’, *Proceedings of the ACM on Software Engineering*, 2(ISSTA), pp. 1678–1700. Available at: https://doi.org/10.1145/3728951 (Accessed: 14 October 2026).

Tabassi, E. (2023) *Artificial Intelligence Risk Management Framework (AI RMF 1.0)*. NIST AI 100-1. National Institute of Standards and Technology. Available at: https://doi.org/10.6028/NIST.AI.100-1 (Accessed: 14 October 2026).
