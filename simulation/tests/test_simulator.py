import unittest
from unittest import TestCase
from unittest.mock import Mock, patch, call
from simulation.simulator import Simulator


class SimulatorTest(TestCase):

    def setUp(self):
        self.person_patcher = patch('simulation.simulator.Person')
        self.person_cls = self.person_patcher.start()

    def tearDown(self):
        self.person_cls.stop()

    def test_simulate_creates_persons_from_population(self):
        simulator = Simulator()
        universe = Mock()
        pop1 = Mock()
        pop2 = Mock()
        universe.populations = [pop1, pop2]

        simulator.simulate(universe)

        self.person_cls.from_population.assert_has_calls([call(pop1), call(pop2)],
                                                         any_order=True)

if __name__ == '__main__':
    unittest.main()
