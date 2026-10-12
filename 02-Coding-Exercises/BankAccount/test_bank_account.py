"""Unit and concurrency tests for the thread-safe banking system."""

import threading
import unittest
from decimal import Decimal

from bank_account import BankAccount
from transaction_simulator import TransactionSimulator


class TestBankAccount(unittest.TestCase):
    """
    Test BankAccount and TransactionSimulator behaviour.

    The suite covers basic functionality, validation, concurrent balance
    updates, contested withdrawals and opposite transfers using consistent
    lock ordering.
    """

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

    def test_invalid_account_number_rejected(self):
        with self.assertRaises(ValueError):
            BankAccount("", 100)

        with self.assertRaises(ValueError):
            BankAccount("   ", 100)

    def test_concurrent_deposits_are_not_lost(self):
        """
        Run repeated deposits against one shared account.

        Ten threads make 500 deposits of one unit each. A barrier brings the
        threads to a common starting point to increase contention.
        """
        account = BankAccount("ACC4", 0)

        number_of_threads = 10
        barrier = threading.Barrier(number_of_threads)

        def worker():
            barrier.wait()

            for _ in range(500):
                account.deposit(1)

        threads = [threading.Thread(target=worker) for _ in range(number_of_threads)]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        self.assertEqual(
            account.get_balance(),
            Decimal("5000"),
        )

    def test_concurrent_withdrawals_do_not_overdraw_account(self):
        """
        Run competing withdrawals against a limited balance.

        Twenty threads each request ten units from an account containing 100.
        A barrier increases contention. Exactly ten withdrawals should succeed.
        """
        account = BankAccount("ACC_WITHDRAW", 100)

        number_of_threads = 20
        barrier = threading.Barrier(number_of_threads)
        results = [False] * number_of_threads

        def worker(index):
            barrier.wait()
            results[index] = account.withdraw(10)

        threads = [
            threading.Thread(target=worker, args=(index,))
            for index in range(number_of_threads)
        ]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        self.assertEqual(sum(results), 10)
        self.assertEqual(account.get_balance(), Decimal("0"))

    def test_transaction_simulator(self):
        """
        Run several user sessions through TransactionSimulator.

        Each user performs 50 deposits and 50 withdrawals of equal value, so
        the expected final balance remains equal to the opening balance.
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

    def test_successful_transfer(self):
        """Transfer funds successfully and verify both resulting balances."""
        account_a = BankAccount("ACC_A2", 100)
        account_b = BankAccount("ACC_B2", 50)

        result = account_a.transfer_to(account_b, 40)

        self.assertTrue(result)
        self.assertEqual(account_a.get_balance(), Decimal("60"))
        self.assertEqual(account_b.get_balance(), Decimal("90"))

    def test_failed_transfer_leaves_accounts_unchanged(self):
        account_a = BankAccount("ACC_A1", 50)
        account_b = BankAccount("ACC_B1", 100)

        result = account_a.transfer_to(account_b, 75)

        self.assertFalse(result)
        self.assertEqual(account_a.get_balance(), Decimal("50"))
        self.assertEqual(account_b.get_balance(), Decimal("100"))

    def test_transfer_to_same_account_rejected(self):
        account = BankAccount("ACC_SELF", 100)

        with self.assertRaises(ValueError):
            account.transfer_to(account, 10)

    def test_opposite_transfers_do_not_deadlock(self):
        """
        Transfer money in opposite directions between the same two accounts.

        Both threads should finish within the timeout. A barrier increases
        overlap so the test exercises the consistent lock-ordering rule.

        Completion within the timeout provides evidence that the chosen lock
        ordering prevents circular waiting in this transfer scenario.
        """
        account_a = BankAccount("ACC_A", 500)
        account_b = BankAccount("ACC_B", 500)

        initial_total = account_a.get_balance() + account_b.get_balance()
        barrier = threading.Barrier(2)

        def transfer_a_to_b():
            barrier.wait()

            for _ in range(100):
                account_a.transfer_to(account_b, 1)

        def transfer_b_to_a():
            barrier.wait()

            for _ in range(100):
                account_b.transfer_to(account_a, 1)

        # Daemon threads allow the test process to exit if a deadlock occurs.
        first = threading.Thread(target=transfer_a_to_b, daemon=True)
        second = threading.Thread(target=transfer_b_to_a, daemon=True)

        first.start()
        second.start()

        # A timeout prevents the test from waiting indefinitely.
        first.join(timeout=5)
        second.join(timeout=5)

        self.assertFalse(
            first.is_alive(),
            "First transfer thread did not finish.",
        )
        self.assertFalse(
            second.is_alive(),
            "Second transfer thread did not finish.",
        )

        final_total = account_a.get_balance() + account_b.get_balance()

        self.assertEqual(final_total, initial_total)
        self.assertEqual(account_a.get_balance(), Decimal("500"))
        self.assertEqual(account_b.get_balance(), Decimal("500"))


if __name__ == "__main__":
    unittest.main()
