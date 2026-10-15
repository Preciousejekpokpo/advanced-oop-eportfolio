# Task 3 Academic and Employability Skills

My banking submission provided a practical foundation in concurrent programming, particularly protecting shared balances and preventing deadlocks. The lecturer's feedback encouraged me to examine how well these decisions were supported by testing and whether their benefits extended to scalability. Building on the original implementation, I independently [mapped requirements to tests](../02-Coding-Exercises/BankAccount/REQUIREMENTS_AND_TEST_EVIDENCE.md) and [investigated lock contention](../02-Coding-Exercises/BankAccount/CONTENTION_EVALUATION.md). Although the balances remained correct, separate account locks showed no sustained performance advantage. Kalibera and Jones (2013) helped me interpret the variation across five trials per configuration. This strengthened my ability to evaluate technical results within their experimental limits, while recognising that a design can be effective for correctness without demonstrating improved performance.

The [checkout exercise](../02-Coding-Exercises/SOLID-Checkout/README.md) tested my problem-solving differently. Six passing tests had overlooked a fractional-penny error, which an additional boundary test exposed. Correcting it reinforced the value of questioning apparently successful results and persisting when the evidence challenged my expectations.

The AI ethics material extended that judgement into professional responsibility. Tabassi (2023) places trustworthy AI within governance and evaluation, while my mocked tests could establish neither fairness nor explainability. I would expect reliable input evidence, human oversight and reviewable decisions before supporting consequential applications.

Developing and documenting the portfolio independently strengthened my research, self-study and technical communication. It also exposed a weakness in how I managed the work. Documentation often followed implementation, leaving less time for critical review. Although revisiting tests and earlier decisions improved my ability to evaluate my work, collaborative practice remains less developed. Without assessed group activities or peer reviews, I cannot claim evidence of those skills.

## References

Kalibera, T. and Jones, R.E. (2013) ‘Rigorous benchmarking in reasonable time’, *Proceedings of the ACM SIGPLAN International Symposium on Memory Management*. Available at https://doi.org/10.1145/2464157.2464160 (Accessed 14 October 2026).

Tabassi, E. (2023) *Artificial Intelligence Risk Management Framework (AI RMF 1.0)*. NIST AI 100-1. National Institute of Standards and Technology. Available at https://doi.org/10.6028/NIST.AI.100-1 (Accessed 14 October 2026).
