import random
from .exchange import Order
from .exchange import Exchange


class Simulator(object):

    NUM_OF_ITERATIONS = 100

    def __init__(self):
        self._persons = []
        self.__snapshots = []

    @property
    def snapshots(self):
        return self.__snapshots

    def simulate(self, universe):
        self._create_persons(universe)
        self._run_iterations()

    def _create_persons(self, universe):
        exchange = Exchange()

        for pop in universe.populations:
            self._fill_persons_from_population(pop, exchange)

    def _fill_persons_from_population(self, pop, exchange):
        for person_idx in range(pop.quantity):
            person = Person.from_population(pop, exchange)
            self._persons.append(person)

    def _run_iterations(self):
        for iteration in range(self.NUM_OF_ITERATIONS):
            self._simulate_iteration()

    def _simulate_iteration(self):
        snapshot = []
        for person in self._persons:
            person.on_iteration()
            snapshot.append(person.copy_full())
        self.snapshots.append(snapshot)


class Person(object):
    MIN_RANDOM_PRICE = 100
    MAX_RANDOM_PRICE = 200
    INITIAL_MONEY = 1000
    MONEY_RESOURCE_NAME = 'Money'

    def __init__(self, population, exchange):
        self.population = population
        self.exchange = exchange
        self.inventory = {self.MONEY_RESOURCE_NAME: self.INITIAL_MONEY}

    @property
    def money(self):
        return self.inventory[self.MONEY_RESOURCE_NAME]

    @money.setter
    def money(self, value):
        self.inventory[self.MONEY_RESOURCE_NAME] = value

    @classmethod
    def from_population(cls, population, exchange):
        persons = []
        initial_person = cls._single_person_from_population(population, exchange)

        for person_idx in range(population.quantity):
            persons.append(initial_person.copy_initial())

        return persons

    @classmethod
    def _single_person_from_population(self, population, exchange):
        return Person(population=population, exchange=exchange)

    def copy_initial(self) -> "Person":
        return Person(self.population, self.exchange)

    def copy_full(self):
        person = self.copy_initial()
        person.inventory = self.inventory.copy()
        return person

    def on_iteration(self):
        for supply_demand in self.population.supplies_demands:
            order = self._create_order_to_handle_supply_demand(supply_demand)
            self.exchange.place_order(order)

    def _create_order_to_handle_supply_demand(self, supply_demand):
        if (supply_demand.value < 0):
            order = self._create_buy_order(supply_demand)
        else:
            order = self._create_sell_order(supply_demand)
        return order

    def _create_sell_order(self, supply):
        order = Order(sender=self, resource=supply.resource,
                      price=random.randint(self.MIN_RANDOM_PRICE,
                                           self.MAX_RANDOM_PRICE),
                      quantity=supply.value)
        return order

    def _create_buy_order(self, demand):
        best_sell = self.exchange.get_best_sell()
        order = Order(sender=self, resource=demand.resource,
                      price=best_sell.price,
                      quantity=demand.value)
        return order

    def on_order_filled(self, order, price, quantity):
        self.money += price * quantity
        resource = order.resource
        self._add_resource_quantity(resource, -quantity)

    def _add_resource_quantity(self, resource, quantity):
        if resource in self.inventory:
            self.inventory[resource] += quantity
        else:
            self.inventory[resource] = quantity

        if self.inventory[resource] == 0:
            self.inventory.pop(resource)
