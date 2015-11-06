from unittest import TestCase
from api.simulator_api import SupplyDemandBase

__author__ = 'chaosord'


class SupplyDemandImplementation(SupplyDemandBase):

    @property
    def value(self) -> float:
        return 2.4

    @property
    def resource(self) -> str:
        return 'Beer'


class TestSupplyDemandBase(TestCase):

    def test_to_dict_returns_correct_data(self):
        supply_demand = SupplyDemandImplementation()

        self.assertEquals(supply_demand.to_dict(), {'resource': 'Beer', 'value': 2.4})
