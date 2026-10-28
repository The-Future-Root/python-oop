# Lesson 7: an order system
#
# Customer, FlatRateShipping and FreeShippingOver are already written.
# Write OrderLine and Order. See README.md for every method.
# Test with:  python3 -m unittest -v


class Customer:
    def __init__(self, name, email):
        self.name = name
        self.email = email


class FlatRateShipping:
    def __init__(self, fee=4.99):
        self.fee = fee

    def cost(self, subtotal):
        return self.fee


class FreeShippingOver:
    def __init__(self, threshold, fee=4.99):
        self.threshold = threshold
        self.fee = fee

    def cost(self, subtotal):
        return 0 if subtotal >= self.threshold else self.fee


class OrderLine:
    def __init__(self, name, unit_price, quantity=1):
        pass

    def subtotal(self):
        pass


class Order:
    def __init__(self, customer, shipping):
        pass

    def add(self, name, unit_price, quantity=1):
        """Add an OrderLine, or increase the quantity of an existing line with the same name."""
        pass

    def remove(self, name):
        """Remove the line with that name. Return True, or False if there wasn't one."""
        pass

    def item_count(self):
        pass

    def subtotal(self):
        pass

    def shipping_cost(self):
        pass

    def total(self):
        pass

    def receipt(self):
        pass


if __name__ == "__main__":
    order = Order(Customer("Alex Kim", "alex@example.com"), FlatRateShipping())
    order.add("Desk lamp", 24.99)
    order.add("Coffee mug", 8.50, 2)
    print(order.receipt())
