from .base import BaseUniverseTestCase
from population.views import simulation_result
from unittest.mock import patch


class TestSimulationResultView(BaseUniverseTestCase):

    def setUp(self):
        super().setUp()
        self.simulate_patcher = patch('population.views.simulate')
        self.simulate_mock = self.simulate_patcher.start()
        self.json_response_patcher = patch('population.views.JsonResponse')
        self.json_response_mock = self.json_response_patcher.start()

    def tearDown(self):
        self.simulate_patcher.stop()
        self.json_response_patcher.stop()

    def test_retrieves_universe_by_id(self):
        simulation_result(self.request, 0)

        self.universe_cls.objects.get.assert_called_once_with(id=0)

    def test_calls_api_simulate(self):
        simulation_result(self.request, 0)

        self.simulate_mock.assert_called_once_with(self.universe)

    def test_returns_simulate_result(self):
        result = simulation_result(self.request, 0)

        self.json_response_mock.assert_called_once_with(self.simulate_mock.return_value)
        self.assertEquals(result, self.json_response_mock.return_value)
