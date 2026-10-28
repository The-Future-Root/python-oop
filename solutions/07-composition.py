# Solution to lesson 7: an order system


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
        self.name = name
        self.unit_price = unit_price
        self.quantity = quantity

    def subtotal(self):
        return round(self.unit_price * self.quantity, 2)


class Order:
    def __init__(self, customer, shipping):
        self.customer = customer
        self.shipping = shipping
        self.lines = []

    def add(self, name, unit_price, quantity=1):
        """Add an OrderLine, or increase the quantity of an existing line with the same name."""
        for line in self.lines:
            if line.name == name:
                line.quantity += quantity
                return
        self.lines.append(OrderLine(name, unit_price, quantity))

    def remove(self, name):
        """Remove the line with that name. Return True, or False if there wasn't one."""
        for line in self.lines:
            if line.name == name:
                self.lines.remove(line)
                return True
        return False

    def item_count(self):
        count = 0
        for line in self.lines:
            count += line.quantity
        return count

    def subtotal(self):
        amount = 0
        for line in self.lines:
            amount += line.subtotal()
        return round(amount, 2)

    def shipping_cost(self):
        return self.shipping.cost(self.subtotal())

    def total(self):
        return round(self.subtotal() + self.shipping_cost(), 2)

    def receipt(self):
        lines = [f"Order for {self.customer.name}"]
        for line in self.lines:
            lines.append(f"{line.quantity} x {line.name}: ${line.subtotal():.2f}")
        lines.append(f"Subtotal: ${self.subtotal():.2f}")
        lines.append(f"Shipping: ${self.shipping_cost():.2f}")
        lines.append(f"Total: ${self.total():.2f}")
        return "\n".join(lines)


if __name__ == "__main__":
    order = Order(Customer("Alex Kim", "alex@example.com"), FlatRateShipping())
    order.add("Desk lamp", 24.99)
    order.add("Coffee mug", 8.50, 2)
    print(order.receipt())
