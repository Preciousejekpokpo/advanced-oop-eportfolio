# Task 1 Learning Outcomes

At the start of the banking exercise, I assessed progress through requirements I could test, including protected balances, rejection of invalid amounts and transfers using a consistent lock order. Those results were useful, but subsequent work showed me the limits of evaluating classes individually. An account could update correctly while another component lost evidence needed to explain the operation. This prompted me to examine failure paths and question whether passing tests offered sufficient assurance.

My experience with design patterns also changed how I evaluate abstraction. Strategy separated transaction behaviour from simulation, while Decorator and Visitor extended recording and reporting without changing the account logic. Abstract Factory established compatible configurations. However, each introduced assumptions or maintenance costs. Prechelt et al. (2001) found that patterns could improve maintainability, although simpler alternatives sometimes performed better. I now consider whether an abstraction solves a demonstrated problem rather than treating flexibility as sufficient justification.

Barr et al. (2015) examine the difficulty of selecting adequate test oracles. This became relevant when passing assertions exposed weaknesses in transaction verification. I learned to distinguish correct execution under test from evidence of reliability, particularly when failures occur between well-tested components.

The injected `ReviewModel` interface demonstrated testable separation from a model dependency, but no live AI model was evaluated. Model Registry and Feature Store remained conceptual. Before extending this design, I would prioritise reliable transaction evidence, recovery testing and performance measurements. These findings shifted my attention towards assumptions connecting components, where apparently successful implementations may conceal important risks.

## References

Barr, E.T., Harman, M., McMinn, P., Shahbaz, M. and Yoo, S. (2015) ‘The oracle problem in software testing: A survey’, *IEEE Transactions on Software Engineering*, 41(5), pp. 507–525. Available at https://doi.org/10.1109/TSE.2014.2372785 (Accessed 14 October 2026).

Prechelt, L., Unger, B., Tichy, W.F., Brössler, P. and Votta, L.G. (2001) ‘A controlled experiment in maintenance: Comparing design patterns to simpler solutions’, *IEEE Transactions on Software Engineering*, 27(12), pp. 1134–1144. Available at https://doi.org/10.1109/32.988711 (Accessed 14 October 2026).
