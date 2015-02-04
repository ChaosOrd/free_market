from django.http.request import HttpRequest
from django.test import TestCase
from unittest.mock import patch
from population.views import resource_form


class TestUniverseView(TestCase):

    def setUp(self):
        self.request = HttpRequest()
        self.request.method = 'GET'

    @patch('population.views.ResourceForm')
    @patch('population.views.render')
    def test_renders_resource_form_template(self, render_mock, form_cls):
        form_obj = form_cls.return_value

        resource_form(self.request)

        render_mock.assert_called_once_with(self.request, 'resource_form.html',
                                            {'form': form_obj})
