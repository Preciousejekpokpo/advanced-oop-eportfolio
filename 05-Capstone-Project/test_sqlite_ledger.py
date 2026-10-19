"""Failure-led checks for the separate SQLite transaction proof of concept."""

import os
import subprocess
import sys
import tempfile
import threading
import unittest
from decimal import Decimal
from pathlib import Path

from sqlite_ledger import SQLiteLedger


class TestSQLiteLedger(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.db_path = Path(self.folder.name) / "account.db"
        self.ledger = SQLiteLedger(self.db_path)
        self.ledger.open_account("ACC", "100.00")

    def test_successful_deposit_commits_balance_and_record(self):
        self.assertEqual(self.ledger.deposit("ACC", "25.00", "deposit-1"), Decimal("125"))
        self.assertEqual(self.ledger.balance("ACC"), Decimal("125"))
        self.assertEqual(self.ledger.record_count("ACC"), 1)

    def test_injected_exception_rolls_back_balance_and_record(self):
        def fail_recording():
            raise OSError("Simulated interruption before record INSERT")

        failed = SQLiteLedger(self.db_path, after_balance_write=fail_recording)
        with self.assertRaises(OSError):
            failed.deposit("ACC", "25.00", "failed-request")
        self.assertEqual(self.ledger.balance("ACC"), Decimal("100"))
        self.assertEqual(self.ledger.record_count("ACC"), 0)

    def test_process_termination_discards_uncommitted_balance_update(self):
        # Terminate a separate interpreter without cleanup or explicit rollback.
        code = (
            "import os, sys; from sqlite_ledger import SQLiteLedger; "
            "bank = SQLiteLedger(sys.argv[1], after_balance_write=lambda: os._exit(17)); "
            "bank.deposit('ACC', '25.00', 'crashed-request')"
        )
        result = subprocess.run(
            [sys.executable, "-c", code, str(self.db_path)],
            cwd=Path(__file__).resolve().parent,
            capture_output=True, text=True, timeout=10, check=False,
        )
        self.assertEqual(result.returncode, 17, result.stderr)
        reopened = SQLiteLedger(self.db_path)
        self.assertEqual(reopened.balance("ACC"), Decimal("100"))
        self.assertEqual(reopened.record_count("ACC"), 0)

    def test_retry_uses_original_request_without_duplicate_credit(self):
        self.ledger.deposit("ACC", "25.00", "same-request")
        self.ledger.deposit("ACC", "25.00", "same-request")
        self.assertEqual(self.ledger.balance("ACC"), Decimal("125"))
        self.assertEqual(self.ledger.record_count("ACC"), 1)
        with self.assertRaises(ValueError):
            self.ledger.deposit("ACC", "30.00", "same-request")

    def test_withdrawal_and_insufficient_funds(self):
        self.assertEqual(self.ledger.withdraw("ACC", "20.00", "withdraw-1"), Decimal("80"))
        with self.assertRaises(ValueError):
            self.ledger.withdraw("ACC", "100.00", "withdraw-2")
        self.assertEqual(self.ledger.balance("ACC"), Decimal("80"))
        self.assertEqual(self.ledger.record_count("ACC"), 1)

    def test_reopening_database_preserves_committed_evidence(self):
        self.ledger.deposit("ACC", "3.50", "persisted")
        reopened = SQLiteLedger(self.db_path)
        self.assertEqual(reopened.balance("ACC"), Decimal("103.50"))
        self.assertEqual(reopened.record_count("ACC"), 1)

    def test_rejects_fractional_pennies_and_invalid_amounts(self):
        for invalid in ("0", "-1", "1.001", "NaN", True):
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    self.ledger.deposit("ACC", invalid, "bad")
        self.assertEqual(self.ledger.record_count("ACC"), 0)

    def test_concurrent_requests_do_not_lose_updates(self):
        failures = []
        def worker(index):
            try:
                SQLiteLedger(self.db_path).deposit("ACC", "1.00", f"req-{index}")
            except Exception as exc:
                failures.append(exc)
        threads = [threading.Thread(target=worker, args=(index,)) for index in range(20)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(timeout=10)
        self.assertFalse(failures)
        self.assertTrue(all(not thread.is_alive() for thread in threads))
        self.assertEqual(self.ledger.balance("ACC"), Decimal("120"))
        self.assertEqual(self.ledger.record_count("ACC"), 20)


if __name__ == "__main__":
    unittest.main()
