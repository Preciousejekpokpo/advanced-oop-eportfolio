# Task 3 Academic and Employability Skills

The lecturer's feedback gave my independent study a clearer direction. I [mapped banking requirements to tests](../02-Coding-Exercises/BankAccount/REQUIREMENTS_AND_TEST_EVIDENCE.md) and [investigated lock contention](../02-Coding-Exercises/BankAccount/CONTENTION_EVALUATION.md). The mapping exposed gaps involving worker-thread exceptions, while five trials per benchmark configuration showed no sustained performance advantage for separate locks. Kalibera and Jones (2013) helped me interpret variability without selecting favourable results. This strengthened my research judgement and ability to explain what evidence supports, and what it cannot.

The [checkout exercise](../02-Coding-Exercises/SOLID-Checkout/README.md) developed my problem-solving differently. Six passing tests missed a fractional-penny error, which a boundary test exposed and explicit rounding corrected. Tracing the failure and documenting the change improved how I debug and explain technical decisions.

Writing the design-pattern evaluations developed a more demanding approach to technical communication. I had to connect design decisions to test evidence, distinguish demonstrated behaviour from proposed safeguards and explain failure conditions that successful tests could obscure. These skills are relevant to software assurance and application security, where risk assessments and deployment decisions depend on defensible evidence rather than confidence in an implementation. The AI review raised a related ethical concern. Mocked responses exercised selected service decisions but established neither fairness nor reliable live-model advice. Tabassi (2023) reinforced the importance of communicating such uncertainty through human oversight, auditability and accountable evaluation.

Working independently through lecturecasts, research and unfamiliar problems developed my persistence and self-management. I also noticed that documenting decisions after implementation reduced the time available for review. Recording assumptions alongside tests and seeking technical feedback earlier would improve my time management and make my work easier for others to scrutinise. Collaborative practice remains a development goal rather than a skill this individual project independently demonstrates.

## References

Kalibera, T. and Jones, R.E. (2013) ‘Rigorous benchmarking in reasonable time’, *Proceedings of the ACM SIGPLAN International Symposium on Memory Management*. Available at https://doi.org/10.1145/2464157.2464160 (Accessed 14 October 2026).

Tabassi, E. (2023) *Artificial Intelligence Risk Management Framework (AI RMF 1.0)*. NIST AI 100-1. National Institute of Standards and Technology. Available at https://doi.org/10.6028/NIST.AI.100-1 (Accessed 14 October 2026).
