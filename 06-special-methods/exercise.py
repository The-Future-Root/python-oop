# Lesson 6: money
#
# Write the Money class. The table in README.md lists every special method it needs.
# Test with:  python3 -m unittest -v


class Money:
    def __init__(self, amount, currency="USD"):
        """Store amount rounded to 2 decimal places, and currency in capitals."""
        pass

    # Add __str__, __repr__, __add__, __sub__, __mul__, __eq__, __lt__,
    # __hash__, __bool__ and __radd__ here.


if __name__ == "__main__":
    lamp = Money(24.99)
    mugs = Money(8.50) * 2
    print(lamp, "+", mugs, "=", lamp + mugs)
