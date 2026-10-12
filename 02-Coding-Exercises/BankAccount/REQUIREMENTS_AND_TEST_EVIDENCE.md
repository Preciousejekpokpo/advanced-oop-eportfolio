# BankAccount | Requirements, Evidence and Remaining Gaps

## Examining the Evidence

The original assessment was designed around protecting account invariants, with each test examining a particular behaviour under concurrent execution. However, revisiting the implementation highlighted a distinction between meeting a requirement in the tested conditions and establishing how reliably that requirement would hold under less predictable workloads.

The following assessment connects the banking requirements to the methods responsible for enforcing them and the tests used to examine their behaviour. It also identifies where the available evidence remains limited.

| Requirement | Implementation and test evidence | Assessment and remaining gap |
|---|---|---|
| Maintain valid account balances | `deposit()`, `withdraw()` and `get_balance()` with transaction and validation tests | Expected results are verified, although transaction values are not restricted to a defined currency precision. |
| Prevent lost updates | Per-account locking, tested through 5,000 concurrent deposits | The expected balance is preserved in the tested run, but alternative thread schedules remain unexplored. |
| Prevent concurrent overspending | Atomic funds check and deduction, tested using twenty competing withdrawals from a balance of 100 | Ten withdrawals succeed and the final balance is zero. Other amounts and workload patterns remain untested. |
| Preserve funds during transfers | `transfer_to()`, successful and failed transfer tests, and opposing-transfer tests | The tested transfers preserve balances. Recovery following a process failure is outside the implementation. |
| Prevent circular waiting | Consistent two-account lock ordering and an opposing-transfer test | Both threads finish within the five-second timeout. Mutable account identifiers remain a potential weakness in the ordering rule. |
| Support multiple concurrent users | `TransactionSimulator` with ten users performing 100 operations each | The expected final balance is reproduced, although the fixed transaction sequence limits workload diversity. |
| Validate account identity | Constructor validation and invalid-account-number tests | Empty identifiers are rejected, but uniqueness and immutability are not enforced. |
| Reject invalid operations | Amount validation, insufficient-funds and self-transfer tests | The tested error conditions are handled, but the suite does not exhaust all possible invalid inputs. |

## What the Evidence Leaves Open

The contested-withdrawal test provides stronger evidence for the withdrawal invariant than the deposit test alone because competing threads must respond correctly when the available funds become insufficient. Even so, `threading.Barrier` coordinates their starting point without controlling the subsequent order of execution, leaving some interleavings unexamined.

The opposing-transfer test also requires careful interpretation. Completion within the timeout supports the lock-ordering decision for that scenario, although it does not establish the absence of every possible deadlock. Moreover, the test checks the final account balances after both threads finish, rather than observing every intermediate state.

A further testing limitation lies in how failures within worker threads are reported. Unhandled thread exceptions do not automatically become assertion failures in the main `unittest` thread, so future concurrency tests should capture and examine worker errors explicitly.

The next stage should concentrate on these evidential gaps and the scalability concerns identified in the lecturer's feedback. Repeated workloads, varied account distributions and measured contention would provide a firmer basis for judging whether the locking strategy remains appropriate as the system grows.
