from django.test import TestCase
from population.forms import SupplyDemandForm
from unittest.mock import patch
from population.models import Resource


class TestSupplyDemandForm(TestCase):

    def setUp(self):
        self.supply_demand_patcher = patch('population.forms.SupplyDemand')
        self.supply_demand_cls = self.supply_demand_patcher.start()

    def tearDown(self):
        self.supply_demand_patcher.stop()

    def test_save_creates_a_supply_and_demand(self):
        create_new = self.supply_demand_cls.create_new
        sd_form = SupplyDemandForm(data={'resource': 1,'value': 3.5})
        resource = Resource.create_new(id=1, value='Bread')

        sd_form.is_valid()
        sd_form.save(for_population=2)

        create_new.assert_called_once_with(
            population=2, resource=1, value=3.5)
