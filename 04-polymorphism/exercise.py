# Lesson 4: discounts
#
# Write NoDiscount, PercentOff, AmountOff and BuyXGetOneFree. Each has
#     apply(unit_price, quantity)  -> the total to pay, rounded to 2 decimal places
#     describe()                   -> a short description
# Then write best_discount. See README.md for the details.
# Test with:  python3 -m unittest -v


class NoDiscount:
    def apply(self, unit_price, quantity):
        pass

    def describe(self):
        pass


# Write PercentOff, AmountOff and BuyXGetOneFree here.


def best_discount(discounts, unit_price, quantity):
    """Return the discount that gives the lowest total (the first one, if there's a tie)."""
    pass


if __name__ == "__main__":
    offers = [NoDiscount()]
    for offer in offers:
        print(offer.describe(), offer.apply(8.50, 3))
