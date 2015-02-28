from django.test import TestCase
from population.forms import (SupplyDemandForm, INVALID_SD_VALUE_ERROR,
                              EMPTY_SD_VALUE_ERROR, EMPTY_RESOURCE_ERROR)
from unittest.mock import Mock, patch
from population.models import Resource


class TestSupplyDemandForm(TestCase):

    def setUp(self):
        self.supply_demand_patcher = patch('population.forms.SupplyDemand')
        self.supply_demand_cls = self.supply_demand_patcher.start()

    def tearDown(self):
        self.supply_demand_patcher.stop()

    def test_save_creates_a_supply_and_demand(self):
        create = self.supply_demand_cls.objects.create
        sd_form = SupplyDemandForm(data={'resource': 1, 'value': 3.5})
        resource = Resource.objects.create(id=1, name='Bread')
        population = Mock()

        sd_form.is_valid()
        sd_form.save(for_population=population)

        create.assert_called_once_with(population=population, resource=resource,
                                       value=3.5)

    def test_validation_for_non_numeric_value(self):
        sd_form = SupplyDemandForm(data={'resource': 1, 'value': 'three'})
        Resource.objects.create(id=1, name='Bread')

        self.assertFalse(sd_form.is_valid())
        self.assertEqual(sd_form.errors['value'], [INVALID_SD_VALUE_ERROR])

    def test_validation_for_empty_value(self):
        sd_form = SupplyDemandForm(data={'resource': 1})
        Resource.objects.create(id=1, name='Bread')

        self.assertFalse(sd_form.is_valid())
        self.assertEqual(sd_form.errors['value'], [EMPTY_SD_VALUE_ERROR])

    def test_validation_for_empty_resource(self):
        sd_form = SupplyDemandForm(data={'value': 'Bread'})

        self.assertFalse(sd_form.is_valid())
        self.assertEqual(sd_form.errors['resource'], [EMPTY_RESOURCE_ERROR])

    def test_sets_up_prefix_when_called_with_sd_num(self):
        sd_form = SupplyDemandForm(sd_num=1)

        self.assertEqual(sd_form.prefix, 'sd_1')

    def test_sets_tab_indices_when_called_with_sd_num(self):
        sd_form = SupplyDemandForm(sd_num=3)

        resource_tabindex = sd_form.fields['resource'].widget.attrs['tabindex']
        value_tabindex = sd_form.fields['value'].widget.attrs['tabindex']
        self.assertEqual(resource_tabindex, '8')
        self.assertEqual(value_tabindex, '9')

