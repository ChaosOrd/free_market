from unittest import TestCase
from unittest.mock import Mock
from ..exchange import Order


class OrderTest(TestCase):

    def test_constructor_initializes_resource(self):
        resource = Mock()

        order = Order(resource=resource, price=Mock(), quantity=Mock())

        self.assertEquals(order.resource, resource)

    def test_constructor_initializes_price(self):
        order = Order(resource=Mock(), price=1, quantity=Mock())

        self.assertEquals(order.price, 1)

    def test_constructor_initializes_quantity(self):
        order = Order(resource=Mock(), price=Mock(), quantity=12)

        self.assertEqual(order.quantity, 12)
