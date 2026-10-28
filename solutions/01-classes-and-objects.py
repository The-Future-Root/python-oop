# Solution to lesson 1: a product with stock control


class Product:
    def __init__(self, name, price, stock=0):
        """Store name, price and stock as attributes."""
        self.name = name
        self.price = price
        self.stock = stock

    def in_stock(self):
        """Return True if there's at least one in stock."""
        return self.stock > 0

    def restock(self, quantity):
        """Add quantity to the stock."""
        self.stock += quantity

    def sell(self, quantity):
        """Remove quantity from the stock and return the cost, rounded to 2 decimal places."""
        if quantity > self.stock:
            raise ValueError(f"Only {self.stock} left")
        self.stock -= quantity
        return round(self.price * quantity, 2)

    def stock_value(self):
        """Return price times stock, rounded to 2 decimal places."""
        return round(self.price * self.stock, 2)

    def label(self):
        """Return "Desk lamp: $24.99 (10 in stock)" or "Desk lamp: $24.99 (out of stock)"."""
        if self.in_stock():
            return f"{self.name}: ${self.price:.2f} ({self.stock} in stock)"
        return f"{self.name}: ${self.price:.2f} (out of stock)"


if __name__ == "__main__":
    lamp = Product("Desk lamp", 24.99, 10)
    print(lamp.label())
    print("Sold 3 for", lamp.sell(3))
    print(lamp.label())
