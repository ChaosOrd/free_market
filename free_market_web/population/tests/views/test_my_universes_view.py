from unittest.mock import Mock, patch
from django.test import TestCase
from django.http import HttpRequest
from population.views import my_universes_view


class TestMyUniversesView(TestCase):

    def setUp(self):
        self.request = HttpRequest()
        self.request.user = Mock()
        self.render_patcher = patch('population.views.render')
        self.render_mock = self.render_patcher.start()
        self.login_required_pathcher = patch('population.views.login_required')
        self.login_required_mock = self.login_required_pathcher.start()
        self.universe_patcher = patch('population.views.Universe')
        self.universe_cls = self.universe_patcher.start()

    def tearDown(self):
        self.render_patcher.stop()
        self.login_required_pathcher.stop()
        self.universe_patcher.stop()

    def test_renders_my_universes_template(self):
        my_universes = self.universe_cls.objects.filter(owner=self.request.user)

        my_universes_view(self.request)

        self.render_mock.assert_called_once_with(
            self.request, 'my_universes.html', {'my_universes': my_universes})
