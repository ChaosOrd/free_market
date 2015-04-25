class Simulator(object):

    def __init__(self):
        self._persons = []

    def simulate(self, universe):
        self._create_persons(universe)

    def _create_persons(self, universe):
        exchange = Exchange()

        for pop in universe.populations:
            self._fill_persons_from_population(pop, exchange)

    def _fill_persons_from_population(self, pop, exchange):
        for person_idx in range(pop.quantity):
            person = Person.from_population(pop, exchange)
            self._persons.append(person)


class Person(object):

    @classmethod
    def from_population(cls, population, exchange):
        pass

    def tick(self):
        pass

class Exchange(object):
    pass
