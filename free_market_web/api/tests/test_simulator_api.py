from unittest import TestCase
from unittest.mock import Mock, patch
from ..simulator_api import simulate


class TestSimulatorApi(TestCase):

    def setUp(self):
        self.universe = Mock()
        self.__patch_sim_universe()

    def __patch_sim_universe(self):
        self.sim_universe_patcher = patch('api.simulator_api.SimUniverse')
        self.sim_universe_cls = self.sim_universe_patcher.start()

    def tearDown(self):
        self.sim_universe_patcher.stop()

    def test_siumlates_converts_universe_to_sim_universe(self):
        simulate(self.universe)

        self.sim_universe_cls.from_universe.assert_called_once_with(self.universe)

    def test_simulate_returns_from_univeres_result(self):
        self.assertEquals(simulate(self.universe),
                          self.sim_universe_cls.from_universe.return_value)
