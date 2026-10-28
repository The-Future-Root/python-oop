# Solution to lesson 6: money

SYMBOLS = {"USD": "$", "EUR": "€", "GBP": "£"}


class Money:
    def __init__(self, amount, currency="USD"):
        """Store amount rounded to 2 decimal places, and currency in capitals."""
        self.amount = round(amount, 2)
        self.currency = currency.upper()

    def __str__(self):
        symbol = SYMBOLS.get(self.currency)
        if symbol:
            return f"{symbol}{self.amount:.2f}"
        return f"{self.amount:.2f} {self.currency}"

    def __repr__(self):
        return f"Money({self.amount!r}, {self.currency!r})"

    def _check_same_currency(self, other):
        if self.currency != other.currency:
            raise ValueError(f"Can't combine {self.currency} and {other.currency}")

    def __add__(self, other):
        self._check_same_currency(other)
        return Money(self.amount + other.amount, self.currency)

    def __radd__(self, other):
        # sum() starts with 0, so 0 + Money(...) comes here
        if other == 0:
            return self
        return self + other

    def __sub__(self, other):
        self._check_same_currency(other)
        return Money(self.amount - other.amount, self.currency)

    def __mul__(self, quantity):
        return Money(self.amount * quantity, self.currency)

    def __eq__(self, other):
        return self.amount == other.amount and self.currency == other.currency

    def __lt__(self, other):
        self._check_same_currency(other)
        return self.amount < other.amount

    def __hash__(self):
        return hash((self.amount, self.currency))

    def __bool__(self):
        return self.amount != 0


if __name__ == "__main__":
    lamp = Money(24.99)
    mugs = Money(8.50) * 2
    print(lamp, "+", mugs, "=", lamp + mugs)
