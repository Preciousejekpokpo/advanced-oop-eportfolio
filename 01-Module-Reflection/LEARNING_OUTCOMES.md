# Task 1 Learning Outcomes

At the start of the banking exercise, I assessed progress through requirements I could test, including protected balances, rejection of invalid amounts and transfers using a consistent lock order. Those results were useful, but subsequent work showed me the limits of evaluating classes individually. An account can update correctly while another component loses the evidence needed to explain the operation. I responded by testing failure paths and putting evidence checks ahead of optional model advice. I would now examine the boundaries between components earlier in the design process, rather than waiting for integration tests to expose them.

Prechelt et al. (2001) found maintenance benefits from design patterns in most of their experimental tasks, although simpler solutions sometimes performed better. Barr et al. (2015) examine why judging software correctness depends on the adequacy of the test oracle. Reading these studies alongside my experiments changed the questions I ask of an implementation. I look for a demonstrable reason to introduce an abstraction and for tests capable of challenging the assumptions behind a passing result.

My pattern choices also revealed different costs. Strategy helped separate workload selection from thread management, while Decorator and Visitor enabled extensions without changing the account logic. Abstract Factory made compatible starting configurations explicit. None of these advantages removes the need to investigate data consistency or changes made after construction. I would assess each additional layer against the specific behaviour it makes easier to change or verify.

The injected `ReviewModel` interface demonstrated testable separation from a model dependency, but I have not evaluated a live model or a feature pipeline. Model Registry and Feature Store remain conceptual. Before developing the AI-facing design further, I would prioritise reliable event evidence, failure recovery and meaningful performance measurements.

## References

Barr, E.T., Harman, M., McMinn, P., Shahbaz, M. and Yoo, S. (2015) ‘The oracle problem in software testing: A survey’, *IEEE Transactions on Software Engineering*, 41(5), pp. 507–525. Available at: https://doi.org/10.1109/TSE.2014.2372785 (Accessed: 14 October 2026).

Prechelt, L., Unger, B., Tichy, W.F., Brössler, P. and Votta, L.G. (2001) ‘A controlled experiment in maintenance: Comparing design patterns to simpler solutions’, *IEEE Transactions on Software Engineering*, 27(12), pp. 1134–1144. Available at: https://doi.org/10.1109/32.988711 (Accessed: 14 October 2026).
