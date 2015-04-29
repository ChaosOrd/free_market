from unittest import TestCase
from unittest.mock import Mock
from ..exchange import Exchange


class ExchangeTest(TestCase):

    def test_orders_with_crossing_prices_result_in_fill(self):
        exchange = Exchange()
        buy_order = Mock()
        buy_order.price = 10
        buy_order.quantity = -5

        sell_order = Mock()
        sell_order.price = 9.7
        sell_order.quantity = 5

        exchange.place_order(buy_order)
        exchange.place_order(sell_order)

        buy_order.sender.on_order_filled.assert_called_once_with(
            order=buy_order, price=10, quantity=-5)
        sell_order.sender.on_order_filled.assert_called_once_with(
            order=buy_order, price=10, quantity=5)
