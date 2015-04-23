class Simulator(object):

    def simulate(self, universe):
        for pop in universe.populations:
            Person.from_population(pop)


class Person(object):

    @classmethod
    def from_population(cls, population):
        pass
