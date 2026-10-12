"""Verify interchangeable transaction behaviour and failure reporting."""

import unittest
from decimal import Decimal

from bank_account import BankAccount
from strategy_simulator import (
    AlternatingTransactions,
    DepositOnlyTransactions,
    StrategySimulator,
    TransactionStrategy,
)


class TestStrategySimulator(unittest.TestCase):
    """Check that swapping policies changes behaviour without changing account logic."""

    def test_alternating_transactions_preserve_balance(self):
        account = BankAccount("ALT", 100)
        simulator = StrategySimulator(account, 4, 10, AlternatingTransactions())

        self.assertEqual(simulator.run(), Decimal("100"))

    def test_deposit_only_transactions_increase_balance(self):
        account = BankAccount("DEPOSITS", 100)
        simulator = StrategySimulator(account, 4, 10, DepositOnlyTransactions())

        self.assertEqual(simulator.run(), Decimal("500"))

    def test_strategy_changes_between_runs(self):
        account = BankAccount("CHANGE", 100)
        simulator = StrategySimulator(
            account, 2, 4, AlternatingTransactions(), Decimal("5")
        )

        self.assertEqual(simulator.run(), Decimal("100"))
        simulator.set_strategy(DepositOnlyTransactions())
        self.assertEqual(simulator.run(), Decimal("140"))

    def test_invalid_amounts_are_rejected(self):
        for amount in (0, -2, "NaN", "not a number"):
            with self.subTest(amount=amount):
                with self.assertRaises(ValueError):
                    StrategySimulator(
                        BankAccount("INVALID", 100),
                        2,
                        4,
                        AlternatingTransactions(),
                        amount,
                    )

    def test_non_strategy_is_rejected(self):
        account = BankAccount("TYPE", 100)

        with self.assertRaises(TypeError):
            StrategySimulator(account, 2, 4, object())

    def test_errors_from_workers_are_reported(self):
        class RejectedOperation(TransactionStrategy):
            def apply(self, account, operation, amount):
                raise ValueError("Example worker failure")

        account = BankAccount("FAIL", 100)
        simulator = StrategySimulator(account, 2, 4, RejectedOperation())

        with self.assertRaises(RuntimeError) as caught:
            simulator.run()

        self.assertIsInstance(caught.exception.__cause__, ValueError)
        self.assertEqual(account.get_balance(), Decimal("100"))

    def test_concurrent_deposits_are_counted(self):
        account = BankAccount("COUNT", 0)
        simulator = StrategySimulator(
            account, 8, 500, DepositOnlyTransactions(), Decimal("1")
        )

        self.assertEqual(simulator.run(), Decimal("4000"))


if __name__ == "__main__":
    unittest.main()
