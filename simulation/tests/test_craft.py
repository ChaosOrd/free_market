from unittest import TestCase

from production import Craft, CanNotProduceDemandException
from tests.helpers import SupplyDemandHelper


class TestCraft(TestCase):

    def setUp(self):
        self.initial_inventory = {'Wheat': 3.4}

    def _create_zero_value_wheat_supply(self):
        supply = SupplyDemandHelper.create_supply_mock()
        supply.resource = 'Wheat'
        supply.value = 0

        return supply

    def _create_beer_supply(self):
        supply = SupplyDemandHelper.create_supply_mock()
        supply.resource = 'Beer'
        supply.value = 2.3

        return supply

    def _create_tools_demand(self):
        demand = SupplyDemandHelper.create_demand_mock()
        demand.resource = 'Tools'
        demand.value = -4.6

        return demand

    def test_calculate_production_result_returns_inventory_as_is_if_supply_is_zero(self):
        supply = self._create_zero_value_wheat_supply()

        craft = Craft()

        self.assertEquals(craft.calculate_production_result(supply, self.initial_inventory), self.initial_inventory)

    def test_calculate_production_result_adds_new_resource_to_inventory(self):
        supply = self._create_beer_supply()
        craft = Craft()

        self.assertEquals(craft.calculate_production_result(supply, self.initial_inventory),
                          {'Wheat': 3.4, 'Beer': 2.3})

    def test_calculate_production_result_adds_to_existing_resource_value(self):
        supply = self._create_beer_supply()
        self.initial_inventory['Beer'] = 0.4
        craft = Craft()

        new_inventory = craft.calculate_production_result(supply, self.initial_inventory)
        self.assertAlmostEqual(new_inventory['Wheat'], 3.4)
        self.assertAlmostEqual(new_inventory['Beer'], 2.7)

    def test_calculate_production_result_raises_exception_if_got_demand(self):
        demand = self._create_tools_demand()
        craft = Craft()

        self.assertRaises(CanNotProduceDemandException, craft.calculate_production_result,
                          demand, self.initial_inventory)
