# SOLID Checkout Refactoring and Testing

The Unit 2 shopping-cart example combines cart management, totals and payment selection in `Order`. I separated payment responsibilities through `PaymentProcessor` and an injected `PaymentMethod`, allowing a mock to replace a provider during testing. `Product` rejects invalid prices, while `Order` calculates discounted totals using `Decimal`.

Six initial tests passed, but none addressed fractional pennies. I added a test expecting £16.99 for an item costing £19.99 with a 15% discount. It failed when the implementation returned £16.9915. Applying `ROUND_HALF_UP` to the final total brought the local suite to seven passing tests in 0.003 seconds. This provides an observed red–green change for rounding, not proof that the whole design followed test-first development.

The Unit 8 refactoring example also cautions against adding complexity automatically. A single discount parameter is sufficient here, whereas separate Strategy classes would need a stronger change requirement. The abstract payment contract enables substitution in tests, but no real providers or integrations have been evaluated.

## Evidence

- [Checkout implementation](checkout.py)
- [Seven unit tests](test_checkout.py)