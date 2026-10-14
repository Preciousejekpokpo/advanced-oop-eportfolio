# Task 3 Academic and Employability Skills

At first, I judged my programming progress by how reliably the code executed, although explaining why one design deserved preference was harder. My initial submission of `bank_account.py`, `transaction_simulator.py` and `test_bank_account.py` demonstrated concurrency safeguards under test, but the lecturer's feedback on traceability and scalability exposed gaps in the evidence. I subsequently [mapped requirements to tests](../02-Coding-Exercises/BankAccount/REQUIREMENTS_AND_TEST_EVIDENCE.md) and [benchmarked contention](../02-Coding-Exercises/BankAccount/CONTENTION_EVALUATION.md), finding no sustained performance improvement as thread counts increased. This has changed how I approach cybersecurity assurance, where a control's success in a defined test cannot justify broader claims about reliability.

Revisiting the SOLID materials and developing the [checkout exercise](../02-Coding-Exercises/SOLID-Checkout/README.md) extended that judgement. Separating payment processing from `Order` made substitution testable, but further abstraction needed a convincing maintenance benefit. Although my first six tests passed, a new rounding test exposed a fractional-penny result, which I corrected and verified through a seven-test run. In a professional release review, I would now pay closer attention to boundary cases and describe what remains untested, rather than present a pass count as assurance.

The AI ethics material raised another professional responsibility. Tabassi (2023) places trustworthy AI within governance and evaluation, whereas my mocked model tests establish neither fairness nor explainability. I would require evidence about data quality, reviewable recommendations and human oversight before supporting the use of such a system in consequential decisions.

Writing GitHub evaluations strengthened my ability to communicate technical judgements to readers unfamiliar with the implementation. Reworking overlapping sections also revealed that I had planned implementation more carefully than documentation, prompting me to allocate space for evidence and analysis earlier. My independent problem-solving is supported by the portfolio, although collaborative design reviews and responding to colleagues' technical criticism remain areas for further development.

## References

Tabassi, E. (2023) *Artificial Intelligence Risk Management Framework (AI RMF 1.0)*. NIST AI 100-1. National Institute of Standards and Technology. Available at: https://doi.org/10.6028/NIST.AI.100-1 (Accessed: 14 October 2026).
