import abc
from typing import Iterable

__author__ = 'chaosord'


class SupplyDemand(object):

    @abc.abstractproperty
    def resource(self) -> str:
        pass

    @abc.abstractproperty
    def value(self) -> float:
        pass


class Population(object):

    @abc.abstractproperty
    def name(self) -> str:
        pass

    @abc.abstractproperty
    def quantity(self) -> float:
        pass

    @abc.abstractproperty
    def supplies_demands(self) -> Iterable[SupplyDemand]:
        pass
