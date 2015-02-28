from django.http.request import HttpRequest
from django.test import TestCase
from unittest.mock import patch
from population.views import supply_demand_form


class TestSupplyDemandFormView(TestCase):

    def setUp(self):
        self.request = HttpRequest()
        self.request.method = 'GET'
        self.render_patcher = patch('population.views.render')
        self.render = self.render_patcher.start()
        self.form_patcher = patch('population.views.SupplyDemandForm')
        self.form_cls = self.form_patcher.start()
        self.form_obj = self.form_cls.return_value

    def tearDown(self):
        self.render_patcher.stop()
        self.form_patcher.stop()

    def test_renders_supply_demand_form_template(self):
        supply_demand_form(self.request, 1)

        self.render.assert_called_once_with(self.request,
                                            'supply_demand_form.html',
                                            {'form': self.form_obj})

    def test_creates_supply_demand_form_with_prefix(self):
        supply_demand_form(self.request, 1)

        self.form_cls.assert_called_once_with(prefix='sd_1')
