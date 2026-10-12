"""Run concurrent deposits and withdrawals against one shared account."""

import threading
from decimal import Decimal

from bank_account import BankAccount


class TransactionSimulator:
    """
    Simulate several users accessing the same bank account concurrently.

    Each user follows the same transaction pattern so the expected final
    balance can be calculated and checked after the simulation.
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
        """Run one user's sequence of deposits and withdrawals."""
        amount = Decimal("10")

        for operation in range(self.operations_per_user):
            # Alternating equal deposits and withdrawals makes the expected
            # balance easy to calculate after all users have finished.
            if operation % 2 == 0:
                self.account.deposit(amount)
            else:
                self.account.withdraw(amount)

    def run(self) -> Decimal:
        """
        Start all user threads, wait for them, and return the final balance.

        A separate thread represents each simulated user accessing the shared
        BankAccount instance.
        """
        threads = []

        for user_number in range(1, self.num_users + 1):
            thread = threading.Thread(
                target=self._user_session,
                name=f"User-{user_number}",
            )
            threads.append(thread)
            thread.start()

        # The final balance is only checked after every user has finished.
        for thread in threads:
            thread.join()

        return self.account.get_balance()


if __name__ == "__main__":
    starting_balance = Decimal("1000")
    account = BankAccount("ACC_DEMO", starting_balance)

    simulator = TransactionSimulator(
        account,
        num_users=10,
        operations_per_user=100,
    )

    final_balance = simulator.run()

    print(f"Starting balance:      £{starting_balance}")
    print(f"Expected final balance: £{starting_balance}")
    print(f"Actual final balance:   £{final_balance}")
