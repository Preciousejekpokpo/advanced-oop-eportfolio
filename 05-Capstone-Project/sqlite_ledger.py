"""Small SQLite experiment addressing the capstone's recording gap.

This is a separate proof of concept, not a replacement for BankAccount or
CapstoneWorkflow. It coordinates a balance change and its record in one
SQLite transaction, using a unique request ID to make retries idempotent.
"""

from __future__ import annotations

import sqlite3
from contextlib import closing
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Callable


def _pennies(value: object, *, require_positive: bool = False) -> int:
    """Accept finite whole-penny amounts, rejecting silent rounding."""
    if isinstance(value, bool):
        raise ValueError("Money must not be a boolean.")
    try:
        amount = Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError) as exc:
        raise ValueError("Invalid money amount.") from exc
    if not amount.is_finite() or amount * 100 != (amount * 100).to_integral_value():
        raise ValueError("Money must be finite and expressed in whole pennies.")
    cents = int(amount * 100)
    if require_positive and cents <= 0:
        raise ValueError("The transaction amount must be positive.")
    return cents


def _money(cents: int) -> Decimal:
    return Decimal(cents) / Decimal(100)


class SQLiteLedger:
    """Coordinate account balance and transaction history on one database.

    The optional callback is an explicit test seam. Tests inject exceptions or
    terminate a child process after the balance UPDATE but before the INSERT.
    """

    def __init__(
        self,
        path: str | Path,
        *,
        after_balance_write: Callable[[], None] | None = None,
    ) -> None:
        self.path = str(path)
        self._after_balance_write = after_balance_write
        with closing(self._connect()) as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS accounts (
                    account_id TEXT PRIMARY KEY,
                    balance_pence INTEGER NOT NULL CHECK (balance_pence >= 0)
                );
                CREATE TABLE IF NOT EXISTS movements (
                    request_id TEXT PRIMARY KEY,
                    account_id TEXT NOT NULL REFERENCES accounts(account_id),
                    delta_pence INTEGER NOT NULL CHECK (delta_pence != 0),
                    balance_after_pence INTEGER NOT NULL
                );
                """
            )

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path, timeout=10.0, isolation_level=None)
        connection.execute("PRAGMA foreign_keys=ON")
        return connection

    def open_account(self, account_id: str, opening_balance: object = "0.00") -> None:
        if not isinstance(account_id, str) or not account_id.strip():
            raise ValueError("Account ID is required.")
        balance = _pennies(opening_balance)
        if balance < 0:
            raise ValueError("Opening balance cannot be negative.")
        with closing(self._connect()) as connection:
            connection.execute(
                "INSERT INTO accounts(account_id, balance_pence) VALUES (?, ?)",
                (account_id, balance),
            )

    def balance(self, account_id: str) -> Decimal:
        with closing(self._connect()) as connection:
            row = connection.execute(
                "SELECT balance_pence FROM accounts WHERE account_id=?", (account_id,)
            ).fetchone()
        if row is None:
            raise ValueError("Unknown account.")
        return _money(row[0])

    def record_count(self, account_id: str) -> int:
        with closing(self._connect()) as connection:
            (count,) = connection.execute(
                "SELECT COUNT(*) FROM movements WHERE account_id=?", (account_id,)
            ).fetchone()
        return count

    def deposit(self, account_id: str, amount: object, request_id: str) -> Decimal:
        return self._apply(account_id, _pennies(amount, require_positive=True), request_id)

    def withdraw(self, account_id: str, amount: object, request_id: str) -> Decimal:
        return self._apply(account_id, -_pennies(amount, require_positive=True), request_id)

    def _apply(self, account_id: str, delta: int, request_id: str) -> Decimal:
        if not isinstance(request_id, str) or not request_id.strip():
            raise ValueError("A non-empty request ID is required.")
        connection = self._connect()
        try:
            # The write lock ensures concurrent writers serialize the whole check
            # and update, including the request-ID idempotency check.
            connection.execute("BEGIN IMMEDIATE")
            prior = connection.execute(
                "SELECT account_id, delta_pence, balance_after_pence "
                "FROM movements WHERE request_id=?", (request_id,)
            ).fetchone()
            if prior is not None:
                if prior[:2] != (account_id, delta):
                    raise ValueError("Request ID reused for different details.")
                connection.commit()
                return _money(prior[2])

            row = connection.execute(
                "SELECT balance_pence FROM accounts WHERE account_id=?", (account_id,)
            ).fetchone()
            if row is None:
                raise ValueError("Unknown account.")
            new_balance = row[0] + delta
            if new_balance < 0:
                raise ValueError("Insufficient funds.")

            connection.execute(
                "UPDATE accounts SET balance_pence=? WHERE account_id=?",
                (new_balance, account_id),
            )
            if self._after_balance_write is not None:
                self._after_balance_write()
            connection.execute(
                "INSERT INTO movements(request_id, account_id, delta_pence, balance_after_pence) "
                "VALUES (?, ?, ?, ?)", (request_id, account_id, delta, new_balance)
            )
            connection.commit()
            return _money(new_balance)
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()
