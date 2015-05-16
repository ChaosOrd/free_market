from .base import BaseUniverseTestCase
from population.views import simulation_result
from unittest.mock import patch


class TestSimulationResultView(BaseUniverseTestCase):

    def setUp(self):
        super().setUp()
        self.simulate_patcher = patch('population.views.simulate')
        self.simulate_mock = self.simulate_patcher.start()

    def tearDown(self):
        self.simulate_patcher.stop()

    def test_retrieves_universe_by_id(self):
        simulation_result(self.request, 0)

        self.universe_cls.objects.get.assert_called_once_with(0)

    def test_calls_api_simulate(self):
        simulation_result(self.request, 0)

        self.simulate_mock.assert_called_once_with(self.universe)

    def test_retunrs_simulate_resunt(self):
        result = simulation_result(self.request, 0)

        self.assertEquals(result, self.simulate_mock.return_value)
