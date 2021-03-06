import unittest
from unittest import TestCase
from unittest.mock import Mock, patch, call, MagicMock
from simulator import Simulator


class SimulatorTest(TestCase):

    def setUp(self):
        self.init_patchers()
        self.universe = Mock()
        self.init_populations()
        self.init_persons()
        self.calls = []

    def init_patchers(self):
        self.person_patcher = patch('simulator.Person')
        self.person_cls = self.person_patcher.start()
        self.exchange_patcher = patch('simulator.Exchange')
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

        self.person_cls.from_population.side_effect = [self.person1, self.person2, self.person3]

    def add_call(self, method_name):
        self.calls.append(method_name)

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

    def test_simulate_calls_methods_in_right_order(self):
        simulator = Simulator()
        simulator._create_persons = Mock()
        simulator._run_iterations = Mock()

        def create_persons_called(*args, **kwargs):
            self.calls.append("create_persons")

        simulator._create_persons.side_effect = create_persons_called

        def run_iterations_called(*args, **kwargs):
            self.calls.append("run_iterations")

        simulator._run_iterations.side_effect = run_iterations_called

        simulator.simulate(self.universe)

        self.assertEquals(self.calls[0], 'create_persons')
        self.assertEquals(self.calls[1], 'run_iterations')

    def test_run_iterations_calls_simulate_iteration_default_number_of_times(self):
        simulator = Simulator()
        simulator._simulate_iteration = Mock()
        Simulator.NUM_OF_ITERATIONS = 10

        simulator._run_iterations()

        calls = [call() for idx in range(10)]
        simulator._simulate_iteration.assert_has_calls(calls)

    def test_simulate_iteration_calls_on_iteration_on_each_person(self):
        simulator = Simulator()
        simulator._persons = [self.person1, self.person2, self.person3]

        simulator._simulate_iteration()

        self.person1.on_iteration.assert_called_once_with()
        self.person2.on_iteration.assert_called_once_with()
        self.person3.on_iteration.assert_called_once_with()

    def test_simulate_iteration_copies_each_person_for_snapshot(self):
        simulator = Simulator()
        simulator._persons = [self.person1, self.person2]

        simulator._simulate_iteration()

        self.person1.copy_full.assert_called_once_with()
        self.person2.copy_full.assert_called_once_with()

    def test_simulate_iteration_adds_copied_persons(self):
        simulator = Simulator()
        simulator._persons = [self.person1, self.person2]

        simulator._simulate_iteration()

        self.assertIn(self.person1.copy_full.return_value, simulator.snapshots[0])
        self.assertIn(self.person2.copy_full.return_value, simulator.snapshots[0])

    def test_get_simulation_results_dictionary_returns_snapshots(self):
        simulator = Simulator()
        person1_snapshot1 = MagicMock()
        person2_snapshot1 = MagicMock()
        person1_snapshot2 = MagicMock()
        person2_snapshot2 = MagicMock()

        simulator._snapshots = [[person1_snapshot1, person2_snapshot1],
                                [person1_snapshot2, person2_snapshot2]]

        simulation_result = simulator.get_simulation_result_dictionary()
        self.assertEquals(simulation_result, {'snapshots': [[person1_snapshot1.to_dict.return_value,
                                                            person2_snapshot1.to_dict.return_value],
                                                            [person1_snapshot2.to_dict.return_value,
                                                             person2_snapshot2.to_dict.return_value]]})

if __name__ == '__main__':
    unittest.main()
