# Solution to lesson 4: discounts


class NoDiscount:
    def apply(self, unit_price, quantity):
        return round(unit_price * quantity, 2)

    def describe(self):
        return "No discount"


class PercentOff:
    def __init__(self, percent):
        self.percent = percent

    def apply(self, unit_price, quantity):
        return round(unit_price * quantity * (1 - self.percent / 100), 2)

    def describe(self):
        return f"{self.percent}% off"


class AmountOff:
    def __init__(self, amount):
        self.amount = amount

    def apply(self, unit_price, quantity):
        return round(max(0, unit_price * quantity - self.amount), 2)

    def describe(self):
        return f"${self.amount:.2f} off"


class BuyXGetOneFree:
    def __init__(self, x):
        self.x = x

    def apply(self, unit_price, quantity):
        free = quantity // (self.x + 1)
        return round(unit_price * (quantity - free), 2)

    def describe(self):
        return f"Buy {self.x}, get 1 free"


def best_discount(discounts, unit_price, quantity):
    """Return the discount that gives the lowest total (the first one, if there's a tie)."""
    best = discounts[0]
    for discount in discounts[1:]:
        if discount.apply(unit_price, quantity) < best.apply(unit_price, quantity):
            best = discount
    return best


if __name__ == "__main__":
    offers = [NoDiscount(), PercentOff(15), AmountOff(5), BuyXGetOneFree(2)]
    for offer in offers:
        print(f"{offer.describe()}: ${offer.apply(8.50, 3):.2f}")
    print("Best:", best_discount(offers, 8.50, 3).describe())
