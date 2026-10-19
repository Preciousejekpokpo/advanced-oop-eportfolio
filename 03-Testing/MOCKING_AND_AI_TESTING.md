
# Mocking AI Dependencies and the Limits of Test Assurance

The recording failures raised a further question about introducing model-assisted review when the transaction history itself could be incomplete. I developed `ModelReviewService` around an injected `ReviewModel`, using `unittest.mock` to test its behaviour without contacting a live model. Nine tests passed, covering reconciliation, invalid responses and dependency failures.

A £25 deposit and matching withdrawal both completed without being recorded, leaving the balance at £100. Reconciliation passed, and the mock returned `no_flag`, which the service treated as `advisory_only`. Although this prevented model advice from becoming an approval decision, the service could not distinguish inactivity from missing transactions. More importantly, `ReviewFacts` supplied only net movement and counts of recorded and failed attempts. Even a capable model would have little basis for identifying transactions absent from those figures. Barr et al. (2015) examine the test-oracle problem, which helped explain why my assertions could pass while the evidence they assessed remained inadequate.

Other tests confirmed that detectable discrepancies prevented model consultation, while invalid responses and expected outages prompted `manual_review`. Unexpected exceptions remained visible. These controls improved how the service handled uncertainty, although a manual-review status does not demonstrate that an effective human review process exists. Mocked responses also provided no evidence of live-model accuracy or fairness, concerns reflected in the wider evaluation requirements of Tabassi (2023).

Shang et al. (2025) examine language models for unit testing, prompting me to consider AI-assisted test generation, less obvious edge-case discovery and regression support. Generating cases involving cancelling transactions or altered record amounts could help challenge assumptions, although I did not evaluate AI-generated tests. A generated assertion could repeat my original assumption that matching totals establish complete records, while regression testing would preserve that weakness across later changes. I would first strengthen transaction-level verification, then examine whether AI assistance identifies failures that deliberately designed tests have missed.

## Evidence

- [Model review implementation](../02-Coding-Exercises/BankAccount/model_review.py)
- [Nine model-review tests](../02-Coding-Exercises/BankAccount/test_model_review.py)
- [Visitor implementation](../02-Coding-Exercises/BankAccount/transaction_visitors.py)

## References

Barr, E.T., Harman, M., McMinn, P., Shahbaz, M. and Yoo, S. (2015) ‘The oracle problem in software testing: A survey’, *IEEE Transactions on Software Engineering*, 41(5), pp. 507–525. Available at https://doi.org/10.1109/TSE.2014.2372785 (Accessed 14 October 2026).

Shang, Y., Zhang, Q., Fang, C., Gu, S., Zhou, J. and Chen, Z. (2025) ‘A large-scale empirical study on fine-tuning large language models for unit testing’, *Proceedings of the ACM on Software Engineering*, 2(ISSTA), pp. 1678–1700. Available at https://doi.org/10.1145/3728951 (Accessed 14 October 2026).

Tabassi, E. (2023) *Artificial Intelligence Risk Management Framework (AI RMF 1.0)*. NIST AI 100-1. National Institute of Standards and Technology. Available at https://doi.org/10.6028/NIST.AI.100-1 (Accessed 14 October 2026).
