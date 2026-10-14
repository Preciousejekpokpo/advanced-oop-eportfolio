# Task 3 Academic and Employability Skills

At first, I judged my programming progress by how reliably the code executed, although explaining why one design deserved preference was harder. My initial banking submission demonstrated concurrency safeguards, but the lecturer's feedback on traceability and scalability exposed gaps in what my tests established. I subsequently [mapped requirements to tests](../02-Coding-Exercises/BankAccount/REQUIREMENTS_AND_TEST_EVIDENCE.md) and [benchmarked contention](../02-Coding-Exercises/BankAccount/CONTENTION_EVALUATION.md). Balances remained correct, yet increasing thread counts brought no sustained performance improvement. This made me cautious about drawing wider conclusions from successful tests.

That concern resurfaced in the [SOLID checkout exercise](../02-Coding-Exercises/SOLID-Checkout/README.md). Six tests passed before an additional rounding test exposed a fractional-penny result. Correcting it made me more aware of overlooked cases and the need to explain what remained untested, particularly when assessing software reliability.

The AI ethics material raised similar questions about professional responsibility. Tabassi (2023) places trustworthy AI within governance and evaluation, while my mocked tests established neither fairness nor explainability. I would expect reliable input evidence, human oversight and reviewable recommendations before supporting consequential AI decisions.

Writing the GitHub evaluations improved how I communicate technical judgements. I also realised that documentation often followed implementation, leaving less time to question my decisions. Although the portfolio demonstrates independent problem-solving, peer review remains a gap, particularly in responding to criticism and recognising weaknesses I might have missed.

## References

Tabassi, E. (2023) *Artificial Intelligence Risk Management Framework (AI RMF 1.0)*. NIST AI 100-1. National Institute of Standards and Technology. Available at https://doi.org/10.6028/NIST.AI.100-1 (Accessed 14 October 2026).
