"""Test compatible scenario families and limits of their verification evidence."""

import unittest
from decimal import Decimal
from unittest.mock import patch

from bank_account import BankAccount
from recording_account import RecordingAccount
from scenario_factories import (
    BalanceScenarioFactory,
    RecordedMovementCheck,
    RecordedScenarioFactory,
    ScenarioFactory,
    ScheduledBalanceCheck,
)
from strategy_simulator import AlternatingTransactions, DepositOnlyTransactions


class TestScenarioFactories(unittest.TestCase):
    """Check factory product families and what their results can establish."""

    def test_balance_factory_creates_compatible_products(self):
        scenario = BalanceScenarioFactory().build("BAL", 100, 2, 4, 5)

        self.assertIsInstance(scenario.account, BankAccount)
        self.assertIsInstance(scenario.simulator.strategy, AlternatingTransactions)
        self.assertIsInstance(scenario.evidence_check, ScheduledBalanceCheck)
        self.assertIs(scenario.simulator.account, scenario.account)

    def test_recorded_factory_creates_compatible_products(self):
        scenario = RecordedScenarioFactory().build("REC", 100, 2, 4, 5)

        self.assertIsInstance(scenario.account, RecordingAccount)
        self.assertIsInstance(scenario.simulator.strategy, DepositOnlyTransactions)
        self.assertIsInstance(scenario.evidence_check, RecordedMovementCheck)
        self.assertIs(scenario.simulator.account, scenario.account)

    def test_balanced_workload_matches_expected_change(self):
        scenario = BalanceScenarioFactory().build("EVEN", 100, 4, 10, 5)
        comparison = scenario.run()

        self.assertEqual(scenario.account.get_balance(), Decimal("100"))
        self.assertEqual(comparison.actual_change, Decimal("0"))
        self.assertTrue(comparison.agrees)

    def test_odd_alternating_workload_counts_final_deposit(self):
        # Each user's last deposit has no matching withdrawal when the count is odd.
        scenario = BalanceScenarioFactory().build("ODD", 100, 2, 3, 5)
        comparison = scenario.run()

        self.assertEqual(scenario.account.get_balance(), Decimal("110"))
        self.assertEqual(comparison.comparison_change, Decimal("10"))
        self.assertTrue(comparison.agrees)

    def test_recorded_workload_matches_successful_deposits(self):
        scenario = RecordedScenarioFactory().build("REC_RUN", 100, 2, 4, 5)
        comparison = scenario.run()

        self.assertEqual(scenario.account.get_balance(), Decimal("140"))
        self.assertEqual(len(scenario.account.records()), 8)
        self.assertEqual(comparison.comparison_change, Decimal("40"))
        self.assertTrue(comparison.agrees)

    def test_failed_withdrawal_does_not_distort_record_comparison(self):
        scenario = RecordedScenarioFactory().build("REJECT", 100, 2, 4, 5)
        self.assertFalse(scenario.account.withdraw(500))
        comparison = scenario.run()

        self.assertEqual(len(scenario.account.records()), 9)
        self.assertEqual(comparison.comparison_change, Decimal("40"))
        self.assertTrue(comparison.agrees)

    def test_record_failure_is_detected_as_balance_discrepancy(self):
        scenario = RecordedScenarioFactory().build("RECORD_GAP", 100, 2, 4, 5)

        # The account can accept a deposit even if writing its record fails.
        with patch.object(scenario.account, "_append", side_effect=OSError("Record unavailable")):
            with self.assertRaises(OSError):
                scenario.account.deposit(25)

        comparison = scenario.evidence_check.evaluate(scenario.account.get_balance())
        self.assertEqual(comparison.actual_change, Decimal("25"))
        self.assertEqual(comparison.comparison_change, Decimal("0"))
        self.assertFalse(comparison.agrees)

    def test_second_wrapper_keeps_activity_outside_the_first_history(self):
        scenario = RecordedScenarioFactory().build("TWO_WRAPPERS", 100, 2, 4, 5)
        second = RecordingAccount(scenario.account._account)
        second.deposit(10)

        # The factory selected a coherent family, but cannot control outside access.
        comparison = scenario.evidence_check.evaluate(scenario.account.get_balance())
        self.assertFalse(comparison.agrees)
        self.assertEqual(comparison.actual_change, Decimal("10"))
        self.assertEqual(comparison.comparison_change, Decimal("0"))

    def test_record_check_rejects_plain_account(self):
        with self.assertRaises(TypeError):
            RecordedMovementCheck(BankAccount("PLAIN", 100), Decimal("100"))

    def test_invalid_simulator_configuration_is_rejected(self):
        with self.assertRaises(ValueError):
            BalanceScenarioFactory().build("BAD_USERS", 100, 0, 4, 5)
        with self.assertRaises(ValueError):
            RecordedScenarioFactory().build("BAD_AMOUNT", 100, 2, 4, -5)

    def test_invalid_opening_balance_is_rejected(self):
        with self.assertRaises(ValueError):
            RecordedScenarioFactory().build("NEG", -100, 2, 4, 5)

    def test_factory_creates_independent_accounts(self):
        factory = RecordedScenarioFactory()
        first = factory.build("ONE", 100, 2, 4, 5)
        second = factory.build("TWO", 100, 2, 4, 5)

        first.account.deposit(20)
        self.assertEqual(second.account.get_balance(), Decimal("100"))
        self.assertEqual(second.account.records(), ())

    def test_abstract_factory_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            ScenarioFactory()


if __name__ == "__main__":
    unittest.main()
