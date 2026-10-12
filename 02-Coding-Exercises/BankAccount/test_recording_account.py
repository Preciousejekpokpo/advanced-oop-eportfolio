"""Test the recording decorator's behaviour and limits."""

import threading
import unittest
from decimal import Decimal

from bank_account import BankAccount
from recording_account import RecordingAccount, TransactionRecord
from strategy_simulator import DepositOnlyTransactions, StrategySimulator


class TestRecordingAccount(unittest.TestCase):
    """Check that recording preserves account outcomes and concurrent counts."""

    def test_deposit_returns_original_result_and_creates_record(self):
        original = BankAccount("DEPOSIT", 100)
        recorded = RecordingAccount(original)

        self.assertEqual(recorded.deposit("25.50"), Decimal("125.50"))
        self.assertEqual(original.get_balance(), Decimal("125.50"))
        self.assertEqual(
            recorded.records(),
            (TransactionRecord("deposit", Decimal("25.50"), True),),
        )

    def test_withdrawal_records_success_and_insufficient_funds(self):
        recorded = RecordingAccount(BankAccount("WITHDRAW", 20))

        self.assertTrue(recorded.withdraw(5))
        self.assertFalse(recorded.withdraw(30))
        self.assertEqual(recorded.get_balance(), Decimal("15"))
        self.assertEqual([entry.succeeded for entry in recorded.records()], [True, False])

    def test_balance_read_does_not_create_record(self):
        recorded = RecordingAccount(BankAccount("READ", 10))

        self.assertEqual(recorded.get_balance(), Decimal("10"))
        self.assertEqual(recorded.records(), ())

    def test_invalid_operation_does_not_create_a_completion_record(self):
        recorded = RecordingAccount(BankAccount("INVALID", 10))

        with self.assertRaises(ValueError):
            recorded.deposit(-2)
        with self.assertRaises(ValueError):
            recorded.withdraw("not a number")

        self.assertEqual(recorded.records(), ())
        self.assertEqual(recorded.get_balance(), Decimal("10"))

    def test_transfer_records_success_and_insufficient_funds(self):
        source = RecordingAccount(BankAccount("SOURCE", 50))
        destination = BankAccount("TARGET", 5)

        self.assertTrue(source.transfer_to(destination, 20))
        self.assertFalse(source.transfer_to(destination, 100))
        self.assertEqual(source.get_balance(), Decimal("30"))
        self.assertEqual(destination.get_balance(), Decimal("25"))
        self.assertEqual(
            source.records(),
            (
                TransactionRecord("transfer", Decimal("20"), True, "TARGET"),
                TransactionRecord("transfer", Decimal("100"), False, "TARGET"),
            ),
        )

    def test_transfer_accepts_another_recording_account(self):
        source = RecordingAccount(BankAccount("SRC", 50))
        destination = RecordingAccount(BankAccount("DST", 10))

        self.assertTrue(source.transfer_to(destination, 5))
        self.assertEqual(source.get_balance(), Decimal("45"))
        self.assertEqual(destination.get_balance(), Decimal("15"))
        self.assertEqual(len(source.records()), 1)
        # A transfer is recorded once at its initiating account, not twice.
        self.assertEqual(destination.records(), ())

    def test_self_transfer_keeps_original_validation(self):
        recorded = RecordingAccount(BankAccount("SELF", 10))

        with self.assertRaises(ValueError):
            recorded.transfer_to(recorded, 1)
        self.assertEqual(recorded.get_balance(), Decimal("10"))
        self.assertEqual(recorded.records(), ())

    def test_concurrent_deposits_do_not_lose_records(self):
        recorded = RecordingAccount(BankAccount("CONCURRENT", 0))
        errors = []

        def deposit_many():
            try:
                for _ in range(250):
                    recorded.deposit(1)
            except Exception as exc:
                errors.append(exc)

        workers = [threading.Thread(target=deposit_many) for _ in range(8)]
        for worker in workers:
            worker.start()
        for worker in workers:
            worker.join()

        self.assertEqual(errors, [])
        self.assertEqual(recorded.get_balance(), Decimal("2000"))
        self.assertEqual(len(recorded.records()), 2000)

    def test_decorator_works_with_the_strategy_simulator(self):
        recorded = RecordingAccount(BankAccount("STRATEGY", 0))
        simulator = StrategySimulator(
            recorded, 4, 10, DepositOnlyTransactions(), Decimal("2")
        )

        self.assertEqual(simulator.run(), Decimal("80"))
        self.assertEqual(len(recorded.records()), 40)

    def test_record_snapshot_cannot_mutate_internal_records(self):
        recorded = RecordingAccount(BankAccount("SNAPSHOT", 10))
        recorded.deposit(1)
        snapshot = recorded.records()

        with self.assertRaises(AttributeError):
            snapshot.append(TransactionRecord("deposit", Decimal("2"), True))
        self.assertEqual(len(recorded.records()), 1)


if __name__ == "__main__":
    unittest.main()
