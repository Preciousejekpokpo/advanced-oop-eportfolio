"""Tests for a shopping order and its payment handling."""

import unittest
from decimal import Decimal
from unittest.mock import Mock

from checkout import Order, Product, PaymentMethod, PaymentProcessor


class TestCheckout(unittest.TestCase):
    """Check order calculations and payment dependencies."""

    def setUp(self):
        self.order = Order()
        self.order.add_item(Product("Book", Decimal("20.00")))
        self.order.add_item(Product("Pen", Decimal("10.00")))

    def test_order_calculates_total(self):
        """The cart total should equal the sum of product prices."""
        self.assertEqual(
            self.order.calculate_total(),
            Decimal("30.00"),
        )

    def test_order_applies_discount(self):
        """A 10% discount should reduce the total correctly."""
        self.assertEqual(
            self.order.calculate_total(Decimal("0.10")),
            Decimal("27.00"),
        )

    def test_invalid_discounts_are_rejected(self):
        """Discount rates outside the allowed range should fail."""
        for rate in (Decimal("-0.10"), Decimal("1.10")):
            with self.subTest(rate=rate):
                with self.assertRaises(ValueError):
                    self.order.calculate_total(rate)

    def test_negative_product_price_is_rejected(self):
        """A product should not accept a negative price."""
        with self.assertRaises(ValueError):
            Product("Invalid", Decimal("-5.00"))

    def test_payment_method_can_be_mocked(self):
        """Payment processing should work with an injected mock."""
        payment = Mock(spec=PaymentMethod)
        payment.pay.return_value = "approved"

        processor = PaymentProcessor(payment)
        result = processor.process(
            self.order,
            Decimal("0.10"),
        )

        self.assertEqual(result, "approved")
        payment.pay.assert_called_once_with(Decimal("27.00"))

    def test_payment_error_is_not_hidden(self):
        """A payment failure should be visible to the caller."""
        payment = Mock(spec=PaymentMethod)
        payment.pay.side_effect = ConnectionError("Payment unavailable")

        processor = PaymentProcessor(payment)

        with self.assertRaises(ConnectionError):
            processor.process(self.order)

    def test_discount_total_is_rounded_to_pennies(self):
        """A discounted total should use two decimal places."""
        order = Order()
        order.add_item(Product("Notebook", Decimal("19.99")))

        total = order.calculate_total(Decimal("0.15"))

        self.assertEqual(total, Decimal("16.99"))


if __name__ == "__main__":
    unittest.main()
