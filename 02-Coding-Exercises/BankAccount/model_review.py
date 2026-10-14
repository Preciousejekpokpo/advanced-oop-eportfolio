"""Review account activity using recorded evidence and optional model advice."""

from dataclasses import dataclass
from decimal import Decimal
from typing import Protocol

from recording_account import TransactionRecord
from transaction_visitors import (
    CashFlowVisitor,
    FailedAttemptVisitor,
    visit_records,
)


@dataclass(frozen=True)
class ReviewFacts:
    """Hold the summary figures available to the review model."""

    net_movement: Decimal
    failed_attempts: int
    recorded_attempts: int


class ReviewModel(Protocol):
    """Define a model interface that can be replaced with a mock during testing."""

    def suggest(self, facts: ReviewFacts) -> str:
        """Return 'flag' or 'no_flag' as an advisory suggestion."""
        ...


class ModelUnavailableError(RuntimeError):
    """Indicate that the model could not provide a response."""


@dataclass(frozen=True)
class ReviewResult:
    """Separate the review status from any suggestion made by the model."""

    status: str
    reason: str
    model_label: str | None = None


class ModelReviewService:
    """
    Review recorded account activity before requesting model advice.

    The existing Visitor classes provide the financial summary and failed
    attempts. The service checks these against the balance movement without
    modifying the account or its records.

    The workload must finish before the balances and records are collected.
    Matching totals alone cannot guarantee that every transaction was recorded.
    """

    def __init__(self, model: ReviewModel) -> None:
        # Supplying the model separately allows tests to control its responses.
        self._model = model

    def assess(
        self,
        opening_balance: Decimal,
        closing_balance: Decimal,
        records: tuple[TransactionRecord, ...],
    ) -> ReviewResult:
        """
        Compare actual balance movement with the available records.

        Both visitors use the same snapshot. A mismatch requires manual
        review before any model suggestion is considered.
        """

        cash_flow = CashFlowVisitor()
        failed_attempts = FailedAttemptVisitor()

        # Both reports must describe the same recorded activity.
        visit_records(records, cash_flow)
        visit_records(records, failed_attempts)

        actual_change = closing_balance - opening_balance
        recorded_change = cash_flow.summary().net_change

        # An unexplained balance difference cannot be resolved by model advice.
        if actual_change != recorded_change:
            return ReviewResult("manual_review", "record_mismatch")

        # Only aggregate figures are passed to the model.
        facts = ReviewFacts(
            net_movement=recorded_change,
            failed_attempts=len(failed_attempts.failures()),
            recorded_attempts=len(records),
        )

        try:
            suggestion = self._model.suggest(facts)
        except ModelUnavailableError:
            # Handle expected model failures without hiding other errors.
            return ReviewResult("manual_review", "model_unavailable")

        # Reject responses outside the two labels defined by the interface.
        if type(suggestion) is not str or suggestion not in {
            "flag",
            "no_flag",
        }:
            return ReviewResult("manual_review", "invalid_model_output")

        # A valid suggestion is not proof that the records are complete.
        return ReviewResult(
            status="advisory_only",
            reason="model_suggestion",
            model_label=suggestion,
        )
