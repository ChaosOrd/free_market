import abc
from typing import Mapping, List, Iterable
import random

from api.simulator_api import SupplyDemand
from exchange import Exchange, Order

__author__ = 'chaosord'


class BaseStrategy(object):

    @abc.abstractmethod
    def make_move(self, supplies_and_demands: Iterable[SupplyDemand], inventory: Mapping) -> Iterable[Order]:
        pass


class SimpleStrategy(BaseStrategy):

    MIN_RANDOM_PRICE = 100
    MAX_RANDOM_PRICE = 200

    def __init__(self, exchange: Exchange):
        self._exchange = exchange

    def make_move(self, supplies_and_demands: Iterable[SupplyDemand], inventory: Mapping) -> Iterable[Order]:
        orders = []
        for supply_demand in supplies_and_demands:
            order = self._get_order_handling_supply_demand(supply_demand)
            if order is not None:
                orders.append(order)

        return orders

    def _get_order_handling_supply_demand(self, supply_demand):
        if supply_demand.value < 0:
            order = self._create_buy_order(supply_demand)
        else:
            order = self._create_sell_order(supply_demand)
        return order

    def _create_buy_order(self, demand: SupplyDemand):
        best_sell = self._exchange.get_best_sell()
        if best_sell is not None:
            return Order(resource=demand.resource, price=best_sell.price, quantity=demand.value)

        return None

    def _create_sell_order(self, supply: SupplyDemand):
        return Order(resource=supply.resource,
                     price=random.randint(self.MIN_RANDOM_PRICE, self.MAX_RANDOM_PRICE),
                     quantity=supply.value)
