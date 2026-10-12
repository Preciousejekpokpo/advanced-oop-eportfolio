"""Record account operations without changing the existing BankAccount class."""

from __future__ import annotations

import threading
from dataclasses import dataclass
from decimal import Decimal

from bank_account import BankAccount


@dataclass(frozen=True)
class TransactionRecord:
    """Describe the outcome of one completed transaction attempt."""

    operation: str
    amount: Decimal
    succeeded: bool
    target_account: str | None = None


class RecordingAccount:
    """Wrap a BankAccount and record its transaction outcomes in memory."""

    def __init__(self, account: BankAccount) -> None:
        if not isinstance(account, BankAccount):
            raise TypeError("RecordingAccount requires a BankAccount.")

        self._account = account
        self._records: list[TransactionRecord] = []
        # This lock protects the record list, not the account balance.
        self._record_lock = threading.Lock()

    @property
    def account_number(self) -> str:
        """Preserve access to the account identifier without copying state."""
        return self._account.account_number

    def _append(self, record: TransactionRecord) -> None:
        with self._record_lock:
            self._records.append(record)

    def deposit(self, amount: object) -> Decimal:
        """Delegate a deposit, then record the completed operation."""
        balance = self._account.deposit(amount)
        self._append(TransactionRecord("deposit", Decimal(str(amount)), True))
        return balance

    def withdraw(self, amount: object) -> bool:
        """Record both successful withdrawals and insufficient-funds attempts."""
        succeeded = self._account.withdraw(amount)
        self._append(
            TransactionRecord("withdraw", Decimal(str(amount)), succeeded)
        )
        return succeeded

    def transfer_to(self, target: BankAccount | RecordingAccount, amount: object) -> bool:
        """Delegate a transfer and record its outcome on the source wrapper."""
        # BankAccount.transfer_to() expects a BankAccount, not a wrapper.
        underlying_target = target._account if isinstance(target, RecordingAccount) else target
        succeeded = self._account.transfer_to(underlying_target, amount)
        self._append(
            TransactionRecord(
                "transfer", Decimal(str(amount)), succeeded,
                underlying_target.account_number,
            )
        )
        return succeeded

    def get_balance(self) -> Decimal:
        """Read the real account balance without creating a transaction record."""
        return self._account.get_balance()

    def records(self) -> tuple[TransactionRecord, ...]:
        """Return a snapshot so callers cannot change the internal record list."""
        with self._record_lock:
            return tuple(self._records)


if __name__ == "__main__":
    original = BankAccount("DECORATOR_DEMO", 100)
    recorded = RecordingAccount(original)

    recorded.deposit(25)
    recorded.withdraw(10)
    recorded.withdraw(500)

    print(f"Final balance £{recorded.get_balance()}")
    print(f"Recorded transaction attempts {len(recorded.records())}")
    for entry in recorded.records():
        print(f"{entry.operation} £{entry.amount}, succeeded={entry.succeeded}")
