from unittest import TestCase
from unittest.mock import MagicMock
from exchange import Exchange, OrderSide


class ExchangeTest(TestCase):

    def setUp(self):
        self.buy_order = MagicMock()
        self.buy_sender = self.buy_order.sender
        self.sell_order = MagicMock()
        self.sell_sender = self.sell_order.sender
        self.buy_order.price = 10
        self.buy_order.quantity = 5
        self.buy_order.side = OrderSide.Buy

        self.sell_order.price = 10
        self.sell_order.quantity = -5
        self.sell_order.side = OrderSide.Sell

    def _create_order_mock(self, price, quantity, side):
        order_mock = MagicMock()
        order_mock.price = price
        order_mock.quantity = quantity
        order_mock.side = side

        return order_mock

    def test_orders_with_same_prices_result_in_fill(self):
        exchange = Exchange()

        exchange.place_order(self.buy_order)
        exchange.place_order(self.sell_order)

        self.buy_sender.on_order_filled.assert_called_once_with(
            order=self.buy_order, price=10, quantity=5)
        self.sell_sender.on_order_filled.assert_called_once_with(
            order=self.sell_order, price=10, quantity=-5)

    def test_orders_with_uncrossing_prices_do_not_result_in_fill(self):
        exchange = Exchange()
        self.sell_order.price = 11

        exchange.place_order(self.buy_order)
        exchange.place_order(self.sell_order)

        self.assertFalse(self.buy_sender.on_order_filled.called)
        self.assertFalse(self.sell_sender.on_order_filled.called)

    def test_orders_with_same_side_do_not_result_in_fill(self):
        exchange = Exchange()
        another_sell_order = self._create_order_mock(11, -5, OrderSide.Sell)

        exchange.place_order(self.sell_order)
        exchange.place_order(another_sell_order)

        self.assertFalse(self.buy_sender.on_order_filled.called)
        self.assertFalse(another_sell_order.on_order_filled.called)

    def test_filled_with_sell_order_price_if_it_came_first(self):
        exchange = Exchange()
        self.sell_order.price = 9.5

        exchange.place_order(self.sell_order)
        exchange.place_order(self.buy_order)

        self.buy_sender.on_order_filled.assert_called_once_with(
            order=self.buy_order, price=9.5, quantity=5)
        self.sell_sender.on_order_filled.assert_called_once_with(
            order=self.sell_order, price=9.5, quantity=-5)

    def test_filled_with_buy_order_price_if_it_came_first(self):
        exchange = Exchange()
        self.sell_order.price = 9.5

        exchange.place_order(self.buy_order)
        exchange.place_order(self.sell_order)

        self.buy_sender.on_order_filled.assert_called_once_with(
            order=self.buy_order, price=10, quantity=5)
        self.sell_sender.on_order_filled.assert_called_once_with(
            order=self.sell_order, price=10, quantity=-5)

    def test_crossing_orders_filled_with_minimal_quantity(self):
        exchange = Exchange()
        self.sell_order.quantity = -3

        exchange.place_order(self.buy_order)
        exchange.place_order(self.sell_order)

        self.buy_sender.on_order_filled.assert_called_once_with(
            order=self.buy_order, price=10, quantity=3)
        self.sell_sender.on_order_filled.assert_called_once_with(
            order=self.sell_order, price=10, quantity=-3)

    def test_crossing_orders_quantities_are_reduced_after_the_fill(self):
        exchange = Exchange()
        self.sell_order.quantity = -3
        self.buy_order.quantity = 4

        exchange.place_order(self.buy_order)
        exchange.place_order(self.sell_order)

        self.assertEquals(self.buy_order.quantity, 1)
        self.assertEquals(self.sell_order.quantity, 0)

    def test_order_removed_from_book_when_left_with_zero_quantity(self):
        exchange = Exchange()
        self.sell_order.quantity = -3
        self.buy_order.quantity = 4

        exchange.place_order(self.buy_order)
        exchange.place_order(self.sell_order)

        self.assertEqual(exchange.book_size, 1)

    def test_get_best_sell_returns_the_only_sell_order(self):
        exchange = Exchange()
        order = self._create_order_mock(10, -5, OrderSide.Sell)

        exchange.place_order(order)
        self.assertEqual(exchange.get_best_sell(), order)

    def test_get_best_sell_returns_sell_order_with_lowest_price_when_there_are_only_sell_orders(self):
        exchange = Exchange()
        first_order = self._create_order_mock(10, -5, OrderSide.Sell)
        second_order = self._create_order_mock(9.8, -3, OrderSide.Sell)

        exchange.place_order(first_order)
        exchange.place_order(second_order)

        self.assertEqual(exchange.get_best_sell(), second_order)

    def test_get_best_sell_returns_sell_order_with_lowest_price_when_there_are_also_buy_orders(self):
        exchange = Exchange()
        first_order = self._create_order_mock(10, -5, OrderSide.Sell)
        second_order = self._create_order_mock(9.8, -3, OrderSide.Sell)
        buy_order = self._create_order_mock(9.4, 6, OrderSide.Buy)

        exchange.place_order(first_order)
        exchange.place_order(second_order)
        exchange.place_order(buy_order)

        self.assertEqual(exchange.get_best_sell(), second_order)

    def test_get_best_buy_returns_the_only_buy_order(self):
        exchange = Exchange()
        order = self._create_order_mock(10, 4, OrderSide.Buy)

        exchange.place_order(order)

        self.assertEquals(exchange.get_best_buy(), order)

    def test_get_best_buy_returns_buy_order_with_highest_price__when_there_are_only_buy_orders(self):
        exchange = Exchange()
        first_buy_order = self._create_order_mock(10, 4, OrderSide.Buy)
        second_buy_order = self._create_order_mock(10.5, 3, OrderSide.Buy)

        exchange.place_order(first_buy_order)
        exchange.place_order(second_buy_order)

        self.assertEquals(exchange.get_best_buy(), second_buy_order)

    def test_get_best_buy_returns_buy_order_with_highest_price_when_there_are_only_sell_orders(self):
        exchange = Exchange()
        first_buy_order = self._create_order_mock(10, 4, OrderSide.Buy)
        second_buy_order = self._create_order_mock(10.5, 3, OrderSide.Buy)
        sell_order = self._create_order_mock(11.6, -4, OrderSide.Sell)

        exchange.place_order(first_buy_order)
        exchange.place_order(second_buy_order)
        exchange.place_order(sell_order)

        self.assertEquals(exchange.get_best_buy(), second_buy_order)

    def test_book_size_returs_the_number_of_placed_orders(self):
        exchange = Exchange()
        first_buy_order = self._create_order_mock(10, 4, OrderSide.Buy)
        second_buy_order = self._create_order_mock(10.5, 3, OrderSide.Buy)

        exchange.place_order(first_buy_order)
        exchange.place_order(second_buy_order)

        self.assertEquals(exchange.book_size, 2)