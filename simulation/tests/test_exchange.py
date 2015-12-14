from unittest import TestCase
from unittest.mock import MagicMock
from exchange import Exchange, OrderSide


# noinspection PyTypeChecker
class ExchangeTest(TestCase):

    def setUp(self):
        self.buy_order = MagicMock()
        self.buy_sender = MagicMock()
        self.sell_order = MagicMock()
        self.sell_sender = MagicMock()
        self.standard_resource = MagicMock()

        self.buy_order.price = 10
        self.buy_order.quantity = 5
        self.buy_order.side = OrderSide.Buy
        self.buy_order.resource = self.standard_resource

        self.sell_order.price = 10
        self.sell_order.quantity = -5
        self.sell_order.side = OrderSide.Sell
        self.sell_order.resource = self.standard_resource

    def _create_order_mock(self, price, quantity, side, resource=None):
        order_mock = MagicMock()
        order_mock.price = price
        order_mock.quantity = quantity
        order_mock.side = side
        order_mock.resource = resource
        if resource is None:
            order_mock.resource = self.standard_resource
        else:
            order_mock.resource = resource

        return order_mock

    def test_orders_with_same_prices_result_in_fill(self):
        exchange = Exchange()

        exchange.place_order(self.buy_order, self.buy_sender)
        exchange.place_order(self.sell_order, self.sell_sender)

        self.buy_sender.on_order_filled.assert_called_once_with(
            order=self.buy_order, price=10, quantity=5)
        self.sell_sender.on_order_filled.assert_called_once_with(
            order=self.sell_order, price=10, quantity=-5)

    def test_orders_with_uncrossing_prices_do_not_result_in_fill(self):
        exchange = Exchange()
        self.sell_order.price = 11

        exchange.place_order(self.buy_order, self.buy_sender)
        exchange.place_order(self.sell_order, self.sell_sender)

        self.assertFalse(self.buy_sender.on_order_filled.called)
        self.assertFalse(self.sell_sender.on_order_filled.called)

    def test_orders_with_same_side_do_not_result_in_fill(self):
        exchange = Exchange()
        another_sell_order = self._create_order_mock(11, -5, OrderSide.Sell)

        exchange.place_order(self.sell_order, self.sell_sender)
        exchange.place_order(another_sell_order, MagicMock())

        self.assertFalse(self.buy_sender.on_order_filled.called)
        self.assertFalse(another_sell_order.on_order_filled.called)

    def test_orders_with_different_resources_do_not_result_in_fill(self):
        exchange = Exchange()
        another_resource = MagicMock()
        another_resource_sell_order = self._create_order_mock(10, -5, OrderSide.Sell, another_resource)

        exchange.place_order(self.buy_order, self.buy_sender)
        exchange.place_order(another_resource_sell_order, self.sell_sender)

        self.assertFalse(self.buy_sender.on_order_filled.called)
        self.assertFalse(another_resource_sell_order.on_order_filled.called)

    def test_filled_with_sell_order_price_if_it_came_first(self):
        exchange = Exchange()
        self.sell_order.price = 9.5

        exchange.place_order(self.sell_order, self.sell_sender)
        exchange.place_order(self.buy_order, self.buy_sender)

        self.buy_sender.on_order_filled.assert_called_once_with(
            order=self.buy_order, price=9.5, quantity=5)
        self.sell_sender.on_order_filled.assert_called_once_with(
            order=self.sell_order, price=9.5, quantity=-5)

    def test_filled_with_buy_order_price_if_it_came_first(self):
        exchange = Exchange()
        self.sell_order.price = 9.5

        exchange.place_order(self.buy_order, self.buy_sender)
        exchange.place_order(self.sell_order, self.sell_sender)

        self.buy_sender.on_order_filled.assert_called_once_with(
            order=self.buy_order, price=10, quantity=5)
        self.sell_sender.on_order_filled.assert_called_once_with(
            order=self.sell_order, price=10, quantity=-5)

    def test_crossing_orders_filled_with_minimal_quantity(self):
        exchange = Exchange()
        self.sell_order.quantity = -3

        exchange.place_order(self.buy_order, self.buy_sender)
        exchange.place_order(self.sell_order, self.sell_sender)

        self.buy_sender.on_order_filled.assert_called_once_with(
            order=self.buy_order, price=10, quantity=3)
        self.sell_sender.on_order_filled.assert_called_once_with(
            order=self.sell_order, price=10, quantity=-3)

    def test_crossing_orders_quantities_are_reduced_after_the_fill(self):
        exchange = Exchange()
        self.sell_order.quantity = -3
        self.buy_order.quantity = 4

        exchange.place_order(self.buy_order, self.buy_sender)
        exchange.place_order(self.sell_order, self.sell_sender)

        self.assertEquals(self.buy_order.quantity, 1)
        self.assertEquals(self.sell_order.quantity, 0)

    def test_order_removed_from_book_when_left_with_zero_quantity(self):
        exchange = Exchange()
        self.sell_order.quantity = -3
        self.buy_order.quantity = 4

        exchange.place_order(self.buy_order, self.buy_sender)
        exchange.place_order(self.sell_order, self.sell_sender)

        self.assertEqual(exchange.get_number_of_placed_orders(self.standard_resource), 1)

    def test_get_best_sell_returns_the_only_sell_order(self):
        exchange = Exchange()
        order = self._create_order_mock(10, -5, OrderSide.Sell)

        exchange.place_order(order, self.sell_sender)
        self.assertEqual(exchange.get_best_sell(self.standard_resource), order)

    def test_get_best_sell_returns_sell_order_with_lowest_price_when_there_are_only_sell_orders(self):
        exchange = Exchange()
        first_order = self._create_order_mock(10, -5, OrderSide.Sell)
        second_order = self._create_order_mock(9.8, -3, OrderSide.Sell)

        exchange.place_order(first_order, MagicMock())
        exchange.place_order(second_order, MagicMock())

        self.assertEqual(exchange.get_best_sell(self.standard_resource), second_order)

    def test_get_best_sell_returns_sell_order_of_requested_resource(self):
        exchange = Exchange()
        first_order = self._create_order_mock(10, -5, OrderSide.Sell)
        another_resource = MagicMock()
        second_order = self._create_order_mock(9.8, -3, OrderSide.Sell, another_resource)

        exchange.place_order(first_order, MagicMock())
        exchange.place_order(second_order, MagicMock())

        self.assertEqual(exchange.get_best_sell(self.standard_resource), first_order)

    def test_get_best_sell_returns_sell_order_with_lowest_price_when_there_are_also_buy_orders(self):
        exchange = Exchange()
        first_order = self._create_order_mock(10, -5, OrderSide.Sell)
        second_order = self._create_order_mock(9.8, -3, OrderSide.Sell)
        buy_order = self._create_order_mock(9.4, 6, OrderSide.Buy)

        exchange.place_order(first_order, MagicMock())
        exchange.place_order(second_order, MagicMock())
        exchange.place_order(buy_order, MagicMock())

        self.assertEqual(exchange.get_best_sell(self.standard_resource), second_order)

    def test_get_best_sell_returns_none_if_no_orders_placed(self):
        exchange = Exchange()

        self.assertIsNone(exchange.get_best_sell(self.standard_resource))

    def test_get_best_buy_returns_the_only_buy_order(self):
        exchange = Exchange()
        order = self._create_order_mock(10, 4, OrderSide.Buy)

        exchange.place_order(order, MagicMock())

        self.assertEquals(exchange.get_best_buy(self.standard_resource), order)

    def test_get_best_buy_returns_buy_order_with_highest_price__when_there_are_only_buy_orders(self):
        exchange = Exchange()
        first_buy_order = self._create_order_mock(10, 4, OrderSide.Buy)
        second_buy_order = self._create_order_mock(10.5, 3, OrderSide.Buy)

        exchange.place_order(first_buy_order, MagicMock())
        exchange.place_order(second_buy_order, MagicMock())

        self.assertEquals(exchange.get_best_buy(self.standard_resource), second_buy_order)

    def test_get_best_buy_returns_buy_order_of_the_right_resource(self):
        exchange = Exchange()
        first_buy_order = self._create_order_mock(10, 4, OrderSide.Buy)
        another_resource = MagicMock()
        second_buy_order = self._create_order_mock(10.5, 3, OrderSide.Buy, another_resource)

        exchange.place_order(first_buy_order, MagicMock())
        exchange.place_order(second_buy_order, MagicMock())

        self.assertEquals(exchange.get_best_buy(self.standard_resource), first_buy_order)

    def test_get_best_buy_returns_buy_order_with_highest_price_when_there_are_only_sell_orders(self):
        exchange = Exchange()
        first_buy_order = self._create_order_mock(10, 4, OrderSide.Buy)
        second_buy_order = self._create_order_mock(10.5, 3, OrderSide.Buy)
        sell_order = self._create_order_mock(11.6, -4, OrderSide.Sell)

        exchange.place_order(first_buy_order, MagicMock())
        exchange.place_order(second_buy_order, MagicMock())
        exchange.place_order(sell_order, MagicMock())

        self.assertEquals(exchange.get_best_buy(self.standard_resource), second_buy_order)

    def test_get_best_buy_returns_none_if_no_orders_placed(self):
        exchange = Exchange()

        self.assertIsNone(exchange.get_best_buy(self.standard_resource))

    def test_get_number_of_placed_orders_returns_the_number_of_placed_orders(self):
        exchange = Exchange()
        first_buy_order = self._create_order_mock(10, 4, OrderSide.Buy)
        second_buy_order = self._create_order_mock(10.5, 3, OrderSide.Buy)

        exchange.place_order(first_buy_order, MagicMock())
        exchange.place_order(second_buy_order, MagicMock())

        self.assertEquals(exchange.get_number_of_placed_orders(self.standard_resource), 2)

    def test_get_number_of_placed_orders_returns_zero_when_no_orders_placed(self):
        exchange = Exchange()

        self.assertEqual(exchange.get_number_of_placed_orders(MagicMock()), 0)

    def test_get_orders_sent_by_returns_orders_of_specified_sender(self):
        exchange = Exchange()
        first_sender_order = self._create_order_mock(10, 4, OrderSide.Buy)
        first_sender = MagicMock()
        second_sender_order = self._create_order_mock(10.5, 3, OrderSide.Buy)
        second_sender = MagicMock()
        another_second_sender_order = self._create_order_mock(10.7, 1, OrderSide.Buy)

        exchange.place_order(first_sender_order, first_sender)
        exchange.place_order(second_sender_order, second_sender)
        exchange.place_order(another_second_sender_order, first_sender)

        expected_orders = {first_sender_order, another_second_sender_order}
        actual_orders = set(exchange.get_orders_sent_by(first_sender))
        self.assertEqual(actual_orders, expected_orders)
