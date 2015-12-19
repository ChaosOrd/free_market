from unittest.mock import MagicMock


class SupplyDemandHelper(object):

    @classmethod
    def create_supply_mock(cls):
        supply_mock = MagicMock()
        supply_mock.is_supply.return_value, supply_mock.is_demand.return_value = True, False

        return supply_mock

    @classmethod
    def create_demand_mock(cls):
        demand_mock = MagicMock()
        demand_mock.is_supply.return_value, demand_mock.is_demand.return_value = False, True

        return demand_mock
