from api.simulator_api import PopulationBase
from exchange import Exchange
from strategies import SimpleStrategy, BaseStrategy


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
            self._persons.extend(person)

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

    def get_snapshots_dictionary(self):
        raise NotImplementedError()


class Person(object):
    MIN_RANDOM_PRICE = 100
    MAX_RANDOM_PRICE = 200
    INITIAL_MONEY = 1000
    MONEY_RESOURCE_NAME = 'Money'

    def __init__(self, population: PopulationBase, exchange: Exchange, strategy: BaseStrategy):
        self.population = population
        self.strategy = strategy
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
    def _single_person_from_population(cls, population, exchange):
        simple_strategy = SimpleStrategy(exchange)
        return Person(population=population, exchange=exchange, strategy=simple_strategy)

    def copy_initial(self) -> "Person":
        return Person(self.population, self.exchange, self.strategy)

    def copy_full(self):
        person = self.copy_initial()
        person.inventory = self.inventory.copy()
        return person

    def on_iteration(self):
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
