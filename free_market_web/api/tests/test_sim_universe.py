from unittest import TestCase
from unittest.mock import Mock, patch, call
from api.simulator_api import SimUniverse


class TestSimUniverse(TestCase):

    def setUp(self):
        self.population_patcher = patch('api.simulator_api.Population')
        self.population_cls = self.population_patcher.start()
        self.pop1 = Mock()
        self.pop2 = Mock()
        self.population_cls.filter.return_value = [self.pop1, self.pop2]

        self.universe_mock = Mock()
        self.sim_population_patcher = patch('api.simulator_api.SimPopulation')
        self.sim_population_mock = self.sim_population_patcher.start()

    def tearDown(self):
        self.population_patcher.stop()
        self.sim_population_patcher.stop()

    def test_from_universe_retreives_universe_populations(self):
        SimUniverse.from_universe(self.universe_mock)

        self.population_cls.filter.assert_called_once_with(
            universe=self.universe_mock)

    def test_from_universe_creates_sim_populations_for_each_pop(self):
        SimUniverse.from_universe(self.universe_mock)

        expected_calls = [call(self.pop1), call(self.pop2)]
        self.sim_population_mock.from_population.assert_has_calls(
            expected_calls, any_order=True)

    def test_from_unverse_returns_sim_universe_with_populations(self):
        sim_pop1 = Mock()
        sim_pop2 = Mock()
        sim_populations = [sim_pop1, sim_pop2]
        self.sim_population_mock.from_population.side_effect = sim_populations

        sim_universe = SimUniverse.from_universe(self.universe_mock)

        self.assertEquals(sim_universe.populations, sim_populations)
