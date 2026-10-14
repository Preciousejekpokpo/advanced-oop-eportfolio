# Capstone: Evaluating AI-Aware Transaction Verification

Developing `CapstoneWorkflow` exposed how easily a modular design can appear more dependable than the evidence it processes. Abstract Factory assembles compatible scenarios, Strategy varies workloads, Decorator records attempts and Visitor summarises their effects. Their separation made integration possible without rewriting `BankAccount`, although each downstream check still trusts the recording wrapper. Prechelt et al. (2001) found that patterns sometimes complicate maintenance compared with simpler alternatives. I would retain these abstractions for their demonstrated testing flexibility, rather than assume that additional classes improve assurance.

The new count check detected an unrecorded £25 deposit and withdrawal whose effects cancelled, withholding model advice where balance reconciliation alone had passed. Seven integration tests passed, bringing the local suite to 72 in 0.043 seconds. A second experiment was more troubling. Replacing both £25 records with £10 records preserved their count and net movement, so the mocked model was consulted. Barr et al. (2015) discuss the difficulty of choosing adequate test oracles. My assertions verified the workflow's rules, while revealing that those rules could accept misleading evidence.

I would prioritise an authoritative event record, transaction identifiers and coordinated balance-and-record updates before broadening AI integration. PostgreSQL Global Development Group (n.d.) explains why related updates need an all-or-nothing boundary, but adopting durable storage would require recovery and contention tests. Tabassi (2023) also locates AI reliability within wider governance and evaluation. Mocked advisory responses cannot establish model accuracy, and the prototype has not demonstrated deployment-scale performance.

## Evidence

- [Workflow](../02-Coding-Exercises/BankAccount/capstone_workflow.py)
- [Integration tests](../02-Coding-Exercises/BankAccount/test_capstone_workflow.py)

## References

Barr, E.T., Harman, M., McMinn, P., Shahbaz, M. and Yoo, S. (2015) ‘The oracle problem in software testing: A survey’, *IEEE Transactions on Software Engineering*, 41(5), pp. 507–525. Available at: https://doi.org/10.1109/TSE.2014.2372785 (Accessed: 14 October 2026).

PostgreSQL Global Development Group (n.d.) ‘3.4 Transactions’, *PostgreSQL 17 Documentation*. Available at: https://www.postgresql.org/docs/17/tutorial-transactions.html (Accessed: 14 October 2026).

Prechelt, L., Unger, B., Tichy, W.F., Brössler, P. and Votta, L.G. (2001) ‘A controlled experiment in maintenance: Comparing design patterns to simpler solutions’, *IEEE Transactions on Software Engineering*, 27(12), pp. 1134–1144. Available at: https://doi.org/10.1109/32.988711 (Accessed: 14 October 2026).

Tabassi, E. (2023) *Artificial Intelligence Risk Management Framework (AI RMF 1.0)*. NIST AI 100-1. National Institute of Standards and Technology. Available at: https://doi.org/10.6028/NIST.AI.100-1 (Accessed: 14 October 2026).
