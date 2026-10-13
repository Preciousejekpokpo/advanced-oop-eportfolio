"""Test transaction reports, including gaps in the records they use."""

import unittest
from decimal import Decimal
from unittest.mock import patch

from bank_account import BankAccount
from recording_account import RecordingAccount, TransactionRecord
from transaction_visitors import (
    CashFlowVisitor,
    DepositEntry,
    FailedAttemptVisitor,
    TransactionVisitor,
    WithdrawalEntry,
    visit_records,
)


class TestTransactionVisitors(unittest.TestCase):
    """Check both the reporting logic and what its results cannot establish."""

    def test_cash_flow_counts_successful_deposits(self):
        account = RecordingAccount(BankAccount("DEPOSITS", 100))

        # Use decimal amounts to check that the report keeps the pennies.
        account.deposit("20.50")
        account.deposit("3.25")
        visitor = CashFlowVisitor()

        visit_records(account.records(), visitor)

        self.assertEqual(visitor.summary().deposits, Decimal("23.75"))
        self.assertEqual(visitor.summary().net_change, Decimal("23.75"))

    def test_failed_withdrawal_does_not_reduce_reported_balance(self):
        account = RecordingAccount(BankAccount("REJECTION", 10))

        # A rejected withdrawal must not appear as money leaving the account.
        self.assertFalse(account.withdraw(20))
        visitor = CashFlowVisitor()

        visit_records(account.records(), visitor)

        self.assertEqual(visitor.summary().net_change, Decimal("0"))
        self.assertEqual(account.get_balance(), Decimal("10"))

    def test_successful_withdrawal_reduces_reported_balance(self):
        account = RecordingAccount(BankAccount("WITHDRAWAL", 50))
        self.assertTrue(account.withdraw(15))
        visitor = CashFlowVisitor()

        visit_records(account.records(), visitor)

        self.assertEqual(visitor.summary().withdrawals, Decimal("15"))
        self.assertEqual(visitor.summary().net_change, Decimal("-15"))

    def test_outgoing_transfer_is_counted_only_for_source(self):
        source = RecordingAccount(BankAccount("SOURCE", 50))
        destination = RecordingAccount(BankAccount("DESTINATION", 10))

        # The transfer reaches the destination, but only the source wrapper logs it.
        self.assertTrue(source.transfer_to(destination, 15))
        source_report = CashFlowVisitor()
        destination_report = CashFlowVisitor()

        visit_records(source.records(), source_report)
        visit_records(destination.records(), destination_report)

        self.assertEqual(
            source_report.summary().outgoing_transfers,
            Decimal("15"),
        )
        self.assertEqual(
            source_report.summary().net_change,
            Decimal("-15"),
        )
        self.assertEqual(
            destination_report.summary().net_change,
            Decimal("0"),
        )
        self.assertEqual(destination.get_balance(), Decimal("25"))

    def test_failed_attempts_visitor_collects_rejections(self):
        source = RecordingAccount(BankAccount("FAILURES", 10))
        destination = BankAccount("TARGET", 0)

        # Two failed operations and one successful deposit give us a mixed record.
        self.assertFalse(source.withdraw(20))
        self.assertFalse(source.transfer_to(destination, 100))
        source.deposit(5)
        visitor = FailedAttemptVisitor()

        visit_records(source.records(), visitor)

        self.assertEqual(
            [(entry.operation, entry.amount) for entry in visitor.failures()],
            [
                ("withdraw", Decimal("20")),
                ("transfer", Decimal("100")),
            ],
        )

    def test_different_visitors_use_the_same_record_snapshot(self):
        account = RecordingAccount(BankAccount("SHARED_SNAPSHOT", 100))
        account.deposit(10)
        account.withdraw(200)

        # Run both reports against one snapshot so they see the same attempts.
        snapshot = account.records()
        flow = CashFlowVisitor()
        failures = FailedAttemptVisitor()

        visit_records(snapshot, flow)
        visit_records(snapshot, failures)

        self.assertEqual(flow.summary().net_change, Decimal("10"))
        self.assertEqual(len(failures.failures()), 1)
        self.assertEqual(len(snapshot), 2)

    def test_visitors_do_not_modify_account_balance(self):
        account = RecordingAccount(BankAccount("UNCHANGED", 100))
        account.deposit(2)

        # Reading records should never change the actual money in the account.
        before = account.get_balance()
        visit_records(account.records(), CashFlowVisitor())
        visit_records(account.records(), FailedAttemptVisitor())

        self.assertEqual(account.get_balance(), before)

    def test_unknown_operation_is_reported(self):
        visitor = CashFlowVisitor()

        # A new operation type needs explicit support in the Visitor adapter.
        record = TransactionRecord("refund", Decimal("5"), True)

        with self.assertRaisesRegex(
            ValueError,
            "Unknown transaction operation",
        ):
            visit_records((record,), visitor)

    def test_rejects_an_object_without_visitor_contract(self):
        with self.assertRaises(TypeError):
            visit_records((), object())

    def test_event_accept_calls_the_matching_visitor_method(self):
        class CalledVisitor(TransactionVisitor):
            def __init__(self):
                self.events = []

            def visit_deposit(self, entry):
                self.events.append(("deposit", entry.record.amount))

            def visit_withdrawal(self, entry):
                self.events.append(("withdraw", entry.record.amount))

            def visit_transfer(self, entry):
                self.events.append(("transfer", entry.record.amount))

        # Check accept() dispatches to the method matching each entry type.
        visitor = CalledVisitor()

        DepositEntry(TransactionRecord("deposit", Decimal("4"), True)).accept(visitor)

        WithdrawalEntry(TransactionRecord("withdraw", Decimal("3"), True)).accept(
            visitor
        )

        self.assertEqual(
            visitor.events,
            [
                ("deposit", Decimal("4")),
                ("withdraw", Decimal("3")),
            ],
        )

    def test_reconciliation_detects_missing_record_after_successful_deposit(self):
        account = RecordingAccount(BankAccount("GAP", 100))
        opening_balance = account.get_balance()

        # Simulate the Decorator failure we found earlier, then compare the report.
        with patch.object(
            account,
            "_append",
            side_effect=OSError("Unavailable"),
        ):
            with self.assertRaises(OSError):
                account.deposit(25)

        cash_flow = CashFlowVisitor()
        visit_records(account.records(), cash_flow)
        actual_change = account.get_balance() - opening_balance

        self.assertEqual(actual_change, Decimal("25"))
        self.assertEqual(cash_flow.summary().net_change, Decimal("0"))
        self.assertNotEqual(
            actual_change,
            cash_flow.summary().net_change,
        )

    def test_snapshot_does_not_include_later_transactions(self):
        account = RecordingAccount(BankAccount("SNAPSHOT", 100))
        account.deposit(10)

        # A snapshot should represent the records available when it was taken.
        snapshot = account.records()
        account.deposit(15)
        visitor = CashFlowVisitor()

        visit_records(snapshot, visitor)

        self.assertEqual(visitor.summary().net_change, Decimal("10"))
