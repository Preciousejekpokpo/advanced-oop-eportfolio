"""A small checkout design with separate order and payment responsibilities."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


def _as_decimal(value: object) -> Decimal:
    """Convert a number to a finite Decimal."""
    try:
        amount = Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError) as exc:
        raise ValueError("Enter a valid number.") from exc

    if not amount.is_finite():
        raise ValueError("Numbers must be finite.")

    return amount


@dataclass(frozen=True)
class Product:
    """Describe an item and its price."""

    name: str
    price: Decimal

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("Product name cannot be empty.")

        price = _as_decimal(self.price)

        if price < 0:
            raise ValueError("Product price cannot be negative.")

        object.__setattr__(self, "price", price)


class Order:
    """Manage cart items and calculate totals without handling payments."""

    def __init__(self) -> None:
        self._items: list[Product] = []

    def add_item(self, item: Product) -> None:
        """Add a valid product to the order."""
        if not isinstance(item, Product):
            raise TypeError("Order items must be Product instances.")

        self._items.append(item)

    def calculate_total(
        self,
        discount_rate: object = Decimal("0"),
    ) -> Decimal:
        """Calculate the discounted total, rounded to two decimal places."""
        rate = _as_decimal(discount_rate)

        if not Decimal("0") <= rate <= Decimal("1"):
            raise ValueError("Discount must be between 0 and 1.")

        subtotal = sum(
            (item.price for item in self._items),
            Decimal("0"),
        )

        discounted_total = subtotal * (Decimal("1") - rate)

        # Apply the rounding policy chosen for this exercise.
        return discounted_total.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )


class PaymentMethod(ABC):
    """Define the operation required of a payment provider."""

    @abstractmethod
    def pay(self, amount: Decimal) -> str:
        """Process the payment and return the provider's response."""


class PaymentProcessor:
    """Process an order using an externally supplied payment method."""

    def __init__(self, payment_method: PaymentMethod) -> None:
        self._payment_method = payment_method

    def process(
        self,
        order: Order,
        discount_rate: object = Decimal("0"),
    ) -> str:
        """Calculate the amount and pass it to the payment method."""
        amount = order.calculate_total(discount_rate)

        return self._payment_method.pay(amount)
