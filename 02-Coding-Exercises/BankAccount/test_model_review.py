"""Test transaction reviews using a mock instead of a live AI model."""

import unittest
from decimal import Decimal
from unittest.mock import Mock, patch

from bank_account import BankAccount
from model_review import (
    ModelReviewService,
    ModelUnavailableError,
    ReviewFacts,
    ReviewModel,
)
from recording_account import RecordingAccount, TransactionRecord


class TestModelReview(unittest.TestCase):
    """Check model responses, recording failures and review limitations."""

    def setUp(self):
        """Give each test a fresh account and an independent mock model."""
        self.opening_balance = Decimal("100")
        self.account = RecordingAccount(
            BankAccount("REVIEW_TEST", self.opening_balance)
        )

        # The mock replaces the model dependency without making API calls.
        self.model = Mock(spec=ReviewModel)
        self.service = ModelReviewService(self.model)

    def _review(self):
        """Review the completed account activity using its recorded history."""
        return self.service.assess(
            self.opening_balance,
            self.account.get_balance(),
            self.account.records(),
        )

    def test_model_receives_correct_summary(self):
        """Check that the model receives figures from both Visitor reports."""
        self.account.deposit(20)
        self.account.withdraw(5)
        self.assertFalse(self.account.withdraw(500))
        self.model.suggest.return_value = "flag"

        result = self._review()

        self.assertEqual(result.status, "advisory_only")
        self.assertEqual(result.model_label, "flag")

        # The failed withdrawal is recorded but does not reduce the balance.
        self.model.suggest.assert_called_once_with(
            ReviewFacts(
                net_movement=Decimal("15"),
                failed_attempts=1,
                recorded_attempts=3,
            )
        )

    def test_no_flag_does_not_mean_approved(self):
        """A reassuring model response must remain advisory."""
        self.account.deposit(10)
        self.model.suggest.return_value = "no_flag"

        result = self._review()

        self.assertEqual(result.status, "advisory_only")
        self.assertEqual(result.reason, "model_suggestion")
        self.assertEqual(result.model_label, "no_flag")
        self.model.suggest.assert_called_once()

    def test_record_mismatch_skips_model(self):
        """Do not consult the model when completed activity is unrecorded."""
        with patch.object(
            self.account,
            "_append",
            side_effect=OSError("Record unavailable"),
        ):
            with self.assertRaises(OSError):
                self.account.deposit(25)

        result = self._review()

        self.assertEqual(self.account.get_balance(), Decimal("125"))
        self.assertEqual(self.account.records(), ())
        self.assertEqual(result.status, "manual_review")
        self.assertEqual(result.reason, "record_mismatch")

        # The existing financial check takes priority over model advice.
        self.model.suggest.assert_not_called()

    def test_invalid_model_responses_require_manual_review(self):
        """Reject responses outside the two labels the service accepts."""
        invalid_responses = (None, "approve", "FLAG", 3, True)

        for response in invalid_responses:
            with self.subTest(response=response):
                self.model.suggest.return_value = response

                result = self._review()

                self.assertEqual(result.status, "manual_review")
                self.assertEqual(result.reason, "invalid_model_output")
                self.assertIsNone(result.model_label)

    def test_model_unavailable_requires_manual_review(self):
        """Handle an expected dependency failure without accepting advice."""
        self.model.suggest.side_effect = ModelUnavailableError("Model unavailable")

        result = self._review()

        self.assertEqual(result.status, "manual_review")
        self.assertEqual(result.reason, "model_unavailable")
        self.assertIsNone(result.model_label)

    def test_unexpected_model_error_is_not_hidden(self):
        """Unexpected programming errors should remain visible."""
        self.model.suggest.side_effect = RuntimeError("Unexpected model error")

        with self.assertRaisesRegex(RuntimeError, "Unexpected model error"):
            self._review()

    def test_review_does_not_modify_account_or_records(self):
        """The review must not change the financial state it examines."""
        self.account.deposit(10)
        balance_before = self.account.get_balance()
        records_before = self.account.records()
        self.model.suggest.return_value = "flag"

        self._review()

        self.assertEqual(self.account.get_balance(), balance_before)
        self.assertEqual(self.account.records(), records_before)

    def test_offsetting_missing_transactions_escape_balance_check(self):
        """Show how two missing records can leave matching net movements."""
        with patch.object(
            self.account,
            "_append",
            side_effect=OSError("Record unavailable"),
        ):
            with self.assertRaises(OSError):
                self.account.deposit(25)

            with self.assertRaises(OSError):
                self.account.withdraw(25)

        # Both balance changes completed, but neither record was saved.
        self.assertEqual(self.account.get_balance(), self.opening_balance)
        self.assertEqual(self.account.records(), ())

        self.model.suggest.return_value = "no_flag"
        result = self._review()

        # The service cannot identify omissions that cancel each other out.
        self.assertEqual(result.status, "advisory_only")
        self.assertEqual(result.model_label, "no_flag")
        self.model.suggest.assert_called_once_with(
            ReviewFacts(
                net_movement=Decimal("0"),
                failed_attempts=0,
                recorded_attempts=0,
            )
        )

    def test_unknown_transaction_type_is_rejected(self):
        """An unsupported operation should not enter a review unnoticed."""
        unknown_record = TransactionRecord("refund", Decimal("5"), True)

        with self.assertRaisesRegex(ValueError, "Unknown transaction operation"):
            self.service.assess(
                self.opening_balance,
                self.opening_balance,
                (unknown_record,),
            )

        self.model.suggest.assert_not_called()


if __name__ == "__main__":
    unittest.main()
