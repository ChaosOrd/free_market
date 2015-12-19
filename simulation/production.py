from api.simulator_api import SupplyDemandBase


class Craft(object):

    def calculate_production_result(self, supply_demand: SupplyDemandBase, inventory: dict):
        if supply_demand.is_demand():
            raise CanNotProduceDemandException()

        if supply_demand.resource not in inventory:
            inventory[supply_demand.resource] = supply_demand.value
        else:
            inventory[supply_demand.resource] += supply_demand.value

        return inventory


class CanNotProduceDemandException(Exception):
    pass
