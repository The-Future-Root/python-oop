import unittest

from exercise import Money


class TestCreating(unittest.TestCase):
    def test_rounds_and_capitalises(self):
        m = Money(12.499, "usd")
        self.assertEqual(m.amount, 12.5)
        self.assertEqual(m.currency, "USD")

    def test_default_currency(self):
        self.assertEqual(Money(5).currency, "USD")


class TestPrinting(unittest.TestCase):
    def test_str_symbols(self):
        self.assertEqual(str(Money(12.5)), "$12.50")
        self.assertEqual(str(Money(8, "EUR")), "€8.00")
        self.assertEqual(str(Money(3.2, "GBP")), "£3.20")

    def test_str_other_currency(self):
        self.assertEqual(str(Money(12.5, "CAD")), "12.50 CAD")

    def test_repr(self):
        self.assertEqual(repr(Money(12.5)), "Money(12.5, 'USD')")
        self.assertEqual(repr([Money(3, "EUR")]), "[Money(3, 'EUR')]")

    def test_fstring(self):
        self.assertEqual(f"Total: {Money(41.99)}", "Total: $41.99")


class TestArithmetic(unittest.TestCase):
    def test_add(self):
        total = Money(24.99) + Money(17)
        self.assertEqual(total, Money(41.99))

    def test_add_returns_new_object(self):
        a, b = Money(1), Money(2)
        a + b
        self.assertEqual((a.amount, b.amount), (1, 2), "+ shouldn't change either side")

    def test_subtract(self):
        self.assertEqual(Money(10) - Money(2.5), Money(7.5))

    def test_multiply(self):
        self.assertEqual(Money(8.5) * 3, Money(25.5))

    def test_different_currencies(self):
        with self.assertRaises(ValueError) as caught:
            Money(5, "USD") + Money(5, "EUR")
        self.assertEqual(str(caught.exception), "Can't combine USD and EUR")
        with self.assertRaises(ValueError):
            Money(5, "GBP") - Money(1, "USD")

    def test_sum(self):
        self.assertEqual(sum([Money(1), Money(2), Money(3.5)]), Money(6.5))


class TestComparing(unittest.TestCase):
    def test_equal(self):
        self.assertEqual(Money(12.5), Money(12.5))
        self.assertNotEqual(Money(12.5, "USD"), Money(12.5, "EUR"))

    def test_sorting(self):
        prices = [Money(9), Money(2.5), Money(5)]
        self.assertEqual(sorted(prices), [Money(2.5), Money(5), Money(9)])
        self.assertEqual(max(prices), Money(9))

    def test_compare_different_currencies(self):
        with self.assertRaises(ValueError):
            Money(1, "USD") < Money(2, "EUR")

    def test_hashable(self):
        self.assertEqual(len({Money(5), Money(5), Money(5, "EUR")}), 2)

    def test_bool(self):
        self.assertFalse(Money(0))
        self.assertTrue(Money(0.01))


if __name__ == "__main__":
    unittest.main()
