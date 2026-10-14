# Task 4 Professional Development Plan

The banking assignment gave me experience of protecting shared state and testing concurrent transactions. Extending it through design patterns, contention experiments and an AI-facing prototype has developed my interest in application security and software assurance. I would like to contribute to evaluating security controls during development, particularly where decisions about reliability depend on evidence that other people can reproduce and question. I want to build on this work while gaining experience with failures beyond controlled exercises.

I use SFIA 9 to guide my development in testing, design and assurance, without claiming an assessed competence level (SFIA Foundation, 2024). The BCS Code of Conduct also informs my approach to continued learning, accurate reporting and professional judgement (BCS, n.d.).

| Skill and benchmark | Evidence and gap | Action and progress marker | Target |
|---|---|---|---|
| Functional testing (SFIA TEST) | Bank and checkout tests pass, but test-first practice is uneven | Write ten boundary and failure tests before a checkout extension, recording defects and gaps | Nov 2026 |
| Non-functional testing (SFIA NFTS) | Contention tests found no consistent throughput gain | Repeat twenty runs per configuration on stable Python and report variation | Dec 2026 |
| Software design (SFIA SWDN) | Balance updates and transaction records lack atomicity | Build an SQLite prototype and test rollback after failure | Jan 2027 |
| Information assurance (SFIA INAS) | Mocked advice leaves provenance and fairness unverified | Trace model inputs and assess manipulation, bias and human review | Feb 2027 |
| Professional communication (BCS) | GitHub documents my decisions, without peer code review | Seek two reviews and document criticism and my responses | Feb 2027 |

I want the boundary tests to inform recovery experiments, whose results could provide a stronger basis for evaluating model advice. I will review progress monthly, including unsuccessful tests and criticism from reviewers, rather than judge my development by passing test totals alone.

## References

BCS (n.d.) *BCS Code of Conduct*. Available at: https://www.bcs.org/membership-and-registrations/become-a-member/bcs-code-of-conduct/ (Accessed: 14 October 2026).

SFIA Foundation (2024) *SFIA 9 skills directory*. Available at: https://sfia-online.org/en/sfia-9/skills (Accessed: 14 October 2026).
