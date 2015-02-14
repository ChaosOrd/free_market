from django.http.request import HttpRequest
from django.test import TestCase
from unittest.mock import patch
from population.views import supply_demand_form


class TestSupplyDemandFormView(TestCase):

    def setUp(self):
        self.request = HttpRequest()
        self.request.method = 'GET'

    @patch('population.views.SupplyDemandForm')
    @patch('population.views.render')
    def test_renders_supply_demand_form_template(self, render_mock, form_cls):
        form_obj = form_cls.return_value

        supply_demand_form(self.request)

        render_mock.assert_called_once_with(self.request,
                                            'supply_demand_form.html',
                                            {'form': form_obj})
