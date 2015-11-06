from unittest import TestCase
from unittest.mock import MagicMock, call, patch
from strategies import SimpleStrategy

__author__ = 'chaosord'


# noinspection PyTypeChecker
class TestSimpleStrategy(TestCase):

    def setUp(self):
        self.population = MagicMock()
        self.exchange = MagicMock()
        self.person = MagicMock()
        self.start_patchers()
        self.create_resources()
        self.create_supplies()
        self.create_demands()
        self.create_sell_orders()

    def tearDown(self):
        self.stop_patches()

    def start_patchers(self):
        self.order_patcher = patch('strategies.Order')
        self.order_cls = self.order_patcher.start()
        self.order = self.order_cls.return_value
        self.random_patcher = patch('strategies.random')
        self.random = self.random_patcher.start()

    def stop_patches(self):
        self.order_patcher.stop()
        self.random_patcher.stop()

    def create_sell_orders(self):
        self.create_water_sell_order()
        self.create_tools_sell_order()

    def create_water_sell_order(self):
        self.water_sell_order = MagicMock()
        self.water_sell_order.resource = self.water_resource
        self.water_sell_order.price = 140
        self.water_sell_order.quantity = 10

    def create_tools_sell_order(self):
        self.tools_sell_order = MagicMock()
        self.tools_sell_order.resource = self.tools_resource
        self.tools_sell_order.price = 240
        self.tools_sell_order.quantity = 15

    def create_resources(self):
        self.water_resource = MagicMock()
        self.tools_resource = MagicMock()
        self.grain_resource = MagicMock()
        self.potatoes_resource = MagicMock()

    def create_demands(self):
        self.create_water_demand()
        self.create_tools_demand()

    def create_water_demand(self):
        self.water_demand = MagicMock()
        self.water_demand.value = -1
        self.water_demand.resource = self.water_resource

    def create_tools_demand(self):
        self.tools_demand = MagicMock()
        self.tools_demand.value = -0.5
        self.tools_demand.resource = self.tools_resource

    def create_supplies(self):
        self.create_grain_supply()
        self.create_potatoes_supply()

    def create_grain_supply(self):
        self.grain_supply = MagicMock()
        self.grain_supply.value = 7.5
        self.grain_supply.resource = self.grain_resource

    def create_potatoes_supply(self):
        self.potatoes_supply = MagicMock()
        self.potatoes_supply.value = 4
        self.potatoes_supply.resource = self.potatoes_resource

    def test_make_move_buy_orders_according_to_demands(self):
        supplies_demands = [self.water_demand, self.tools_demand]
        inventory = {}
        strategy = SimpleStrategy(self.exchange)
        self.exchange.get_best_sell.side_effect = [
            self.water_sell_order, self.tools_sell_order
        ]

        strategy.make_move(supplies_demands, inventory)

        expected_calls = [call(resource=self.water_resource, price=140, quantity=-1),
                          call(resource=self.tools_resource, price=240, quantity=-0.5)]
        self.order_cls.assert_has_calls(expected_calls, any_order=True)

    def test_make_move_returns_created_orders(self):
        supplies_demands = [self.water_demand, self.tools_demand]
        inventory = {}
        first_order = MagicMock()
        second_order = MagicMock()
        self.order_cls.side_effect = [first_order, second_order]
        strategy = SimpleStrategy(self.exchange)
        self.exchange.get_best_sell.side_effect = [
            self.water_sell_order, self.tools_sell_order
        ]

        self.assertEqual([first_order, second_order], strategy.make_move(supplies_demands, inventory))

    def test_make_move_does_not_create_buy_orders_if_there_is_no_supply(self):
        supplies_demands = [self.water_demand, self.tools_demand]
        inventory = {}
        strategy = SimpleStrategy(self.exchange)
        self.exchange.get_best_sell.return_value = None

        strategy.make_move(supplies_demands, inventory)

        self.assertFalse(self.order_cls.called)

    def test_returns_empty_list_when_there_is_no_supply(self):
        supplies_demands = [self.water_demand, self.tools_demand]
        inventory = {}
        strategy = SimpleStrategy(self.exchange)
        self.exchange.get_best_sell.return_value = None

        orders = strategy.make_move(supplies_demands, inventory)

        self.assertEqual(orders, [])

    def test_make_move_creates_sell_orders_for_each_supply(self):
        supplies_demands = [self.grain_supply, self.potatoes_supply]
        inventory = {}
        strategy = SimpleStrategy(self.exchange)

        strategy.make_move(supplies_demands, inventory)

        expected_calls = [call(resource=self.grain_resource, price=self.random.randint.return_value, quantity=7.5),
                          call(resource=self.potatoes_resource, price=self.random.randint.return_value, quantity=4)]
        self.order_cls.assert_has_calls(expected_calls, any_order=True)

    def test_make_move_calls_random_for_each_demand(self):
        supplies_demands = [self.grain_supply, self.potatoes_supply]
        inventory = {}
        strategy = SimpleStrategy(self.exchange)

        strategy.make_move(supplies_demands, inventory)

        random_call = call(SimpleStrategy.MIN_RANDOM_PRICE, SimpleStrategy.MAX_RANDOM_PRICE)
        self.random.randint.assert_has_calls([random_call, random_call])

    def test_make_move_places_buy_order_for_each_supply(self):
        supplies_demands = [self.grain_supply, self.potatoes_supply]
        inventory = {}
        first_order = MagicMock()
        second_order = MagicMock()
        self.order_cls.side_effect = [first_order, second_order]
        strategy = SimpleStrategy(self.exchange)

        orders = strategy.make_move(supplies_demands, inventory)

        self.assertEqual(orders, [first_order, second_order])

    def test_does_not_return_orders_if_orders_were_already_placed(self):
        supplies_demands = [self.grain_supply, self.potatoes_supply]
        inventory = {}
        self.exchange.get_orders_sent_by.return_value = [MagicMock()]
        strategy = SimpleStrategy(self.exchange)

        orders = strategy.make_move(supplies_demands, inventory, working_orders=[MagicMock()])
        self.assertEquals(orders, [])
