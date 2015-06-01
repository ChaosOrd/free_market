from unittest import TestCase
from unittest.mock import Mock
from exchange import Exchange


class ExchangeTest(TestCase):

    def setUp(self):
        self.buy_order = Mock()
        self.buy_sender = self.buy_order.sender
        self.sell_order = Mock()
        self.sell_sender = self.sell_order.sender
        self.buy_order.price = 10
        self.buy_order.quantity = -5

        self.sell_order.price = 10
        self.sell_order.quantity = 5

    def test_orders_with_same_prices_result_in_fill(self):
        exchange = Exchange()

        exchange.place_order(self.buy_order)
        exchange.place_order(self.sell_order)

        self.buy_sender.on_order_filled.assert_called_once_with(
            order=self.buy_order, price=10, quantity=-5)
        self.sell_sender.on_order_filled.assert_called_once_with(
            order=self.sell_order, price=10, quantity=5)

    def test_orders_with_uncrossing_prices_do_not_result_in_fill(self):
        exchange = Exchange()
        self.sell_order.price = 11

        exchange.place_order(self.buy_order)
        exchange.place_order(self.sell_order)

        self.assertFalse(self.buy_sender.on_order_filled.called)
        self.assertFalse(self.sell_sender.on_order_filled.called)

    def test_filled_with_sell_order_price_if_it_came_first(self):
        exchange = Exchange()
        self.sell_order.price = 9.5

        exchange.place_order(self.sell_order)
        exchange.place_order(self.buy_order)

        self.buy_sender.on_order_filled.assert_called_once_with(
            order=self.buy_order, price=9.5, quantity=-5)
        self.sell_sender.on_order_filled.assert_called_once_with(
            order=self.sell_order, price=9.5, quantity=5)

    def test_filled_with_buy_order_price_if_it_came_first(self):
        exchange = Exchange()
        self.sell_order.price = 9.5

        exchange.place_order(self.buy_order)
        exchange.place_order(self.sell_order)

        self.buy_sender.on_order_filled.assert_called_once_with(
            order=self.buy_order, price=10, quantity=-5)
        self.sell_sender.on_order_filled.assert_called_once_with(
            order=self.sell_order, price=10, quantity=5)

    def test_crossing_orders_filled_with_minimal_quantity(self):
        exchange = Exchange()
        self.sell_order.quantity = 3

        exchange.place_order(self.buy_order)
        exchange.place_order(self.sell_order)

        self.buy_sender.on_order_filled.assert_called_once_with(
            order=self.buy_order, price=10, quantity=-3)
        self.sell_sender.on_order_filled.assert_called_once_with(
            order=self.sell_order, price=10, quantity=3)
