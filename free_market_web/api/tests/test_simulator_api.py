from unittest import TestCase
from unittest.mock import patch
from ..simulator_api import simulate


class TestSimulatorApi(TestCase):

    def setUp(self):
        self.__patch_universe()
        self.__patch_sim_universe()

    def __patch_universe(self):
        self.universe_patcher = patch('api.simulator_api.Universe')
        self.universe_cls = self.universe_patcher.start()
        self.universe = self.universe_cls.return_value

    def __patch_sim_universe(self):
        self.sim_universe_patcher = patch('api.simulator_api.SimUniverse')
        self.sim_universe_cls = self.sim_universe_patcher.start()

    def tearDown(self):
        self.universe_patcher.stop()
        self.sim_universe_patcher.stop()

    def test_siumlates_converts_universe_to_sim_universe(self):
        simulate(self.universe)

        self.sim_universe_cls.from_universe.assert_called_once_with(self.universe)
