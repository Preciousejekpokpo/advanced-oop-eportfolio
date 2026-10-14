"""Test the capstone's transaction checks and model review workflow."""

import unittest
from decimal import Decimal
from unittest.mock import Mock, patch

from bank_account import BankAccount
from capstone_workflow import CapstoneWorkflow
from model_review import ReviewFacts, ReviewModel
from recording_account import RecordingAccount, TransactionRecord
from scenario_factories import (
    BalanceScenarioFactory,
    BankingScenario,
    RecordedMovementCheck,
    RecordedScenarioFactory,
)
from strategy_simulator import AlternatingTransactions, StrategySimulator


class TestCapstoneWorkflow(unittest.TestCase):
    """Check how the workflow responds to complete and unreliable records."""

    def setUp(self):
        self.model = Mock(spec=ReviewModel)
        self.model.suggest.return_value = "no_flag"
        self.workflow = CapstoneWorkflow(self.model)

    def make_alternating_scenario(self, account_number):
        """Create a recorded deposit-and-withdrawal scenario."""
        account = RecordingAccount(BankAccount(account_number, 100))

        simulator = StrategySimulator(
            account,
            num_users=1,
            operations_per_user=2,
            strategy=AlternatingTransactions(),
            transaction_amount=Decimal("25"),
        )

        check = RecordedMovementCheck(
            account,
            account.get_balance(),
        )

        return BankingScenario(account, simulator, check)

    def test_complete_records_reach_model_review(self):
        scenario = RecordedScenarioFactory().build("COMPLETE", 100, 2, 3, 5)

        result = self.workflow.run(scenario)

        self.assertEqual(result.status, "advisory_only")
        self.assertEqual(result.model_label, "no_flag")
        self.assertEqual(scenario.account.get_balance(), Decimal("130"))
        self.assertEqual(len(scenario.account.records()), 6)

        self.model.suggest.assert_called_once_with(
            ReviewFacts(
                net_movement=Decimal("30"),
                failed_attempts=0,
                recorded_attempts=6,
            )
        )

    def test_missing_records_cause_balance_mismatch(self):
        scenario = RecordedScenarioFactory().build("MISMATCH", 100, 1, 2, 5)

        with patch.object(scenario.account, "_append", return_value=None):
            result = self.workflow.run(scenario)

        self.assertEqual(scenario.account.get_balance(), Decimal("110"))
        self.assertEqual(scenario.account.records(), ())
        self.assertEqual(result.status, "manual_review")
        self.assertEqual(result.reason, "record_mismatch")
        self.model.suggest.assert_not_called()

    def test_count_check_detects_offsetting_missing_records(self):
        scenario = self.make_alternating_scenario("OFFSET")

        # Both operations finish, but neither produces a record.
        with patch.object(scenario.account, "_append", return_value=None):
            result = self.workflow.run(scenario)

        self.assertEqual(scenario.account.get_balance(), Decimal("100"))
        self.assertEqual(scenario.account.records(), ())
        self.assertEqual(result.status, "manual_review")
        self.assertEqual(result.reason, "record_count_mismatch")
        self.model.suggest.assert_not_called()

    def test_recording_exception_stops_the_workflow(self):
        scenario = RecordedScenarioFactory().build("FAILURE", 100, 1, 2, 5)

        with patch.object(
            scenario.account,
            "_append",
            side_effect=OSError("Record unavailable"),
        ):
            with self.assertRaises(RuntimeError) as caught:
                self.workflow.run(scenario)

        self.assertIsInstance(caught.exception.__cause__, OSError)
        self.assertEqual(scenario.account.get_balance(), Decimal("105"))
        self.assertEqual(scenario.account.records(), ())
        self.model.suggest.assert_not_called()

    def test_invalid_model_response_requires_manual_review(self):
        scenario = RecordedScenarioFactory().build("INVALID", 100, 1, 2, 5)
        self.model.suggest.return_value = "approved"

        result = self.workflow.run(scenario)

        self.assertEqual(result.status, "manual_review")
        self.assertEqual(result.reason, "invalid_model_output")
        self.model.suggest.assert_called_once()

    def test_plain_account_scenario_is_rejected(self):
        scenario = BalanceScenarioFactory().build("PLAIN", 100, 1, 2, 5)

        with self.assertRaises(TypeError):
            self.workflow.run(scenario)

        self.model.suggest.assert_not_called()

    def test_matching_counts_can_still_hide_incorrect_amounts(self):
        scenario = self.make_alternating_scenario("WRONG_AMOUNTS")
        original_append = scenario.account._append

        # Replace both £25 records with £10 records.
        def record_wrong_amount(entry):
            altered = TransactionRecord(
                entry.operation,
                Decimal("10"),
                entry.succeeded,
                entry.target_account,
            )
            original_append(altered)

        with patch.object(
            scenario.account,
            "_append",
            side_effect=record_wrong_amount,
        ):
            result = self.workflow.run(scenario)

        self.assertEqual(scenario.account.get_balance(), Decimal("100"))
        self.assertEqual(len(scenario.account.records()), 2)
        self.assertTrue(
            all(record.amount == Decimal("10") for record in scenario.account.records())
        )
        self.assertEqual(result.status, "advisory_only")
        self.assertEqual(result.model_label, "no_flag")
        self.model.suggest.assert_called_once()


if __name__ == "__main__":
    unittest.main()
