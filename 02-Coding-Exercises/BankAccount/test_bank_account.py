"""Unit and concurrency tests for the thread-safe banking system."""

import threading
import unittest
from decimal import Decimal

from bank_account import BankAccount
from transaction_simulator import TransactionSimulator


class TestBankAccount(unittest.TestCase):
    """Tests for BankAccount and TransactionSimulator behaviour."""

    def test_deposit_and_withdraw(self):
        account = BankAccount("ACC1", 100)

        self.assertEqual(account.deposit(50), Decimal("150"))
        self.assertTrue(account.withdraw(120))
        self.assertEqual(account.get_balance(), Decimal("30"))

    def test_insufficient_funds(self):
        account = BankAccount("ACC2", 50)

        self.assertFalse(account.withdraw(100))
        self.assertEqual(account.get_balance(), Decimal("50"))

    def test_invalid_transaction_amounts(self):
        account = BankAccount("ACC3", 10)

        with self.assertRaises(ValueError):
            account.deposit(0)

        with self.assertRaises(ValueError):
            account.withdraw(-5)

    def test_negative_opening_balance_rejected(self):
        with self.assertRaises(ValueError):
            BankAccount("ACC_NEG", -100)

    def test_concurrent_deposits_are_not_lost(self):
        """
        Multiple threads repeatedly deposit into the same account.

        Ten threads make 500 deposits of one unit each, so the final balance
        should be 5,000 if no updates are lost.
        """
        account = BankAccount("ACC4", 0)

        def worker():
            for _ in range(500):
                account.deposit(1)

        threads = [
            threading.Thread(target=worker)
            for _ in range(10)
        ]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        self.assertEqual(
            account.get_balance(),
            Decimal("5000"),
        )

    def test_transaction_simulator(self):
        """
        Run several user sessions concurrently through TransactionSimulator.

        Each user performs 50 deposits and 50 withdrawals of the same amount,
        so the expected final balance is the original balance.
        """
        account = BankAccount("ACC5", 1000)

        simulator = TransactionSimulator(
            account,
            num_users=10,
            operations_per_user=100,
        )

        final_balance = simulator.run()

        self.assertEqual(
            final_balance,
            Decimal("1000"),
        )

    def test_opposite_transfers_do_not_deadlock(self):
        """
        Transfer money in opposite directions between the same two accounts.

        Both threads should finish within the timeout, and the equal transfers
        should leave both accounts with their original balances.
        """
        account_a = BankAccount("ACC_A", 500)
        account_b = BankAccount("ACC_B", 500)

        initial_total = (
            account_a.get_balance()
            + account_b.get_balance()
        )

        def transfer_a_to_b():
            for _ in range(100):
                account_a.transfer_to(account_b, 1)

        def transfer_b_to_a():
            for _ in range(100):
                account_b.transfer_to(account_a, 1)

        # Daemon threads allow the test process to exit if a deadlock is detected.
        first = threading.Thread(target=transfer_a_to_b, daemon=True)
        second = threading.Thread(target=transfer_b_to_a, daemon=True)

        first.start()
        second.start()

        # A timeout lets the test detect a possible deadlock instead of
        # waiting forever.
        first.join(timeout=2)
        second.join(timeout=2)

        self.assertFalse(
            first.is_alive(),
            "First transfer thread did not finish.",
        )
        self.assertFalse(
            second.is_alive(),
            "Second transfer thread did not finish.",
        )

        final_total = (
            account_a.get_balance()
            + account_b.get_balance()
        )

        self.assertEqual(final_total, initial_total)
        self.assertEqual(account_a.get_balance(), Decimal("500"))
        self.assertEqual(account_b.get_balance(), Decimal("500"))


if __name__ == "__main__":
    unittest.main()
