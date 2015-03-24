from django.http.request import HttpRequest
from django.test import TestCase
from population.views import delete_population
from unittest.mock import patch


class TestDeletePopulationView(TestCase):

    def setUp(self):
        self.request = HttpRequest()
        self.request.method = 'POST'
        self.create_class_mocks()

    def create_class_mocks(self):
        self.population_model_patcher = patch('population.views.Population')
        self.population_model_cls = self.population_model_patcher.start()
        self.redirect_patcher = patch('population.views.redirect')
        self.redirect_mock = self.redirect_patcher.start()

    def tearDown(self):
        self.tear_down_class_mocks()

    def tear_down_class_mocks(self):
        self.population_model_patcher.stop()
        self.redirect_patcher.stop()

    def test_redirects_to_universe_view(self):
        population = self.population_model_cls.objects.get(id=0)

        delete_population(self.request, 0)

        self.redirect_mock.assert_called_once_with(population.universe)

    def test_deletes_population(self):
        population = self.population_model_cls.objects.get(id=0)

        delete_population(self.request, 0)

        population.delete.assert_called_once_with()
