# Mocking AI Dependencies and the Limits of Test Assurance

The recording failures raised a further question about introducing model-assisted review when the transaction history itself could be incomplete. `ModelReviewService` was developed to verify recorded movements before requesting advice through a replaceable `ReviewModel` interface. Using `unittest.mock` allowed me to examine its decisions without claiming to test a live model.

Nine tests passed, yet one exposed how easily a correct response could rest on weak evidence. An unrecorded £25 deposit and withdrawal cancelled out, leaving the balance at £100 and the history empty. Reconciliation passed, the mock returned `no_flag`, and the service labelled it `advisory_only`. That safeguard avoided approval, but could not distinguish an inactive account from unrecorded activity. Barr et al. (2015) examine the test oracle problem, which matters here because my assertions verified the rules I had written, including their blind spots.

The other tests demonstrated useful controls. A detectable mismatch stopped model consultation, invalid outputs and expected model failures prompted manual review, while unexpected exceptions remained visible. However, `Mock(spec=ReviewModel)` does not fully enforce method signatures, and scripted responses cannot establish how a real model would behave. Shang et al. (2025) examine LLM-based testing, but I did not measure generated-test quality or defect detection. NIST's AI RMF (Tabassi, 2023) also places reliability within broader evaluation and oversight, neither of which my mocks established.

I would address the recording boundary before expanding the AI layer, prioritising coordinated balance-and-record updates, recovery testing and a defined human review process. More passing mock tests would offer limited assurance while the evidence they depend on remains incomplete.

## Evidence

- [Model review implementation](../02-Coding-Exercises/BankAccount/model_review.py)
- [Nine model-review tests](../02-Coding-Exercises/BankAccount/test_model_review.py)
- [Visitor implementation](../02-Coding-Exercises/BankAccount/transaction_visitors.py)

## References

Barr, E.T., Harman, M., McMinn, P., Shahbaz, M. and Yoo, S. (2015) ‘The oracle problem in software testing: A survey’, *IEEE Transactions on Software Engineering*, 41(5), pp. 507–525. Available at https://doi.org/10.1109/TSE.2014.2372785 (Accessed 14 October 2026).

Shang, Y., Zhang, Q., Fang, C., Gu, S., Zhou, J. and Chen, Z. (2025) ‘A large-scale empirical study on fine-tuning large language models for unit testing’, *Proceedings of the ACM on Software Engineering*, 2(ISSTA), pp. 1678–1700. Available at https://doi.org/10.1145/3728951 (Accessed 14 October 2026).

Tabassi, E. (2023) *Artificial Intelligence Risk Management Framework (AI RMF 1.0)*. NIST AI 100-1. National Institute of Standards and Technology. Available at https://doi.org/10.6028/NIST.AI.100-1 (Accessed 14 October 2026).
