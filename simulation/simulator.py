from api.simulator_api import PopulationBase
from exchange import Exchange
from strategies import SimpleStrategy, BaseStrategy
from production import Craft


class Simulator(object):

    NUM_OF_ITERATIONS = 100

    def __init__(self):
        self._persons = []
        self._snapshots = []

    @property
    def snapshots(self):
        return self._snapshots

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
            print('Simulated {} iterations'.format(iteration))

    def _simulate_iteration(self):
        snapshot = []
        for person in self._persons:
            person.on_iteration()
            snapshot.append(person.copy_full())
        self.snapshots.append(snapshot)

    def get_simulation_result_dictionary(self):
        snapshots = []
        for snapshot in self.snapshots:
            current_snapshot = []
            for person in snapshot:
                current_snapshot.append(person.to_dict())
            snapshots.append(current_snapshot)

        return {'snapshots': snapshots}


class Person(object):
    INITIAL_MONEY = 1000
    MONEY_RESOURCE_NAME = 'Money'

    def __init__(self, population: PopulationBase, exchange: Exchange, strategy: BaseStrategy):
        self.population = population
        self.strategy = strategy
        self.exchange = exchange
        self.inventory = {self.MONEY_RESOURCE_NAME: self.INITIAL_MONEY}
        self.craft = Craft()

    @property
    def money(self):
        return self.inventory[self.MONEY_RESOURCE_NAME]

    @money.setter
    def money(self, value):
        self.inventory[self.MONEY_RESOURCE_NAME] = value

    @classmethod
    def from_population(cls, population, exchange):
        simple_strategy = SimpleStrategy(exchange)
        return Person(population=population, exchange=exchange, strategy=simple_strategy)

    def copy_initial(self) -> "Person":
        return Person(self.population, self.exchange, self.strategy)

    def copy_full(self):
        person = self.copy_initial()
        person.inventory = self.inventory.copy()
        return person

    def on_iteration(self):
        self._produce_resources()
        self._place_orders()

    def _produce_resources(self):
        for supply_demand in self.population.supplies_demands:
            if supply_demand.is_supply():
                self.inventory = self.craft.calculate_production_result(supply_demand, self.inventory)

    def _place_orders(self):
        working_orders = self.exchange.get_orders_sent_by(self)
        orders_to_place = self.strategy.make_move(self.population.supplies_demands, self.inventory, working_orders)
        for order in orders_to_place:
            self.exchange.place_order(order, self)

    def on_order_filled(self, order, price, quantity):
        self.money -= price * quantity
        resource = order.resource
        self._add_resource_quantity(resource, quantity)

    def _add_resource_quantity(self, resource, quantity):
        if resource in self.inventory:
            self.inventory[resource] += quantity
        else:
            self.inventory[resource] = quantity

        if self.inventory[resource] == 0:
            self.inventory.pop(resource)

    def to_dict(self):
        return {'population': self.population.to_dict(), 'inventory': self.inventory}
