# Mocking AI Dependencies and the Limits of Test Assurance

The recording failures identified earlier raised a difficult question about introducing AI when the evidence reaching it was already incomplete. `ModelReviewService` was developed to keep model suggestions separate from financial verification. It reuses the Visitor reports and accepts a replaceable `ReviewModel` dependency, allowing the surrounding logic to be tested with `unittest.mock` rather than a trained model or external API.

Nine tests passed, followed at this stage by 65 banking regression tests in 0.037 seconds. A missing £25 deposit triggered manual review before the model was consulted. Invalid responses and expected model failures were also directed to manual review, while unexpected exceptions remained visible. These results demonstrate controlled failure handling, but only for the behaviours exercised.

The more revealing test forced recording to fail after a £25 deposit and an equal withdrawal. Both operations completed, yet the account returned to £100 with no records. Reconciliation therefore passed and the mock returned `no_flag`, although the service labelled it advisory rather than approved. An inactive account and one containing two unrecorded, opposing transactions had become indistinguishable to the model.

Barr et al. (2015) examine the difficulty of selecting adequate test oracles. The passing assertion in this case confirmed a predicted weakness, not dependable financial review. AI assistance helped develop the offsetting-transaction scenario, but generated tests still required verification against the implementation. Shang et al. (2025) examine both the potential and limitations of LLM-based unit testing. No coverage or defect-detection study was reported here, so the passing suite cannot establish its ability to expose other defects.

Mocking also leaves important boundaries untested. `Mock(spec=ReviewModel)` does not fully enforce method signatures, the service cannot guarantee consistent balance-and-record snapshots, and `manual_review` has no operational process behind it. The NIST AI Risk Management Framework places model reliability and accountability within wider governance and evaluation (Tabassi, 2023). Until transaction-level evidence can be independently verified, a more capable model would inherit the same information gaps.

## Evidence

- [Model review implementation](../02-Coding-Exercises/BankAccount/model_review.py)
- [Nine model-review tests](../02-Coding-Exercises/BankAccount/test_model_review.py)
- [Visitor implementation](../02-Coding-Exercises/BankAccount/transaction_visitors.py)

## References

Barr, E.T., Harman, M., McMinn, P., Shahbaz, M. and Yoo, S. (2015) ‘The oracle problem in software testing: A survey’, *IEEE Transactions on Software Engineering*, 41(5), pp. 507–525. Available at https://doi.org/10.1109/TSE.2014.2372785 (Accessed 14 October 2026).

Shang, Y., Zhang, Q., Fang, C., Gu, S., Zhou, J. and Chen, Z. (2025) ‘A large-scale empirical study on fine-tuning large language models for unit testing’, *Proceedings of the ACM on Software Engineering*, 2(ISSTA), pp. 1678–1700. Available at https://doi.org/10.1145/3728951 (Accessed 14 October 2026).

Tabassi, E. (2023) *Artificial Intelligence Risk Management Framework (AI RMF 1.0)*. NIST AI 100-1. National Institute of Standards and Technology. Available at https://doi.org/10.6028/NIST.AI.100-1 (Accessed 14 October 2026).
