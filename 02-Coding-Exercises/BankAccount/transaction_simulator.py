"""Run concurrent deposits and withdrawals against one shared account."""

import threading
from decimal import Decimal

from bank_account import BankAccount


class TransactionSimulator:
    """
    Simulate several users accessing the same bank account concurrently.

    Each user follows a fixed pattern of deposits and withdrawals so the
    expected final balance can be calculated in advance. Comparing expected
    and actual balances provides evidence that concurrent operations preserve
    the expected account state in this simulation.
    """

    def __init__(
        self,
        account: BankAccount,
        num_users: int,
        operations_per_user: int,
    ) -> None:
        if num_users <= 0 or operations_per_user <= 0:
            raise ValueError("Users and operations must be greater than zero.")

        self.account = account
        self.num_users = num_users
        self.operations_per_user = operations_per_user

    def _user_session(self) -> None:
        """
        Run one user's sequence of deposits and withdrawals.

        Each user session runs in its own thread and shares the same BankAccount
        instance with the other users. The alternating pattern creates
        contention while keeping the expected final balance easy to calculate.
        """
        amount = Decimal("10")

        for operation in range(self.operations_per_user):
            if operation % 2 == 0:
                self.account.deposit(amount)
            else:
                self.account.withdraw(amount)

    def run(self) -> Decimal:
        """
        Start all user threads, wait for them, and return the final balance.

        One thread represents each simulated user. All threads finish before
        the balance is read so no simulated operations remain in progress.
        """
        threads = []

        for user_number in range(1, self.num_users + 1):
            thread = threading.Thread(
                target=self._user_session,
                name=f"User-{user_number}",
            )
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        return self.account.get_balance()


if __name__ == "__main__":
    starting_balance = Decimal("1000")
    num_users = 10
    operations_per_user = 100
    transaction_amount = Decimal("10")

    account = BankAccount("ACC_DEMO", starting_balance)

    simulator = TransactionSimulator(
        account,
        num_users=num_users,
        operations_per_user=operations_per_user,
    )

    final_balance = simulator.run()

    deposits_per_user = (operations_per_user + 1) // 2
    withdrawals_per_user = operations_per_user // 2

    expected_final_balance = starting_balance + (
        num_users * (deposits_per_user - withdrawals_per_user) * transaction_amount
    )

    print(f"Starting balance:       £{starting_balance}")
    print(f"Expected final balance: £{expected_final_balance}")
    print(f"Actual final balance:   £{final_balance}")
