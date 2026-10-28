import unittest

from exercise import Customer, FlatRateShipping, FreeShippingOver, Order, OrderLine


def alex_order(shipping=None):
    order = Order(Customer("Alex Kim", "alex@example.com"), shipping or FlatRateShipping())
    order.add("Desk lamp", 24.99)
    order.add("Coffee mug", 8.50, 2)
    return order


class TestOrderLine(unittest.TestCase):
    def test_line(self):
        line = OrderLine("Coffee mug", 8.50, 2)
        self.assertEqual((line.name, line.unit_price, line.quantity), ("Coffee mug", 8.5, 2))
        self.assertEqual(line.subtotal(), 17.0)

    def test_default_quantity(self):
        self.assertEqual(OrderLine("Lamp", 24.99).quantity, 1)


class TestOrder(unittest.TestCase):
    def test_holds_customer_and_lines(self):
        order = alex_order()
        self.assertEqual(order.customer.name, "Alex Kim")
        self.assertEqual(len(order.lines), 2)
        self.assertTrue(all(isinstance(line, OrderLine) for line in order.lines),
                        "Order.lines should hold OrderLine objects")

    def test_add_same_item_increases_quantity(self):
        order = alex_order()
        order.add("Coffee mug", 8.50, 3)
        self.assertEqual(len(order.lines), 2, "Adding an item that's already there shouldn't add a new line")
        self.assertEqual(order.item_count(), 6)

    def test_remove(self):
        order = alex_order()
        self.assertIs(order.remove("Desk lamp"), True)
        self.assertIs(order.remove("Kettle"), False)
        self.assertEqual(order.item_count(), 2)

    def test_totals(self):
        order = alex_order()
        self.assertEqual(order.subtotal(), 41.99)
        self.assertEqual(order.shipping_cost(), 4.99)
        self.assertEqual(order.total(), 46.98)

    def test_swapping_shipping_changes_total(self):
        order = alex_order(FreeShippingOver(40))
        self.assertEqual(order.shipping_cost(), 0)
        self.assertEqual(order.total(), 41.99)
        order.shipping = FlatRateShipping(2.50)
        self.assertEqual(order.total(), 44.49, "shipping_cost should ask whatever shipping object the order has")

    def test_receipt(self):
        self.assertEqual(alex_order().receipt(), "\n".join([
            "Order for Alex Kim",
            "1 x Desk lamp: $24.99",
            "2 x Coffee mug: $17.00",
            "Subtotal: $41.99",
            "Shipping: $4.99",
            "Total: $46.98",
        ]))

    def test_empty_order(self):
        order = Order(Customer("Sam", "sam@example.com"), FreeShippingOver(40))
        self.assertEqual((order.item_count(), order.subtotal()), (0, 0))
        self.assertEqual(order.total(), 4.99)


if __name__ == "__main__":
    unittest.main()
