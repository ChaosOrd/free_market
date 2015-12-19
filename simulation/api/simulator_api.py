import abc
from typing import Iterable

__author__ = 'chaosord'


class SupplyDemandBase(object):

    @abc.abstractproperty
    def resource(self) -> str:
        pass

    @abc.abstractproperty
    def value(self) -> float:
        pass

    def is_demand(self):
        return self.value < 0

    def is_supply(self):
        return not self.is_demand()

    def to_dict(self):
        return {'resource': self.resource, 'value': self.value}


class PopulationBase(object):

    @abc.abstractproperty
    def name(self) -> str:
        pass

    @abc.abstractproperty
    def quantity(self) -> float:
        pass

    @abc.abstractproperty
    def supplies_demands(self) -> Iterable[SupplyDemandBase]:
        pass

    def to_dict(self):
        supplies_demands = [supply_demand.to_dict() for supply_demand in self.supplies_demands]
        return {'name': self.name, 'supplies_demands': supplies_demands}
