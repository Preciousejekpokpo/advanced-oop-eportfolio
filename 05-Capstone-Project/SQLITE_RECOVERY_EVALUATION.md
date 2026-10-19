# Supplementary SQLite Transaction and Recovery Experiment

The capstone showed that `RecordingAccount` could change a balance before its separate record write failed. This **standalone proof of concept** tests a narrower alternative using SQLite. It does not replace `BankAccount`, `RecordingAccount` or `CapstoneWorkflow`.

A balance update and its corresponding record are committed in one `BEGIN IMMEDIATE` transaction. A unique request ID allows an identical request to be retried without a second credit. The eight automated tests check successful writes, an injected failure between writes, process termination before commit, reopening the database, invalid amounts, withdrawals and concurrent requests.

The interrupted-process test ends a child Python process with `os._exit(17)` after updating the balance, then reopens the database to verify that neither change persisted. This investigates **uncommitted** work. It does not demonstrate recovery from power loss, ambiguous outcomes after commit, cross-account transfers, independent audit integrity or production-scale throughput.

- [Implementation](sqlite_ledger.py)
- [Eight tests](test_sqlite_ledger.py)

Run from the repository root:

```powershell
py -m unittest discover -s "05-Capstone-Project" -p "test_*.py" -v
```
