# Mocking AI Dependencies and the Limits of Test Assurance

The recording failures raised a further question about introducing model-assisted review when the transaction history itself could be incomplete. `ModelReviewService` was developed to verify recorded movements before requesting advice through a replaceable `ReviewModel` interface. This allowed the review logic to be tested using `unittest.mock`, without relying on a trained model or external API.

Nine tests passed, covering financial reconciliation, invalid model responses, dependency failures and unexpected exceptions. A missing £25 deposit correctly triggered manual review before the model was consulted. However, a later test exposed a limitation in that safeguard. When an unrecorded £25 deposit was followed by an equally unrecorded withdrawal, the balance returned to £100 with no transaction history. Reconciliation passed and the mock returned `no_flag`. Although the service treated this as advisory rather than approval, it could not distinguish an inactive account from one containing unrecorded activity.

Barr et al. (2015) examine the difficulty of establishing adequate test oracles. Here, a passing test demonstrated a weakness in verification rather than dependable financial assurance. The scenario also illustrates a challenge for AI-assisted test generation. Suggested edge cases can broaden testing, but their assertions still require examination against the intended behaviour. Shang et al. (2025) investigate LLM-based unit testing, although this project did not measure coverage or defect-detection effectiveness.

Mocking established how the service responded to controlled inputs, but could not assess model accuracy, fairness or explainability. `Mock(spec=ReviewModel)` also provides limited signature checking, while balance and record snapshots lack an atomic boundary. These limitations matter because the NIST AI Risk Management Framework places reliability and accountability within wider governance and evaluation (Tabassi, 2023). Before introducing a live model, I would prioritise independently verifiable transaction evidence and a defined human review process.

## Evidence

- [Model review implementation](../02-Coding-Exercises/BankAccount/model_review.py)
- [Nine model-review tests](../02-Coding-Exercises/BankAccount/test_model_review.py)
- [Visitor implementation](../02-Coding-Exercises/BankAccount/transaction_visitors.py)

## References

Barr, E.T., Harman, M., McMinn, P., Shahbaz, M. and Yoo, S. (2015) ‘The oracle problem in software testing: A survey’, *IEEE Transactions on Software Engineering*, 41(5), pp. 507–525. Available at https://doi.org/10.1109/TSE.2014.2372785 (Accessed 14 October 2026).

Shang, Y., Zhang, Q., Fang, C., Gu, S., Zhou, J. and Chen, Z. (2025) ‘A large-scale empirical study on fine-tuning large language models for unit testing’, *Proceedings of the ACM on Software Engineering*, 2(ISSTA), pp. 1678–1700. Available at https://doi.org/10.1145/3728951 (Accessed 14 October 2026).

Tabassi, E. (2023) *Artificial Intelligence Risk Management Framework (AI RMF 1.0)*. NIST AI 100-1. National Institute of Standards and Technology. Available at https://doi.org/10.6028/NIST.AI.100-1 (Accessed 14 October 2026).
