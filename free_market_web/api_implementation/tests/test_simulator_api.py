from unittest.mock import Mock, patch
from django.test import TestCase
from api_implementation.simulator_api import simulate


class TestSimulatorApi(TestCase):

    def setUp(self):
        super().setUp()
        self.universe = Mock()
        self.__patch_sim_universe()
        self.__patch_models()
        self.__patch_simulator()

    def __patch_models(self):
        self.population_patcher = patch('api_implementation.simulator_api.Population')
        self.population_patcher.start()
        self.supply_demand_patcher = patch('api_implementation.simulator_api.SupplyDemand')
        self.supply_demand_patcher.start()

    def __patch_sim_universe(self):
        self.sim_universe_patcher = patch('api_implementation.simulator_api.SimUniverse')
        self.sim_universe_cls = self.sim_universe_patcher.start()

    def __patch_simulator(self):
        self.simulator_patcher = patch('api_implementation.simulator_api.Simulator')
        self.simulator_cls = self.simulator_patcher.start()
        self.simulator_obj = self.simulator_cls.return_value

    def tearDown(self):
        self.sim_universe_patcher.stop()
        self.population_patcher.stop()
        self.supply_demand_patcher.stop()
        self.simulator_patcher.stop()

    def test_simulate_converts_universe_to_sim_universe(self):
        simulate(self.universe)

        self.sim_universe_cls.from_universe.assert_called_once_with(self.universe)

    def test_simulate_gets_simulation_result_dictionary(self):
        simulated_result = simulate(self.universe)

        self.simulator_obj.get_simulation_result_dictionary.assert_called_once_with()
        self.assertEquals(simulated_result, self.simulator_obj.get_simulation_result_dictionary.return_value)
