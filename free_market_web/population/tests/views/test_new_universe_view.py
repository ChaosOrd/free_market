from django.http.request import HttpRequest
from django.test import TestCase
from unittest.mock import patch
from population.views import new_universe


class CustomPopulationTest(TestCase):

    def setUp(self):
        self.request = HttpRequest()
        self.request.method = 'POST'
        self.request.POST['name'] = 'Farmers'
        self.request.POST['quantity'] = 100

    def test_renders_new_universe(self):
        response = self.client.get('/new_universe/')
        self.assertTemplateUsed(response, 'new_universe.html')

    @patch('population.views.NewPopulationForm')
    def test_passes_POST_data_to_NewPopulationForm(self, form_class_mock):
        new_universe(self.request)
        form_class_mock.assert_called_once_with(data=self.request.POST)

    @patch('population.views.NewPopulationForm')
    def test_saves_form_if_form_is_valid(self, form_class_mock):
        form_object_mock = form_class_mock.return_value
        form_object_mock.is_valid.return_value = True

        new_universe(self.request)

        form_object_mock.save.assert_called_once_with()

    @patch('population.views.NewPopulationForm')
    def test_does_not_save_if_form_is_not_valid(self, form_class_mock):
        form_object_mock = form_class_mock.return_value
        form_object_mock.is_valid.return_value = False

        new_universe(self.request)

        self.assertFalse(form_object_mock.save.called)

    @patch('population.views.NewPopulationForm')
    @patch('population.views.render')
    def test_passes_form_to_template(
        self, render_mock, form_class_mock
    ):
        form_object_mock = form_class_mock.return_value
        self.request.method = 'GET'

        new_universe(self.request)

        render_mock.assert_called_once_with(
            self.request, 'new_universe.html', {'form': form_object_mock})

    @patch('population.views.NewPopulationForm')
    @patch('population.views.redirect')
    def test_redirects_to_form_save_return_value(self, redirect_mock, form_class_mock):
        form_object_mock = form_class_mock.return_value

        new_universe(self.request)

        redirect_mock.assert_called_once_with(
            form_object_mock.save.return_value)
