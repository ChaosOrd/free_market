from population.models import Population, SupplyDemand


def simulate(universe):
    return SimUniverse.from_universe(universe)


class SimUniverse(object):

    def __init__(self, populations):
        self.__populations = populations

    @property
    def populations(self):
        return self.__populations

    @classmethod
    def from_universe(cls, universe):
        sim_populations = []
        populations = Population.filter(universe=universe)
        for pop in populations:
            sim_populations.append(SimPopulation.from_population(pop))

        return SimUniverse(sim_populations)


class SimPopulation(object):
    def __init__(self, name, quantity, supplies_demands):
        self.__name = name
        self.__quantity = quantity
        self.__supplies_demands = supplies_demands

    @property
    def name(self):
        return self.__name

    @property
    def quantity(self):
        return self.__quantity

    @property
    def supplies_demands(self):
        return self.__supplies_demands

    @classmethod
    def from_population(cls, population):
        pop_supplies_demands = SupplyDemand.filter(population=population)
        sim_supply_demands = []

        for pop_sd in pop_supplies_demands:
            sim_supply_demands.append(SimSupplyDemand(pop_sd.resource.name,
                                                      pop_sd.value))

        return SimPopulation(population.name, population.quantity,
                             sim_supply_demands)

class SimSupplyDemand(object):

    def __init__(self, resource, value):
        self.__resource = resource
        self.__value = value

    @property
    def resource(self):
        return self.__resource

    @property
    def value(self):
        return self.__value
