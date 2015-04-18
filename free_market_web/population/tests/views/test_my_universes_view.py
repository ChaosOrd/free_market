from .base import BaseUniverseTestCase
from django.test import TestCase
from unittest.mock import Mock, patch
from population.views import my_universes_view
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required


class TestMyUniversesView(TestCase):

    def setUp(self):
        self.request = HttpRequest()
        self.request.user = Mock()
        self.render_patcher = patch('population.views.render')
        self.render_mock = self.render_patcher.start()
        self.login_required_pathcher = patch('population.views.login_required')
        self.login_required_mock = self.login_required_pathcher.start()

    def tearDown(self):
        self.render_patcher.stop()
        self.login_required_pathcher.stop()

    def test_renders_my_views_template(self):
        my_universes_view(self.request)

        self.render_mock.assert_called_once_with(
            self.request, 'my_universes.html')
