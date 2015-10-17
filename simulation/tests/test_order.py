from unittest import TestCase
from unittest.mock import Mock
from exchange import Order, OrderSide


class OrderTest(TestCase):

    def test_constructor_initializes_resource(self):
        resource = Mock()

        order = Order(sender=Mock(), resource=resource, price=Mock(),
                      quantity=Mock())

        self.assertEquals(order.resource, resource)

    def test_constructor_initializes_price(self):
        order = Order(sender=Mock(), resource=Mock(), price=1, quantity=Mock())

        self.assertEquals(order.price, 1)

    def test_constructor_initializes_quantity(self):
        order = Order(sender=Mock(), resource=Mock(), price=Mock(), quantity=12)

        self.assertEquals(order.quantity, 12)

    def test_constructor_initializes_sender(self):
        sender = Mock()

        order = Order(sender=sender, resource=Mock(), price=Mock(),
                      quantity=Mock())

        self.assertEquals(order.sender, sender)

    def test_order_side_returns_buy_if_quantity_greater_than_0(self):
        order = Order(sender=Mock(), resource=Mock(), price=Mock(), quantity=12)

        self.assertEquals(order.side, OrderSide.Buy)

    def test_order_side_returns_sell_if_quantity_less_than_0(self):
        order = Order(sender=Mock(), resource=Mock(), price=Mock(), quantity=-4)

        self.assertEquals(order.side, OrderSide.Sell)

    def test_order_side_returns_none_if_quantity_is_0(self):
        order = Order(sender=Mock(), resource=Mock(), price=Mock(), quantity=0)

        self.assertIsNone(order.side)
