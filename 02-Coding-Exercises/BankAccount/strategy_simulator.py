"""Compare transaction workloads without changing the BankAccount class."""

import threading
from abc import ABC, abstractmethod
from decimal import Decimal, InvalidOperation

from bank_account import BankAccount


class TransactionStrategy(ABC):
    """Define how one simulated transaction is selected and performed."""

    @abstractmethod
    def apply(self, account: BankAccount, operation: int, amount: Decimal) -> None:
        """Perform the transaction for the given position in a user session."""


class AlternatingTransactions(TransactionStrategy):
    """Alternate deposits and withdrawals, beginning with a deposit."""

    def apply(self, account: BankAccount, operation: int, amount: Decimal) -> None:
        if operation % 2 == 0:
            account.deposit(amount)
        elif not account.withdraw(amount):
            # Do not treat a rejected withdrawal as a successful simulation.
            raise RuntimeError("The account could not fund a scheduled withdrawal.")


class DepositOnlyTransactions(TransactionStrategy):
    """Use repeated deposits to exercise updates to a shared balance."""

    def apply(self, account: BankAccount, operation: int, amount: Decimal) -> None:
        account.deposit(amount)


class StrategySimulator:
    """Run user threads with an interchangeable transaction strategy."""

    def __init__(
        self,
        account: BankAccount,
        num_users: int,
        operations_per_user: int,
        strategy: TransactionStrategy,
        transaction_amount: Decimal = Decimal("10"),
    ) -> None:
        if num_users <= 0 or operations_per_user <= 0:
            raise ValueError("Users and operations must be greater than zero.")
        if not isinstance(strategy, TransactionStrategy):
            raise TypeError("Strategy must implement TransactionStrategy.")

        try:
            amount = Decimal(str(transaction_amount))
        except (InvalidOperation, ValueError, TypeError) as exc:
            raise ValueError("Transaction amount must be a valid number.") from exc

        if not amount.is_finite() or amount <= 0:
            raise ValueError("Transaction amount must be positive and finite.")

        self.account = account
        self.num_users = num_users
        self.operations_per_user = operations_per_user
        self.strategy = strategy
        self.transaction_amount = amount

    def set_strategy(self, strategy: TransactionStrategy) -> None:
        """Choose a different workload for the next call to run()."""
        if not isinstance(strategy, TransactionStrategy):
            raise TypeError("Strategy must implement TransactionStrategy.")
        self.strategy = strategy

    def run(self) -> Decimal:
        """Wait for all users and report worker failures to the caller."""
        errors = [None] * self.num_users
        threads = []

        # Take a snapshot so each worker uses the same policy for this run.
        active_strategy = self.strategy

        def user_session(index: int) -> None:
            try:
                for operation in range(self.operations_per_user):
                    active_strategy.apply(
                        self.account, operation, self.transaction_amount
                    )
            except Exception as exc:
                # An exception in a worker thread must not be silently ignored.
                errors[index] = exc

        for user_number in range(self.num_users):
            thread = threading.Thread(
                target=user_session,
                args=(user_number,),
                name=f"User-{user_number + 1}",
            )
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        for error in errors:
            if error is not None:
                raise RuntimeError("A simulated user could not finish.") from error

        return self.account.get_balance()


if __name__ == "__main__":
    account = BankAccount("STRATEGY_DEMO", 100)
    simulator = StrategySimulator(account, 4, 10, AlternatingTransactions())

    print(f"After alternating transactions  £{simulator.run()}")

    simulator.set_strategy(DepositOnlyTransactions())
    print(f"After deposit-only transactions £{simulator.run()}")
