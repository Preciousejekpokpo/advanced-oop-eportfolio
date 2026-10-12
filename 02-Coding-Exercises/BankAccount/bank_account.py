"""Thread-safe bank account used for the concurrency assignment."""

import threading
from decimal import Decimal, InvalidOperation


class BankAccount:
    """
    Represent a bank account whose balance is protected by a lock.

    All balance reads and updates are synchronised using a per-account lock
    to prevent race conditions when multiple threads access the same account.
    """

    def __init__(self, account_number: str, balance=0) -> None:
        if not isinstance(account_number, str) or not account_number.strip():
            raise ValueError("Account number must be a non-empty string.")

        self.account_number = account_number.strip()
        self._balance = self._to_decimal(balance)

        if self._balance < 0:
            raise ValueError("Opening balance cannot be negative.")

        # The lock protects operations that read or change this account's balance.
        self._lock = threading.Lock()

    @staticmethod
    def _to_decimal(amount) -> Decimal:
        """Convert an amount to Decimal, rejecting invalid values."""
        try:
            value = Decimal(str(amount))
        except (InvalidOperation, ValueError, TypeError) as exc:
            raise ValueError("Amount must be a valid number.") from exc

        if not value.is_finite():
            raise ValueError("Amount must be a finite number.")

        return value

    @staticmethod
    def _validate_transaction_amount(amount) -> Decimal:
        """
        Return a valid positive transaction amount.

        Zero and negative values are rejected because deposits and withdrawals
        should represent positive transaction amounts.
        """
        value = BankAccount._to_decimal(amount)

        if value <= 0:
            raise ValueError("Transaction amount must be greater than zero.")

        return value

    def deposit(self, amount) -> Decimal:
        """
        Deposit money and return the new balance.

        The account lock prevents another thread from changing the balance
        while the deposit is being applied.
        """
        value = self._validate_transaction_amount(amount)

        with self._lock:
            self._balance += value
            return self._balance

    def withdraw(self, amount) -> bool:
        """
        Withdraw money if sufficient funds are available.

        The balance check and deduction use the same lock so another withdrawal
        cannot change the balance between the check and the update.
        """
        value = self._validate_transaction_amount(amount)

        with self._lock:
            if value > self._balance:
                return False

            self._balance -= value
            return True

    def get_balance(self) -> Decimal:
        """
        Return the current balance.

        The same account lock is used for reads so balance access follows the
        same synchronisation policy as deposits and withdrawals.
        """
        with self._lock:
            return self._balance

    def transfer_to(self, target: "BankAccount", amount) -> bool:
        """
        Transfer money to another account using a fixed lock order.

        Both account locks are acquired in a consistent order based on account
        number. This prevents circular waiting when two threads transfer money
        between the same accounts in opposite directions.
        """
        if not isinstance(target, BankAccount):
            raise TypeError("Target must be a BankAccount.")

        if target is self:
            raise ValueError("Source and target accounts must be different.")

        value = self._validate_transaction_amount(amount)

        # Account numbers are unique in the assignment, so every transfer
        # acquires the two locks in the same order.
        if self.account_number < target.account_number:
            first, second = self, target
        else:
            first, second = target, self

        # Both balances are changed while both account locks are held.
        with first._lock:
            with second._lock:
                if value > self._balance:
                    return False

                self._balance -= value
                target._balance += value
                return True
