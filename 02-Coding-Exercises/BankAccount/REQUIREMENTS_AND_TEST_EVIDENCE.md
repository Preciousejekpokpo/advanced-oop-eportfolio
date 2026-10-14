# BankAccount: Requirements and Test Evidence

The initial implementation protects specific account invariants, but passing tests cannot establish how reliably these guarantees hold under different execution schedules or failures. The following assessment maps each requirement to its implementation and test evidence, identifying both what was demonstrated and where assurance remains limited.

| Requirement | Implementation and test evidence | Critical assessment and remaining gap |
|---|---|---|
| Maintain valid balances | `deposit()`, `withdraw()`, `get_balance()` and validation tests | Expected results are verified, although transaction amounts are not restricted to a defined currency precision. |
| Prevent lost updates | Per-account locking, tested through 5,000 concurrent deposits | The expected balance was preserved, but alternative thread schedules remain unexplored. |
| Prevent overspending | Locked funds check and deduction, tested through twenty competing withdrawals | Exactly ten £10 withdrawals succeeded from £100. This challenges the withdrawal invariant more directly than deposits alone, although other amounts remain untested. |
| Preserve funds during transfers | `transfer_to()`, successful and failed transfer tests | Tested balances remain consistent, but recovery following process failure is unsupported. |
| Prevent circular waiting | Consistent lock ordering and opposing-transfer test | Both threads completed within five seconds. Mutable account identifiers could undermine the ordering assumption. |
| Support concurrent users | `TransactionSimulator`, tested with ten users performing 100 operations each | The expected final balance was reproduced, although the fixed transaction sequence limits workload diversity. |
| Validate account identity | Constructor validation and invalid-account-number tests | Blank identifiers are rejected, but uniqueness and immutability are not enforced. |
| Reject invalid operations | Amount validation, insufficient-funds and self-transfer tests | Tested invalid operations are rejected, although the suite does not exhaust all possible inputs. |

## Interpreting the Evidence

The contested-withdrawal test provides stronger evidence for the withdrawal invariant because competing threads must respond correctly when available funds cannot satisfy every request. However, `threading.Barrier` coordinates their starting point without controlling subsequent execution, leaving other interleavings unexamined. Similarly, completion of opposing transfers supports the lock-ordering decision for that scenario, rather than proving universal deadlock freedom.

Worker-error reporting presents another limitation. Unhandled exceptions in worker threads do not automatically fail the main `unittest` assertions, so the original simulator could return a plausible balance despite an interrupted operation. The later Strategy implementation improves exception reporting, although transactions completed before a failure are not reversed. Further assurance would require varied schedules, explicit worker-error checks and recovery testing.
