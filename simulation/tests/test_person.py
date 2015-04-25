import unittest
from unittest import TestCase
from unittest.mock import Mock, patch, call
from simulation.simulator import Person

class BasePersonTest(TestCase):

    def setUp(self):
        self.population = Mock()
        self.population.quantity = 3
        self.exchange = Mock()

class PersonInitializationTest(BasePersonTest):

    @patch('simulation.simulator.Person._single_person_from_population')
    def test_from_population_calls_single_person_from_population(
        self, single_person_from_population_mock):
        Person.from_population(self.population, self.exchange)

        single_person_from_population_mock.assert_called_once_with(
            self.population, self.exchange)

    @patch('simulation.simulator.Person._single_person_from_population')
    def test_from_population_returns_list_of_copies_from_initial_person(
        self, single_person_from_population_mock):

        Person.copy = Mock()
        first_person_copy = Mock()
        second_person_copy = Mock()
        third_person_copy = Mock()
        initial_person = single_person_from_population_mock.return_value
        initial_person.copy.side_effect = [first_person_copy, second_person_copy,
                                           third_person_copy]

        persons = Person.from_population(self.population, self.exchange)

        self.assertEquals(persons, [first_person_copy, second_person_copy,
                                    third_person_copy])

    def test_single_person_from_population_sets_person_population(self):
        initial_person = Person._single_person_from_population(self.population,
                                                               self.exchange)

        self.assertEquals(initial_person.population, self.population)

    def test_singpe_person_from_population_stes_person_exchange(self):
        initial_person = Person._single_person_from_population(self.population,
                                                               self.exchange)

        self.assertEquals(initial_person.exchange, self.exchange)

    def test_copy_copies_population(self):
        person = Person(Mock(), Mock())

        copy_person = person.copy()

        self.assertEquals(copy_person.population, person.population)

    def test_copy_copies_exchange(self):
        person = Person(Mock(), Mock())

        copy_person = person.copy()

        self.assertEquals(copy_person.exchange, person.exchange)

    def test_copy_does_not_copy_inventory(self):
        person = Person(Mock(), Mock())

        copy_person = person.copy()

        self.assertIsNot(person.inventory, copy_person.inventory)

    def test_constructor_creates_empty_inventory(self):
        person = Person(Mock(), Mock())

        self.assertEquals(person.inventory, {})

class PersonOrderPlacementTest(BasePersonTest):

    def setUp(self):
        super().setUp()
        self.start_patchers()
        self.create_resources()
        self.create_demands()
        self.create_supplies()
        self.create_sell_orders()

    def tearDown(self):
        super().tearDown()
        self.stop_patchers()

    def start_patchers(self):
        self.order_patcher = patch('simulation.simulator.Order')
        self.order_cls = self.order_patcher.start()
        self.random_patcher = patch('simulation.simulator.random')
        self.random = self.random_patcher.start()

    def stop_patchers(self):
        self.order_patcher.stop()
        self.random_patcher.stop()

    def create_resources(self):
        self.water_resource = Mock()
        self.tools_resource = Mock()
        self.grain_resource = Mock()
        self.potatoes_resource = Mock()

    def create_sell_orders(self):
        self.create_water_sell_order()
        self.create_tools_sell_order()

    def create_water_sell_order(self):
        self.water_sell_order = Mock()
        self.water_sell_order.resource = self.water_resource
        self.water_sell_order.price = 140
        self.water_sell_order.quantity = 10

    def create_tools_sell_order(self):
        self.tools_sell_order = Mock()
        self.tools_sell_order.resource = self.tools_resource
        self.tools_sell_order.price = 240
        self.tools_sell_order.quantity = 15

    def create_demands(self):
        self.create_water_demand()
        self.create_toos_demand()

    def create_water_demand(self):
        self.water_demand = Mock()
        self.water_demand.value = -1
        self.water_demand.resource = self.water_resource

    def create_toos_demand(self):
        self.tools_demand = Mock()
        self.tools_demand.value = -0.5
        self.tools_demand.resource = self.tools_resource

    def create_supplies(self):
        self.create_grain_supply()
        self.create_potatoes_supply()

    def create_grain_supply(self):
        self.grain_supply = Mock()
        self.grain_supply.value = 7.5
        self.grain_supply.resource = self.grain_resource

    def create_potatoes_supply(self):
        self.potatoes_supply = Mock()
        self.potatoes_supply.value = 4
        self.potatoes_supply.resource = self.potatoes_resource

    def test_on_iteration_creates_buy_orders_according_to_demands(self):
        self.population.supplies_demands = [self.water_demand, self.tools_demand]
        person = Person(self.population, self.exchange)
        self.exchange.get_best_sell.side_effect = [
            self.water_sell_order, self.tools_sell_order
        ]

        person.on_iteration()

        expected_calls = [call(resource=self.water_resource, price=140,
                               quantity=-1),
                          call(resource=self.tools_resource, price=240,
                               quantity=-0.5)]
        self.order_cls.assert_has_calls(expected_calls, any_order=True)

    def test_on_iteration_creates_sell_orders_for_each_supply(self):
        self.population.supplies_demands = [self.grain_supply, self.potatoes_supply]
        person = Person(self.population, self.exchange)

        person.on_iteration()

        expected_calls = [call(resource=self.grain_resource,
                               price=self.random.randint.return_value,
                               quantity=7.5),
                          call(resource=self.potatoes_resource,
                               price=self.random.randint.return_value,
                               quantity=4)]
        self.order_cls.assert_has_calls(expected_calls, any_order=True)

    def test_on_iteration_calls_random_for_each_demand(self):
        self.population.supplies_demands = [self.grain_supply, self.potatoes_supply]
        person = Person(self.population, self.exchange)

        person.on_iteration()

        random_call = call(Person.MIN_RANDOM_PRICE, Person.MAX_RANDOM_PRICE)
        self.random.randint.assert_has_calls([random_call, random_call])

    def test_on_iteration_places_buy_order_for_each_supply_demand(self):
        self.population.supplies_demands = [self.water_demand, self.grain_supply]
        person = Person(self.population, self.exchange)

        person.on_iteration()

        expected_calls = [call(self.order_cls.return_value),
                          call(self.order_cls.return_value)]
        self.exchange.place_order.assert_has_calls(expected_calls)


if __name__ == '__main__':
    unittest.main()
