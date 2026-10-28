import unittest

import exercise
from exercise import NoDiscount, best_discount


def get(name):
    cls = getattr(exercise, name, None)
    if cls is None:
        raise AssertionError(f"Write a class called {name} in exercise.py")
    return cls


class TestDiscounts(unittest.TestCase):
    def test_no_discount(self):
        self.assertEqual(NoDiscount().apply(8.50, 3), 25.5)
        self.assertEqual(NoDiscount().describe(), "No discount")

    def test_percent_off(self):
        d = get("PercentOff")(15)
        self.assertEqual(d.apply(8.50, 3), 21.68)
        self.assertEqual(d.describe(), "15% off")

    def test_amount_off(self):
        d = get("AmountOff")(5)
        self.assertEqual(d.apply(8.50, 3), 20.5)
        self.assertEqual(d.describe(), "$5.00 off")

    def test_amount_off_never_negative(self):
        self.assertEqual(get("AmountOff")(50).apply(8.50, 1), 0)

    def test_buy_x_get_one_free(self):
        d = get("BuyXGetOneFree")(2)
        self.assertEqual(d.apply(8.50, 3), 17.0)
        self.assertEqual(d.apply(8.50, 7), 42.5, "7 items with buy 2 get 1 free: 2 are free, so pay for 5")
        self.assertEqual(d.apply(8.50, 2), 17.0, "With only 2 items, none are free yet")
        self.assertEqual(d.describe(), "Buy 2, get 1 free")


class TestBestDiscount(unittest.TestCase):
    def test_picks_lowest(self):
        offers = [NoDiscount(), get("PercentOff")(15), get("AmountOff")(5), get("BuyXGetOneFree")(2)]
        self.assertIs(best_discount(offers, 8.50, 3), offers[3])
        self.assertIs(best_discount(offers, 8.50, 1), offers[2])

    def test_tie_returns_first(self):
        a, b = get("AmountOff")(10), get("AmountOff")(10)
        self.assertIs(best_discount([a, b], 20, 1), a)

    def test_works_with_any_discount(self):
        class HalfPrice:
            def apply(self, unit_price, quantity):
                return round(unit_price * quantity / 2, 2)

            def describe(self):
                return "Half price"

        half = HalfPrice()
        self.assertIs(best_discount([NoDiscount(), half], 10, 2), half,
                      "best_discount should work with any object that has apply(), without checking its class")


if __name__ == "__main__":
    unittest.main()
