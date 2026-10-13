
"""Analyse transaction records without changing the account's financial logic."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal

from recording_account import RecordingAccount, TransactionRecord


class TransactionVisitor(ABC):
    """Define the operations that each transaction report must support."""

    @abstractmethod
    def visit_deposit(self, entry: "DepositEntry") -> None:
        pass

    @abstractmethod
    def visit_withdrawal(self, entry: "WithdrawalEntry") -> None:
        pass

    @abstractmethod
    def visit_transfer(self, entry: "TransferEntry") -> None:
        pass


# These entries adapt the existing records for Visitor.
# This keeps reporting changes out of RecordingAccount.
@dataclass(frozen=True)
class DepositEntry:
    record: TransactionRecord

    def accept(self, visitor: TransactionVisitor) -> None:
        visitor.visit_deposit(self)


@dataclass(frozen=True)
class WithdrawalEntry:
    record: TransactionRecord

    def accept(self, visitor: TransactionVisitor) -> None:
        visitor.visit_withdrawal(self)


@dataclass(frozen=True)
class TransferEntry:
    record: TransactionRecord

    def accept(self, visitor: TransactionVisitor) -> None:
        visitor.visit_transfer(self)


def visit_records(records: tuple[TransactionRecord, ...], visitor: TransactionVisitor) -> None:
    """Pass recorded operations to the appropriate visitor methods."""
    if not isinstance(visitor, TransactionVisitor):
        raise TypeError("Visitor must implement TransactionVisitor.")

    # Match each recorded operation to its entry type.
    # An unfamiliar operation needs explicit support before it can be analysed.
    entry_types = {
        "deposit": DepositEntry,
        "withdraw": WithdrawalEntry,
        "transfer": TransferEntry,
    }

    for record in records:
        try:
            entry_type = entry_types[record.operation]
        except KeyError as exc:
            raise ValueError(f"Unknown transaction operation: {record.operation}") from exc
        entry_type(record).accept(visitor)


@dataclass(frozen=True)
class CashFlowSummary:
    deposits: Decimal
    withdrawals: Decimal
    outgoing_transfers: Decimal
    net_change: Decimal


class CashFlowVisitor(TransactionVisitor):
    """Calculate balance movements from transactions recorded as successful."""

    def __init__(self) -> None:
        self._deposits = Decimal("0")
        self._withdrawals = Decimal("0")
        self._outgoing_transfers = Decimal("0")

    def visit_deposit(self, entry: DepositEntry) -> None:
        # A failed attempt must not increase the reported balance.
        if entry.record.succeeded:
            self._deposits += entry.record.amount

    def visit_withdrawal(self, entry: WithdrawalEntry) -> None:
        # Only completed withdrawals count as money leaving the account.
        if entry.record.succeeded:
            self._withdrawals += entry.record.amount

    def visit_transfer(self, entry: TransferEntry) -> None:
        if entry.record.succeeded:
            # The source wrapper records the outgoing transfer.
            # The destination receives the money but has no matching entry.
            self._outgoing_transfers += entry.record.amount

    def summary(self) -> CashFlowSummary:
        # These totals describe recorded activity, which may be incomplete.
        return CashFlowSummary(
            self._deposits,
            self._withdrawals,
            self._outgoing_transfers,
            self._deposits - self._withdrawals - self._outgoing_transfers,
        )


class FailedAttemptVisitor(TransactionVisitor):
    """Collect failed attempts found in the available transaction records."""

    def __init__(self) -> None:
        self._failed: list[TransactionRecord] = []

    def visit_deposit(self, entry: DepositEntry) -> None:
        if not entry.record.succeeded:
            self._failed.append(entry.record)

    def visit_withdrawal(self, entry: WithdrawalEntry) -> None:
        if not entry.record.succeeded:
            self._failed.append(entry.record)

    def visit_transfer(self, entry: TransferEntry) -> None:
        if not entry.record.succeeded:
            self._failed.append(entry.record)

    def failures(self) -> tuple[TransactionRecord, ...]:
        # A missing record cannot be identified from this report alone.
        # Its findings depend on what RecordingAccount successfully captured.
        return tuple(self._failed)


if __name__ == "__main__":
    from bank_account import BankAccount

    account = RecordingAccount(BankAccount("VISITOR_DEMO", 100))
    destination = BankAccount("RECIPIENT", 0)

    account.deposit(25)
    account.withdraw(10)
    account.withdraw(500)
    account.transfer_to(destination, 5)

    # Use one snapshot for both reports so they examine the same activity.
    snapshot = account.records()
    cash_flow = CashFlowVisitor()
    failed_attempts = FailedAttemptVisitor()

    visit_records(snapshot, cash_flow)
    visit_records(snapshot, failed_attempts)

    print(f"Recorded net change £{cash_flow.summary().net_change}")
    print(f"Rejected recorded attempts {len(failed_attempts.failures())}")
    print(f"Actual final balance £{account.get_balance()}")
