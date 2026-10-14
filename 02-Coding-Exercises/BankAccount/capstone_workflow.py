"""Coordinate a recorded banking scenario and optional model review."""

from model_review import ModelReviewService, ReviewModel, ReviewResult
from recording_account import RecordingAccount
from scenario_factories import BankingScenario


class CapstoneWorkflow:
    """
    Run a recorded banking scenario and examine its transaction evidence.

    The additional count check compares scheduled operations with recorded
    attempts. This can reveal omissions that cancel out financially, but it
    cannot prove that every record is accurate or complete.
    """

    def __init__(self, model: ReviewModel) -> None:
        self._review_service = ModelReviewService(model)

    def run(self, scenario: BankingScenario) -> ReviewResult:
        """Run one fresh scenario before requesting any model advice."""
        if not isinstance(scenario, BankingScenario):
            raise TypeError("A BankingScenario is required.")

        if not isinstance(scenario.account, RecordingAccount):
            raise TypeError("The scenario must use a RecordingAccount.")

        if scenario.simulator.account is not scenario.account:
            raise ValueError("The simulator must use the scenario's account.")

        if scenario.account.records():
            raise ValueError("Use a fresh scenario with no previous records.")

        opening_balance = scenario.account.get_balance()

        # Use the scheduled operations to work out how many records we expect.
        expected_attempts = (
            scenario.simulator.num_users * scenario.simulator.operations_per_user
        )

        # If a worker fails, the simulation raises an error and stops the review.
        comparison = scenario.run()

        if not comparison.agrees:
            return ReviewResult("manual_review", "record_mismatch")

        records = scenario.account.records()

        # Missing deposits and withdrawals can cancel out, so check the count too.
        if len(records) != expected_attempts:
            return ReviewResult("manual_review", "record_count_mismatch")

        return self._review_service.assess(
            opening_balance,
            scenario.account.get_balance(),
            records,
        )
