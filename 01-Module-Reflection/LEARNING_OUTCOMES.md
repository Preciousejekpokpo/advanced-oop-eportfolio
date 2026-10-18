# Task 1 Learning Outcomes

The original banking task gave me a practical way to examine encapsulation and secure coding. `BankAccount` validates amounts using `Decimal`, protects balance changes with account-level locks and acquires transfer locks consistently. Twelve tests supported its behaviour under the tested conditions. However, the [requirements map](../02-Coding-Exercises/BankAccount/REQUIREMENTS_AND_TEST_EVIDENCE.md) exposed mutable account identifiers and worker exceptions that the original tests could miss. A protected balance was only part of what reliable operation required.

The lecturer's feedback on traceability and scalability prompted a [contention investigation](../02-Coding-Exercises/BankAccount/CONTENTION_EVALUATION.md). Across sixty trials, separate accounts showed no sustained throughput advantage despite correct final balances. This helped me distinguish concurrency correctness from performance claims, particularly given the restricted workload and alpha Python environment.

In the [Unit 2 SOLID checkout](../02-Coding-Exercises/SOLID-Checkout/README.md), separating payment from order calculation allowed mocked testing, but six passing tests missed a fractional-penny error. A new boundary test and rounding correction demonstrated that clearer responsibilities improve testability without ensuring the right cases have been examined. It also strengthened my preference for targeted refactoring over adding classes without a demonstrated need.

The four pattern extensions exposed related trade-offs. [Strategy](../02-Coding-Exercises/BankAccount/STRATEGY_EVALUATION.md) enabled interchangeable workloads, [Decorator](../02-Coding-Exercises/BankAccount/DECORATOR_EVALUATION.md) added transaction recording, [Visitor](../02-Coding-Exercises/BankAccount/VISITOR_EVALUATION.md) separated reporting and [Abstract Factory](../02-Coding-Exercises/BankAccount/ABSTRACT_FACTORY_EVALUATION.md) assembled compatible scenarios. Yet a failed record write left a completed deposit without evidence. Prechelt et al. (2001) found maintenance benefits for patterns in most examined tasks, but those findings cannot establish financial consistency in this implementation.

Unit 9's architecture case study made me question whether distributing responsibilities could improve reliability without coordinating updates and recovery. The [capstone](../05-Capstone-Project/CAPSTONE_EVALUATION.md) caught missing records that reconciliation overlooked, but substituted amounts still passed its record-count check. Barr et al. (2015) helped frame this as a test-oracle limitation. The [model-review tests](../03-Testing/MOCKING_AND_AI_TESTING.md) used dependency injection to examine nine mocked decisions, not live-model accuracy. Visitor supported aggregate financial analysis, but I did not evaluate efficiency in data-science workloads. Model Registry and Feature Store remained concepts for managing models and features, not implemented components. Tabassi (2023) reinforced the importance of trustworthy inputs and oversight.

![Feedback and development evidence map](Feedback%20and%20development%20evidence%20map.png)

*Figure 1 connects the five learning outcomes with module study, lecturer feedback and tested artefacts. It distinguishes implemented evidence from conceptual learning and proposed safeguards.*

## References

Barr, E.T., Harman, M., McMinn, P., Shahbaz, M. and Yoo, S. (2015) ‘The oracle problem in software testing: A survey’, *IEEE Transactions on Software Engineering*, 41(5), pp. 507–525. Available at https://doi.org/10.1109/TSE.2014.2372785 (Accessed 16 October 2026).

Prechelt, L., Unger, B., Tichy, W.F., Brössler, P. and Votta, L.G. (2001) ‘A controlled experiment in maintenance: Comparing design patterns to simpler solutions’, *IEEE Transactions on Software Engineering*, 27(12), pp. 1134–1144. Available at https://doi.org/10.1109/32.988711 (Accessed 16 October 2026).

Tabassi, E. (2023) *Artificial Intelligence Risk Management Framework (AI RMF 1.0)*. NIST AI 100-1. National Institute of Standards and Technology. Available at https://doi.org/10.6028/NIST.AI.100-1 (Accessed 16 October 2026).
