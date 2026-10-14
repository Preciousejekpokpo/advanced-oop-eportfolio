# Case Study – The Limits of Transaction Evidence

The banking case exposes a weakness that account-level concurrency tests could not establish. Per-account locks protected balance updates, but `RecordingAccount` saved transaction evidence only after each operation. A failed record write could therefore leave a correct balance with an incomplete history, even when subsequent reports accurately processed the available records.

The consequences become harder to detect when missing transactions cancel. An unrecorded £25 deposit and withdrawal return the balance to its opening value, allowing net-movement reconciliation to pass. This agreement offers little assurance that individual operations can be traced or investigated. Even matching record counts cannot establish accuracy when transaction amounts are misrepresented.

The findings suggest that financial assurance depends on reliable event evidence alongside protected account balances. Coordinated updates, transaction-level verification and recovery testing would offer stronger safeguards, although their implementation and performance costs remain unexplored. The [capstone evaluation](../05-Capstone-Project/CAPSTONE_EVALUATION.md) examines how far the additional checks address these weaknesses.
