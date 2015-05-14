from .base import BaseUniverseTestCase
from population.views import play_universe
from unittest.mock import patch


class TestPlayUniverseView(BaseUniverseTestCase):

    def setUp(self):
        super().setUp()
        self.simulator_api_patcher = patch('population.views.simulator_api')
        self.simulator_api_mock = self.simulator_api_patcher.start()

    def tear_down(self):
        self.simulator_api_patcher.stop()

    def test_renders_play_summary(self):
        play_universe(self.request, 0)
        simulate = self.simulator_api_mock.simulate

        self.render_mock.assert_called_once_with(
            self.request, 'play_summary.html',
            {'simulation_data': simulate.return_value})

    def test_returns_render_result(self):
        self.assertEqual(play_universe(self.request, 0),
                         self.render_mock.return_value)

    def test_gets_universe_by_id(self):
        play_universe(self.request, 0)

        self.universe_cls.objects.get.assert_called_once_with(id=0)

    def test_calse_simulate_with_universe(self):
        play_universe(self.request, 0)

        self.simulator_api_mock.simulate.assert_called_once_with(self.universe)
