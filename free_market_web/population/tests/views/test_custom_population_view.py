from django.http.request import HttpRequest
from django.test import TestCase
from unittest.mock import patch
from population.views import custom_population


class CustomPopulationTest(TestCase):

    def setUp(self):
        self.request = HttpRequest()
        self.request.method = 'POST'
        self.request.POST['name'] = 'Farmers'
        self.request.POST['quantity'] = 100

    def test_renders_custom_population(self):
        response = self.client.get('/custom_population/')
        self.assertTemplateUsed(response, 'custom_population.html')

    @patch('population.views.NewPopulationForm')
    def test_passes_POST_data_to_NewPopulationForm(self, form_class_mock):
        custom_population(self.request)
        form_class_mock.assert_called_once_with(data=self.request.POST)

    @patch('population.views.NewPopulationForm')
    def test_saves_form_if_form_is_valid(self, form_class_mock):
        form_object_mock = form_class_mock.return_value
        form_object_mock.is_valid.return_value = True

        custom_population(self.request)

        form_object_mock.save.assert_called_once_with()

    @patch('population.views.NewPopulationForm')
    def test_does_not_save_if_form_is_not_valid(self, form_class_mock):
        form_object_mock = form_class_mock.return_value
        form_object_mock.is_valid.return_value = False

        custom_population(self.request)

        self.assertFalse(form_object_mock.save.called)

    @patch('population.views.NewPopulationForm')
    @patch('population.views.render')
    def test_custom_population_passes_form_to_template(
        self, render_mock, form_class_mock
    ):
        form_object_mock = form_class_mock.return_value
        self.request.method = 'GET'

        custom_population(self.request)

        render_mock.assert_called_once_with(
            self.request, 'custom_population.html', {'form': form_object_mock})

    @patch('population.views.NewPopulationForm')
    @patch('population.views.redirect')
    def test_redirects_to_form_save_return_value(self, redirect_mock, form_class_mock):
        form_object_mock = form_class_mock.return_value

        custom_population(self.request)

        redirect_mock.assert_called_once_with(
            form_object_mock.save.return_value)
