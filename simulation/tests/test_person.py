import unittest
from unittest import TestCase
from unittest.mock import Mock, patch, call, MagicMock
from numpy.lib.polynomial import poly1d
from simulator import Person


# noinspection PyTypeChecker
class BasePersonTest(TestCase):

    def setUp(self):
        self.population_mock = Mock()
        self.population_mock.quantity = 3
        self.exchange_mock = Mock()
        self.strategy_mock = MagicMock()
        self.create_simple_person()

    def create_simple_person(self):
        self.simple_person = Person(self.population_mock, self.exchange_mock, self.strategy_mock)


# noinspection PyTypeChecker
class PersonInitializationTest(BasePersonTest):

    def setUp(self):
        super().setUp()
        self.create_strategy_mock()

    def tearDown(self):
        super().tearDown()
        self.simple_strategy_patcher.stop()

    def create_strategy_mock(self):
        self.simple_strategy_patcher = patch('simulator.SimpleStrategy')
        self.simple_strategy_mock = self.simple_strategy_patcher.start()

    @patch('simulator.Person._single_person_from_population')
    def test_from_population_calls_single_person_from_population(self, single_person_from_population_mock):
        Person.from_population(self.population_mock, self.exchange_mock)

        single_person_from_population_mock.assert_called_once_with(
            self.population_mock, self.exchange_mock)

    @patch('simulator.Person._single_person_from_population')
    def test_from_population_returns_list_of_copies_from_initial_person(self, single_person_from_population_mock):

        Person.copy_initial = Mock()
        first_person_copy = Mock()
        second_person_copy = Mock()
        third_person_copy = Mock()
        initial_person = single_person_from_population_mock.return_value
        initial_person.copy_initial.side_effect = [first_person_copy, second_person_copy,
                                                   third_person_copy]

        persons = Person.from_population(self.population_mock, self.exchange_mock)

        self.assertEquals(persons, [first_person_copy, second_person_copy,
                                    third_person_copy])

    def test_single_person_from_population_sets_person_population(self):
        initial_person = Person._single_person_from_population(self.population_mock,
                                                               self.exchange_mock)

        self.assertEquals(initial_person.population, self.population_mock)

    def test_single_person_from_population_sets_person_exchange(self):
        initial_person = Person._single_person_from_population(self.population_mock,
                                                               self.exchange_mock)

        self.assertEquals(initial_person.exchange, self.exchange_mock)

    def test_single_person_from_population_sets_person_strategy(self):
        initial_person = Person._single_person_from_population(self.population_mock,
                                                               self.exchange_mock)

        self.simple_strategy_mock.assert_called_once_with(self.exchange_mock)
        self.assertEqual(initial_person.strategy, self.simple_strategy_mock.return_value)

    def test_copy_initial_copies_population(self):
        copy_person = self.simple_person.copy_initial()

        self.assertEquals(copy_person.population, self.simple_person.population)

    def test_copy_initial_copies_exchange(self):
        copy_person = self.simple_person.copy_initial()

        self.assertEquals(copy_person.exchange, self.simple_person.exchange)

    def test_copy_initial_copies_strategy(self):
        copy_person = self.simple_person.copy_initial()

        self.assertEquals(copy_person.strategy, self.simple_person.strategy)

    def test_copy_initial_does_not_copy_inventory(self):
        self.simple_person.inventory['SomeResource'] = Mock()

        copy_person = self.simple_person.copy_initial()

        self.assertNotIn('SomeResource', copy_person.inventory)

    def test_copy_full_copies_exchange(self):
        copy_person = self.simple_person.copy_full()

        self.assertEqual(self.simple_person.exchange, copy_person.exchange)

    def test_copy_full_copies_population(self):
        copy_person = self.simple_person.copy_full()

        self.assertEqual(self.simple_person.population, copy_person.population)

    def test_copy_full_copies_inventory(self):
        self.simple_person.inventory['SomeResource'] = Mock()

        copy_person = self.simple_person.copy_full()

        self.assertCountEqual(self.simple_person.inventory, copy_person.inventory)

    def test_initial_money(self):
        self.assertEquals(self.simple_person.money, Person.INITIAL_MONEY)


# noinspection PyTypeChecker
class PersonOrderPlacementTest(BasePersonTest):

    def setUp(self):
        super().setUp()
        self.order = MagicMock()
        self.resource = self.order.resource

    def assert_placed_orders(self, person, orders):
        self.strategy_mock.make_move.assert_called_once_with(person.population.supplies_demands,
                                                             person.inventory,
                                                             self.exchange_mock.get_orders_sent_by.return_value)
        self.exchange_mock.get_orders_sent_by.assert_called_once_with(person)

        expected_calls = []
        for order in orders:
            expected_calls.append(call(order, person))
        self.exchange_mock.place_order.assert_has_calls(expected_calls)

    def add_resource_to_person(self, person, resource, value):
        person.inventory[resource] = value

    def test_on_iteration_places_orders_from_strategy(self):
        self.simple_person.inventory = {'MONEY': 20}
        first_order = MagicMock()
        second_order = MagicMock()
        self.strategy_mock.make_move.return_value = [first_order, second_order]

        self.simple_person.on_iteration()

        self.assert_placed_orders(self.simple_person, [first_order, second_order])

    def test_on_order_filled_reduces_money_when_buying(self):
        self.simple_person.money = 100

        self.simple_person.on_order_filled(self.order, 7, 10)

        self.assertEqual(self.simple_person.money, 30)

    def test_on_order_filled_adds_money_when_selling(self):
        self.simple_person.money = 100

        self.simple_person.on_order_filled(self.order, 8, -6)

        self.assertEqual(self.simple_person.money, 148)

    def test_on_order_filled_adds_resource_when_buying(self):
        self.simple_person.on_order_filled(self.order, 6, 5)

        self.assertEqual(self.simple_person.inventory[self.resource], 5)

    def test_on_order_updates_existing_resource_when_buying(self):
        self.add_resource_to_person(self.simple_person, self.resource, 10)

        self.simple_person.on_order_filled(self.order, 6, 5)

        self.assertEquals(self.simple_person.inventory[self.resource], 15)

    def test_on_order_filled_subtracts_resource_when_selling(self):
        self.add_resource_to_person(self.simple_person, self.resource, 6)

        self.simple_person.on_order_filled(self.order, 6, -5)

        self.assertEqual(self.simple_person.inventory[self.resource], 1)

    def test_on_order_filled_removes_resource_if_ran_out(self):
        self.add_resource_to_person(self.simple_person, self.resource, 7)

        self.simple_person.on_order_filled(self.order, 6, -7)

        self.assertNotIn(self.resource, self.simple_person.inventory)

    def test_to_dict_returns_correct_data(self):
        result = self.simple_person.to_dict()

        self.assertEquals(result, {'inventory': self.simple_person.inventory,
                                   'population': self.population_mock.to_dict.return_value})

if __name__ == '__main__':
    unittest.main()
