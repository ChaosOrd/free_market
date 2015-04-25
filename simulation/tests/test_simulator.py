from collections import Counter
import unittest
from unittest import TestCase, skip
from unittest.mock import Mock, patch, call
from simulation.simulator import Simulator


class SimulatorTest(TestCase):

    def setUp(self):
        self.init_patchers()
        self.universe = Mock()
        self.init_populations()
        self.init_persons()

    def init_patchers(self):
        self.person_patcher = patch('simulation.simulator.Person')
        self.person_cls = self.person_patcher.start()
        self.exchange_patcher = patch('simulation.simulator.Exchange')
        self.exchange_cls = self.exchange_patcher.start()
        self.exchange = self.exchange_cls.return_value

    def init_populations(self):
        self.pop1 = Mock()
        self.pop1.quantity = 1
        self.pop2 = Mock()
        self.pop2.quantity = 2
        self.universe.populations = [self.pop1, self.pop2]

    def init_persons(self):
        self.person1 = Mock()
        self.person2 = Mock()
        self.person3 = Mock()
        self.person_cls.from_population.side_effect = \
            [self.person1, self.person2, self.person3]

    def tearDown(self):
        self.person_patcher.stop()
        self.exchange_patcher.stop()

    def test_create_persons_creates_persons_from_population(self):
        simulator = Simulator()

        simulator._create_persons(self.universe)

        self.person_cls.from_population.assert_has_calls(
            [call(self.pop1, self.exchange), call(self.pop2, self.exchange)],
            any_order=True)

    def test_create_persons_stores_persons_in_list(self):
        simulator = Simulator()

        simulator._create_persons(self.universe)

        self.assertIn(self.person1, simulator._persons)
        self.assertIn(self.person2, simulator._persons)
        self.assertIn(self.person3, simulator._persons)

    def test_create_persons_creates_exchange(self):
        simulator = Simulator()

        simulator._create_persons(self.universe)

        self.exchange_cls.assert_called_once_with()

    @skip('Implement later')
    def test_simulate_calls_methods_in_right_order(self):
        self_mock = Mock()

        Simulator.simulate(self_mock, self.universe)

        self_mock._create_persons.assert_has_calls(
            call(self_mock, self.universe), call(self_mock, self.universe))

    @skip('Implement later')
    def test_simulate_calls_person_tick_default_amount_of_times(self):
        simulator = Simulator()

        simulator.simulate(self.universe)

        self.person1.tick.assert_called_once_with()
        self.person2.tick.assert_called_once_with()
        self.person3.tick.assert_called_once_with()

if __name__ == '__main__':
    unittest.main()