# Task 1 Learning Outcomes

The initial banking tests examined requirements that could be verified directly, including protected balance updates, invalid transaction handling and consistent transfer lock ordering. Subsequent extensions exposed weaknesses beyond those individual operations. A balance could remain correct while its transaction history became incomplete, revealing the importance of testing interactions between components rather than relying on passing class-level tests.

The design patterns offered different forms of flexibility. Strategy separated transaction behaviour from simulation, while Decorator and Visitor extended recording and reporting without changing the original account logic. Abstract Factory established compatible scenario configurations. Yet each abstraction introduced costs or assumptions that required further examination. Prechelt et al. (2001) found that patterns could support maintenance, although simpler alternatives sometimes performed better. Their findings reinforce the need to justify patterns against demonstrated requirements.

Testing also changed the interpretation of correctness. Barr et al. (2015) examine the difficulty of selecting adequate test oracles, reflected in experiments where passing assertions exposed weaknesses in financial verification. Secure coding therefore requires attention to failure handling and evidence integrity alongside locking and input validation.

The replaceable `ReviewModel` interface made model-dependent logic testable without a live AI service. Model Registry and Feature Store architectures were explored conceptually rather than implemented. Further development would require reliable transaction evidence, recovery testing and evaluation of real model behaviour before stronger claims about AI readiness could be justified.

## References

Barr, E.T., Harman, M., McMinn, P., Shahbaz, M. and Yoo, S. (2015) ‘The oracle problem in software testing: A survey’, *IEEE Transactions on Software Engineering*, 41(5), pp. 507–525. Available at https://doi.org/10.1109/TSE.2014.2372785 (Accessed 14 October 2026).

Prechelt, L., Unger, B., Tichy, W.F., Brössler, P. and Votta, L.G. (2001) ‘A controlled experiment in maintenance: Comparing design patterns to simpler solutions’, *IEEE Transactions on Software Engineering*, 27(12), pp. 1134–1144. Available at https://doi.org/10.1109/32.988711 (Accessed 14 October 2026).
