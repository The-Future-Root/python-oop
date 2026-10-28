# Lesson 1: a product with stock control
#
# Finish the Product class. The table in README.md says what each method does.
# Replace each `pass` with your code. Test with:  python3 -m unittest -v


class Product:
    def __init__(self, name, price, stock=0):
        """Store name, price and stock as attributes."""
        pass

    def in_stock(self):
        """Return True if there's at least one in stock."""
        pass

    def restock(self, quantity):
        """Add quantity to the stock."""
        pass

    def sell(self, quantity):
        """Remove quantity from the stock and return the cost, rounded to 2 decimal places.
        Raise ValueError("Only 3 left") (with the real number) if there aren't enough."""
        pass

    def stock_value(self):
        """Return price times stock, rounded to 2 decimal places."""
        pass

    def label(self):
        """Return "Desk lamp: $24.99 (10 in stock)" or "Desk lamp: $24.99 (out of stock)"."""
        pass


if __name__ == "__main__":
    lamp = Product("Desk lamp", 24.99, 10)
    print(lamp.label())
    print("Sold 3 for", lamp.sell(3))
    print(lamp.label())
