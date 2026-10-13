"""Build compatible banking experiments with different forms of evidence."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal

from bank_account import BankAccount
from recording_account import RecordingAccount
from strategy_simulator import (
    AlternatingTransactions,
    DepositOnlyTransactions,
    StrategySimulator,
    TransactionStrategy,
)
from transaction_visitors import CashFlowVisitor, visit_records


@dataclass(frozen=True)
class EvidenceComparison:
    """Compare the actual balance movement with a separate source of evidence."""

    actual_change: Decimal
    comparison_change: Decimal
    agrees: bool


class EvidenceCheck(ABC):
    """Define the check used after a scenario has finished."""

    @abstractmethod
    def evaluate(self, closing_balance: Decimal) -> EvidenceComparison:
        """Compare the closing balance with the scenario's expected evidence."""


class ScheduledBalanceCheck(EvidenceCheck):
    """Compare the balance change with the alternating workload's expected net."""

    def __init__(self, opening_balance: Decimal, expected_change: Decimal) -> None:
        self._opening_balance = opening_balance
        self._expected_change = expected_change

    def evaluate(self, closing_balance: Decimal) -> EvidenceComparison:
        actual_change = closing_balance - self._opening_balance
        return EvidenceComparison(
            actual_change,
            self._expected_change,
            actual_change == self._expected_change,
        )


class RecordedMovementCheck(EvidenceCheck):
    """Compare actual movement with the available Decorator records."""

    def __init__(self, account: RecordingAccount, opening_balance: Decimal) -> None:
        if not isinstance(account, RecordingAccount):
            raise TypeError("Recorded checks need an account with transaction records.")
        self._account = account
        self._opening_balance = opening_balance

    def evaluate(self, closing_balance: Decimal) -> EvidenceComparison:
        flow = CashFlowVisitor()
        # The visitor can analyse a snapshot, but cannot restore missing records.
        visit_records(self._account.records(), flow)
        actual_change = closing_balance - self._opening_balance
        recorded_change = flow.summary().net_change
        return EvidenceComparison(
            actual_change,
            recorded_change,
            actual_change == recorded_change,
        )


@dataclass
class BankingScenario:
    """Keep the configured account, workload and evidence check together."""

    account: BankAccount | RecordingAccount
    simulator: StrategySimulator
    evidence_check: EvidenceCheck

    def run(self) -> EvidenceComparison:
        """Finish all workers before comparing the closing balance."""
        closing_balance = self.simulator.run()
        return self.evidence_check.evaluate(closing_balance)


class ScenarioFactory(ABC):
    """Create a compatible account, transaction policy and evidence check."""

    @abstractmethod
    def create_account(self, number: str, opening_balance: object) -> BankAccount | RecordingAccount:
        """Create the account used by this scenario family."""

    @abstractmethod
    def create_strategy(self) -> TransactionStrategy:
        """Choose the family-specific transaction workload."""

    @abstractmethod
    def create_check(
        self, account: BankAccount | RecordingAccount,
        opening_balance: Decimal,
        simulator: StrategySimulator,
    ) -> EvidenceCheck:
        """Build a check compatible with the account and its workload."""

    def build(
        self,
        number: str,
        opening_balance: object,
        num_users: int,
        operations_per_user: int,
        amount: object = Decimal("10"),
    ) -> BankingScenario:
        account = self.create_account(number, opening_balance)
        simulator = StrategySimulator(
            account, num_users, operations_per_user, self.create_strategy(), amount
        )
        # Read the validated starting balance and amount from the built objects.
        evidence_check = self.create_check(
            account, account.get_balance(), simulator
        )
        return BankingScenario(account, simulator, evidence_check)


class BalanceScenarioFactory(ScenarioFactory):
    """Pair a plain account with an alternating workload and a balance check."""

    def create_account(self, number: str, opening_balance: object) -> BankAccount:
        return BankAccount(number, opening_balance)

    def create_strategy(self) -> TransactionStrategy:
        return AlternatingTransactions()

    def create_check(
        self, account: BankAccount | RecordingAccount,
        opening_balance: Decimal,
        simulator: StrategySimulator,
    ) -> EvidenceCheck:
        if not isinstance(account, BankAccount):
            raise TypeError("Balance scenarios require a plain BankAccount.")
        # Each user starts with a deposit. Odd workloads leave one extra deposit.
        expected_change = (
            simulator.num_users
            * (simulator.operations_per_user % 2)
            * simulator.transaction_amount
        )
        return ScheduledBalanceCheck(opening_balance, expected_change)


class RecordedScenarioFactory(ScenarioFactory):
    """Pair a recording wrapper with deposits and a record-comparison check."""

    def create_account(self, number: str, opening_balance: object) -> RecordingAccount:
        return RecordingAccount(BankAccount(number, opening_balance))

    def create_strategy(self) -> TransactionStrategy:
        return DepositOnlyTransactions()

    def create_check(
        self, account: BankAccount | RecordingAccount,
        opening_balance: Decimal,
        simulator: StrategySimulator,
    ) -> EvidenceCheck:
        if not isinstance(account, RecordingAccount):
            raise TypeError("Recorded scenarios require a RecordingAccount.")
        return RecordedMovementCheck(account, opening_balance)


if __name__ == "__main__":
    balance_scenario = BalanceScenarioFactory().build("BALANCE_DEMO", 100, 2, 4, 5)
    balance_check = balance_scenario.run()
    print(
        f"Balance scenario £{balance_scenario.account.get_balance()}, "
        f"check agrees={balance_check.agrees}"
    )

    recorded_scenario = RecordedScenarioFactory().build("RECORD_DEMO", 100, 2, 4, 5)
    record_check = recorded_scenario.run()
    print(
        f"Recorded scenario £{recorded_scenario.account.get_balance()}, "
        f"records={len(recorded_scenario.account.records())}, "
        f"check agrees={record_check.agrees}"
    )
