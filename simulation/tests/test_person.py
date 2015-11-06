import unittest
from unittest import TestCase
from unittest.mock import Mock, patch, call, MagicMock
from simulator import Person


class BasePersonTest(TestCase):

    def setUp(self):
        self.population = Mock()
        self.population.quantity = 3
        self.exchange = Mock()


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
        Person.from_population(self.population, self.exchange)

        single_person_from_population_mock.assert_called_once_with(
            self.population, self.exchange)

    @patch('simulator.Person._single_person_from_population')
    def test_from_population_returns_list_of_copies_from_initial_person(self, single_person_from_population_mock):

        Person.copy_initial = Mock()
        first_person_copy = Mock()
        second_person_copy = Mock()
        third_person_copy = Mock()
        initial_person = single_person_from_population_mock.return_value
        initial_person.copy_initial.side_effect = [first_person_copy, second_person_copy,
                                                   third_person_copy]

        persons = Person.from_population(self.population, self.exchange)

        self.assertEquals(persons, [first_person_copy, second_person_copy,
                                    third_person_copy])

    def test_single_person_from_population_sets_person_population(self):
        initial_person = Person._single_person_from_population(self.population,
                                                               self.exchange)

        self.assertEquals(initial_person.population, self.population)

    def test_single_person_from_population_sets_person_exchange(self):
        initial_person = Person._single_person_from_population(self.population,
                                                               self.exchange)

        self.assertEquals(initial_person.exchange, self.exchange)

    def test_single_person_from_population_sets_person_strategy(self):
        initial_person = Person._single_person_from_population(self.population,
                                                               self.exchange)

        self.simple_strategy_mock.assert_called_once_with(self.exchange)
        self.assertEqual(initial_person.strategy, self.simple_strategy_mock.return_value)

    def test_copy_initial_copies_population(self):
        person = Person(Mock(), Mock(), Mock())

        copy_person = person.copy_initial()

        self.assertEquals(copy_person.population, person.population)

    def test_copy_initial_copies_exchange(self):
        person = Person(Mock(), Mock(), Mock())

        copy_person = person.copy_initial()

        self.assertEquals(copy_person.exchange, person.exchange)

    def test_copy_initial_copies_strategy(self):
        person = Person(Mock(), Mock(), Mock())

        copy_person = person.copy_initial()

        self.assertEquals(copy_person.strategy, person.strategy)

    def test_copy_initial_does_not_copy_inventory(self):
        person = Person(Mock(), Mock(), Mock())
        person.inventory['SomeResource'] = Mock()

        copy_person = person.copy_initial()

        self.assertNotIn('SomeResource', copy_person.inventory)

    def test_copy_full_copies_exchange(self):
        person = Person(Mock(), Mock(), Mock())

        copy_person = person.copy_full()

        self.assertEqual(person.exchange, copy_person.exchange)

    def test_copy_full_copies_population(self):
        person = Person(Mock(), Mock(), Mock())

        copy_person = person.copy_full()

        self.assertEqual(person.population, copy_person.population)

    def test_copy_full_copies_inventory(self):
        person = Person(Mock(), Mock(), Mock())
        person.inventory['SomeResource'] = Mock()

        copy_person = person.copy_full()

        self.assertCountEqual(person.inventory, copy_person.inventory)

    def test_initial_money(self):
        person = Person(Mock(), Mock(), Mock())

        self.assertEquals(person.money, Person.INITIAL_MONEY)


# noinspection PyTypeChecker
class PersonOrderPlacementTest(BasePersonTest):

    def setUp(self):
        super().setUp()
        self.create_strategy()
        self.create_order()

    def create_strategy(self):
        self.strategy_cls = MagicMock()
        self.strategy_obj = self.strategy_cls.return_value

    def create_order(self):
        self.order = MagicMock()

    def test_on_iteration_gets_orders_from_strategy(self):
        person = Person(self.population, self.exchange, self.strategy_obj)
        person.inventory = {'MONEY': 20}
        first_order = MagicMock()
        second_order = MagicMock()
        self.strategy_obj.make_move.return_value = [first_order, second_order]

        person.on_iteration()

        self.strategy_obj.make_move.assert_called_once_with(person.population.supplies_demands, person.inventory)
        expected_calls = [call(first_order, person), call(second_order, person)]
        self.exchange.place_order.assert_has_calls(expected_calls)

    def test_on_order_filled_reduces_money_when_buying(self):
        person = Person(Mock(), Mock(), Mock())
        person.money = 100

        person.on_order_filled(self.order, 7, 10)

        self.assertEqual(person.money, 30)

    def test_on_order_filled_adds_money_when_selling(self):
        person = Person(Mock(), Mock(), Mock())
        person.money = 100

        person.on_order_filled(self.order, 8, -6)

        self.assertEqual(person.money, 148)

    def test_on_order_filled_adds_resource_when_buying(self):
        resource = self.order.resource
        person = Person(Mock(), Mock(), Mock())

        person.on_order_filled(self.order, 6, 5)

        self.assertEqual(person.inventory[resource], 5)

    def test_on_order_updates_existing_resource_when_buying(self):
        resource = self.order.resource
        person = Person(Mock(), Mock(), Mock())
        person.inventory[resource] = 10

        person.on_order_filled(self.order, 6, 5)

        self.assertEquals(person.inventory[resource], 15)

    def test_on_order_filled_substracts_resource_when_selling(self):
        resource = self.order.resource
        person = Person(Mock(), Mock(), Mock())
        person.inventory[resource] = 6

        person.on_order_filled(self.order, 6, -5)

        self.assertEqual(person.inventory[resource], 1)

    def test_on_order_filled_removes_resource_if_ran_out(self):
        resource = self.order.resource
        person = Person(Mock(), Mock(), Mock())
        person.inventory[resource] = 7

        person.on_order_filled(self.order, 6, -7)

        self.assertNotIn(resource, person.inventory)

if __name__ == '__main__':
    unittest.main()
