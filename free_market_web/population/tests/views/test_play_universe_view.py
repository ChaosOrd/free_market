from .base import BaseUniverseTestCase
from population.views import play_universe


class TestPlayUniverseView(BaseUniverseTestCase):

    def setUp(self):
        super().setUp()

    def tear_down(self):
        self.simulator_api_patcher.stop()

    def test_renders_play_summary(self):
        play_universe(self.request, 0)

        self.render_mock.assert_called_once_with(
            self.request, 'play_summary.html', {'universe_id': 0})

    def test_returns_render_result(self):
        self.assertEqual(play_universe(self.request, 0),
                         self.render_mock.return_value)
