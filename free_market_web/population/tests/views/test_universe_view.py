from django.http.request import HttpRequest
from django.test import TestCase
from population.views import universe
from unittest.mock import patch


class TestUniverseView(TestCase):

    def setUp(self):
        self.request = HttpRequest()
        self.request.method = 'GET'

    @patch('population.views.NewPopulationForm')
    @patch('population.views.Universe')
    @patch('population.views.render')
    def test_renderes_universe_template_with_universe_and_form(
        self, render, universe_cls, population_form_cls
    ):
        universe_obj = universe_cls.get.return_value
        form_obj = population_form_cls.return_value

        universe(self.request, 1)

        universe_cls.get.assert_called_once_with(universe_id=1)
        render.assert_called_once_with(self.request, 'universe.html', {
            'universe': universe_obj, 'form': form_obj
        })
