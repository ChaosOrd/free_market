from population.models import Population, SupplyDemand
from simulation.simulator import Simulator
from simulation.api.simulator_api import PopulationBase, SupplyDemandBase


def simulate(universe):
    simulator = Simulator()
    sim_universe = SimUniverse.from_universe(universe)
    simulator.simulate(sim_universe)
    return simulator.get_snapshots_dictionary()


class SimulatorApi(object):

    @classmethod
    def simulate(cls, universe):
        simulator = Simulator()
        sim_universe = SimUniverse.from_universe(universe)
        simulator.simulate(sim_universe)
        return simulator.snapshots


class SimUniverse(object):

    def __init__(self, populations):
        self.__populations = populations

    @property
    def populations(self):
        return self.__populations

    @classmethod
    def from_universe(cls, universe):
        sim_populations = []
        populations = Population.objects.filter(universe=universe)
        for pop in populations:
            sim_populations.append(SimPopulation.from_population(pop))

        return SimUniverse(sim_populations)


class SimPopulation(PopulationBase):
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
        pop_supplies_demands = SupplyDemand.objects.filter(population=population)
        sim_supply_demands = []

        for pop_sd in pop_supplies_demands:
            sim_supply_demands.append(SimSupplyDemand(pop_sd.resource.name,
                                                      pop_sd.value))

        return SimPopulation(population.name, population.quantity,
                             sim_supply_demands)


class SimSupplyDemand(SupplyDemandBase):

    def __init__(self, resource, value):
        self.__resource = resource
        self.__value = value

    @property
    def resource(self):
        return self.__resource

    @property
    def value(self):
        return self.__value
