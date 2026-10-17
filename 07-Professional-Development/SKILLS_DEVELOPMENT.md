# Task 3 Academic and Employability Skills

The lecturer's feedback gave my independent study a clearer direction. [Mapping banking requirements to tests](../02-Coding-Exercises/BankAccount/REQUIREMENTS_AND_TEST_EVIDENCE.md) exposed gaps involving worker-thread exceptions, while the [contention investigation](../02-Coding-Exercises/BankAccount/CONTENTION_EVALUATION.md) challenged my expectation that separate account locks would improve throughput. Five repetitions per configuration showed no consistent advantage. Kalibera and Jones (2013) helped me interpret variation rather than favour results that supported my initial assumption. This made me more careful about distinguishing correct concurrent behaviour from claims of scalability.

The [checkout exercise](../02-Coding-Exercises/SOLID-Checkout/README.md) presented a smaller but revealing problem. Six passing tests overlooked a fractional-penny error until a boundary case exposed it. Correcting the rounding was easier than recognising why my tests had missed it, and made me question coverage rather than rely on test counts.

Writing the design-pattern evaluations strengthened my ability to explain technical decisions and their consequences. When the Decorator completed a £25 deposit but failed to record it, I had to distinguish a correct balance from a verifiable transaction. Documenting reproducible failures and untested remedies made my analysis more useful to someone scrutinising the design, an important skill in application security and software assurance.

The [AI review](../03-Testing/MOCKING_AND_AI_TESTING.md) raised a related ethical concern. Mocked tests examined service behaviour, not model fairness, explainability or live accuracy. Similarly, returning `manual_review` does not establish that anyone has sufficient evidence or authority to act. Tabassi (2023) reinforced the importance of evaluating oversight rather than assuming it exists.

Working independently through lecturecasts and research strengthened my persistence, although documenting decisions late reduced the time available for critical review. Recording assumptions alongside tests and seeking feedback earlier would improve my planning and make my work easier to scrutinise. Collaborative delivery remains a development goal rather than an achievement this individual project demonstrates.

## References

Kalibera, T. and Jones, R.E. (2013) ‘Rigorous benchmarking in reasonable time’, *Proceedings of the ACM SIGPLAN International Symposium on Memory Management*. Available at https://doi.org/10.1145/2464157.2464160 (Accessed 14 October 2026).

Tabassi, E. (2023) *Artificial Intelligence Risk Management Framework (AI RMF 1.0)*. NIST AI 100-1. National Institute of Standards and Technology. Available at https://doi.org/10.6028/NIST.AI.100-1 (Accessed 14 October 2026).
