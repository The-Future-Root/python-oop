import unittest

from exercise import Product


class TestCreating(unittest.TestCase):
    def test_attributes(self):
        lamp = Product("Desk lamp", 24.99, 10)
        self.assertEqual((lamp.name, lamp.price, lamp.stock), ("Desk lamp", 24.99, 10))

    def test_stock_defaults_to_zero(self):
        self.assertEqual(Product("Mug", 8.5).stock, 0)

    def test_objects_are_separate(self):
        a = Product("A", 1, 5)
        b = Product("B", 2, 5)
        a.restock(10)
        self.assertEqual(b.stock, 5, "Changing one product shouldn't change another")


class TestStock(unittest.TestCase):
    def test_in_stock(self):
        self.assertIs(Product("Lamp", 24.99, 1).in_stock(), True)
        self.assertIs(Product("Lamp", 24.99, 0).in_stock(), False)

    def test_restock(self):
        lamp = Product("Lamp", 24.99, 2)
        lamp.restock(5)
        self.assertEqual(lamp.stock, 7)

    def test_sell(self):
        lamp = Product("Lamp", 24.99, 10)
        self.assertEqual(lamp.sell(3), 74.97)
        self.assertEqual(lamp.stock, 7)

    def test_sell_too_many(self):
        lamp = Product("Lamp", 24.99, 3)
        with self.assertRaises(ValueError) as caught:
            lamp.sell(5)
        self.assertEqual(str(caught.exception), "Only 3 left")
        self.assertEqual(lamp.stock, 3, "A failed sale shouldn't change the stock")

    def test_stock_value(self):
        self.assertEqual(Product("Mug", 8.5, 40).stock_value(), 340.0)
        self.assertEqual(Product("Pen", 0.99, 3).stock_value(), 2.97)


class TestLabel(unittest.TestCase):
    def test_in_stock_label(self):
        self.assertEqual(Product("Desk lamp", 24.99, 10).label(), "Desk lamp: $24.99 (10 in stock)")

    def test_out_of_stock_label(self):
        self.assertEqual(Product("Desk lamp", 24.99).label(), "Desk lamp: $24.99 (out of stock)")

    def test_two_decimal_places(self):
        self.assertEqual(Product("Mug", 8.5, 1).label(), "Mug: $8.50 (1 in stock)")


if __name__ == "__main__":
    unittest.main()
