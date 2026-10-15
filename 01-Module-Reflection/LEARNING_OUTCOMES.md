# Task 1 Learning Outcomes

At the start of the banking exercise, I assessed progress through requirements I could test, including protected balances, rejection of invalid amounts and transfers using a consistent lock order. Those results were useful, but subsequent work showed me the limits of evaluating classes individually. When recording failed after a deposit, the balance changed without a corresponding record. I had protected the balance, but not the evidence needed to explain it.

My experience with design patterns changed how I evaluate abstraction. Strategy separated transaction selection from thread management. Decorator and Visitor extended recording and reporting, while Abstract Factory paired compatible components. Yet recording failures exposed the cost of separating updates from evidence. Prechelt et al. (2001) found that simpler solutions sometimes performed better than patterns. I now judge abstractions by both their benefits and failure boundaries.

Barr et al. (2015) examine the difficulty of choosing adequate test oracles. Two unrecorded opposing movements allowed reconciliation to pass, while [contention trials](../02-Coding-Exercises/BankAccount/CONTENTION_EVALUATION.md) preserved balances without showing scalability gains. Both challenged my reliance on passing tests as evidence of reliability.

The injected `ReviewModel` interface allowed mock testing without a live model. Conceptually, a Model Registry could manage model versions and their lifecycle, while a Feature Store could supply consistent, reusable inputs. Neither was implemented, nor would either restore missing transactions. I would prioritise recording integrity, recovery tests and performance evidence before extending the architecture.

## References

Barr, E.T., Harman, M., McMinn, P., Shahbaz, M. and Yoo, S. (2015) ‘The oracle problem in software testing: A survey’, *IEEE Transactions on Software Engineering*, 41(5), pp. 507–525. Available at https://doi.org/10.1109/TSE.2014.2372785 (Accessed 14 October 2026).

Prechelt, L., Unger, B., Tichy, W.F., Brössler, P. and Votta, L.G. (2001) ‘A controlled experiment in maintenance: Comparing design patterns to simpler solutions’, *IEEE Transactions on Software Engineering*, 27(12), pp. 1134–1144. Available at https://doi.org/10.1109/32.988711 (Accessed 14 October 2026).
