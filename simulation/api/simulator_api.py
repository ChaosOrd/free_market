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
