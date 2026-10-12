"""Bank account implementation with thread-safe balance operations."""

import threading
from decimal import Decimal, InvalidOperation


class BankAccount:
    """
    Represent a bank account with thread-safe balance operations.

    Deposits, withdrawals and balance reads use a per-account lock to prevent
    race conditions. Each method that touches the balance defines a critical
    section protected by this lock.

    Transfers acquire both account locks in a consistent order to prevent
    circular waiting between concurrent transfers using this method.
    """

    def __init__(self, account_number: str, balance=0) -> None:
        if not isinstance(account_number, str) or not account_number.strip():
            raise ValueError("Account number must be a non-empty string.")

        self.account_number = account_number.strip()
        self._balance = self._to_decimal(balance)

        if self._balance < 0:
            raise ValueError("Opening balance cannot be negative.")

        # One lock per account protects balance reads and updates.
        self._lock = threading.Lock()

    @staticmethod
    def _to_decimal(amount: object) -> Decimal:
        """Convert an amount to Decimal, rejecting invalid values."""
        try:
            value = Decimal(str(amount))
        except (InvalidOperation, ValueError, TypeError) as exc:
            raise ValueError("Amount must be a valid number.") from exc

        if not value.is_finite():
            raise ValueError("Amount must be a finite number.")

        return value

    @staticmethod
    def _validate_transaction_amount(amount: object) -> Decimal:
        """Return a valid positive transaction amount."""
        value = BankAccount._to_decimal(amount)

        if value <= 0:
            raise ValueError("Transaction amount must be greater than zero.")

        return value

    def deposit(self, amount: object) -> Decimal:
        """
        Deposit money and return the new balance.

        The increment and return occur inside one critical section so another
        locked operation cannot modify the balance during the update.
        """
        value = self._validate_transaction_amount(amount)

        with self._lock:
            self._balance += value
            return self._balance

    def withdraw(self, amount: object) -> bool:
        """
        Withdraw money if sufficient funds are available.

        Return True when the withdrawal succeeds and False when the account
        does not contain enough funds.
        """
        value = self._validate_transaction_amount(amount)

        # The funds check and deduction form one critical section.
        with self._lock:
            if value > self._balance:
                return False

            self._balance -= value
            return True

    def get_balance(self) -> Decimal:
        """
        Return the current balance safely.

        The read occurs while holding the account lock so it cannot interleave
        with another operation using the same lock.
        """
        with self._lock:
            return self._balance

    def transfer_to(self, target: "BankAccount", amount: object) -> bool:
        """
        Transfer money to another account using a consistent lock order.

        Both account locks are acquired before either balance is changed,
        making the transfer atomic with respect to operations using those
        account locks.

        Consistent lock acquisition prevents circular waiting when concurrent
        transfers use this method.
        """
        if not isinstance(target, BankAccount):
            raise TypeError("Target must be a BankAccount.")

        if target is self:
            raise ValueError("Source and target accounts must be different.")

        value = self._validate_transaction_amount(amount)

        # Account number provides the normal ordering key. Object identity
        # provides a consistent tie-breaker for the two live objects if
        # duplicate account numbers exist.
        first, second = sorted(
            (self, target),
            key=lambda account: (account.account_number, id(account)),
        )

        # Both balances change while both locks are held.
        with first._lock:
            with second._lock:
                if value > self._balance:
                    return False

                self._balance -= value
                target._balance += value
                return True
