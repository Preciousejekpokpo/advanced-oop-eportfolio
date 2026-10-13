"""Test gaps in transaction recording when account balances change."""

import unittest
from unittest.mock import patch

from bank_account import BankAccount
from recording_account import RecordingAccount


class TestRecordingFailureModes(unittest.TestCase):
    """Check what happens when account activity is not fully recorded."""

    def test_recording_failure_does_not_undo_a_completed_deposit(self):
        account = BankAccount("FAILURE", 100)
        recorded = RecordingAccount(account)

        # Force recording to fail after the deposit has been processed.
        with patch.object(
            recorded, "_append", side_effect=OSError("Record unavailable")
        ):
            with self.assertRaises(OSError):
                recorded.deposit(25)

        self.assertEqual(account.get_balance(), 125)
        self.assertEqual(recorded.records(), ())

    def test_two_wrappers_have_incomplete_individual_histories(self):
        account = BankAccount("SHARED", 100)
        first = RecordingAccount(account)
        second = RecordingAccount(account)

        first.deposit(10)
        second.deposit(20)

        self.assertEqual(account.get_balance(), 130)
        self.assertEqual(len(first.records()), 1)
        self.assertEqual(len(second.records()), 1)
        self.assertNotEqual(first.records(), second.records())


if __name__ == "__main__":
    unittest.main()
