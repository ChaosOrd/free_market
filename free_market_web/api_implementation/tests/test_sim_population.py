from api_implementation.simulator_api import SimPopulation
from unittest import TestCase
from unittest.mock import Mock, patch


class TestSimPopulation(TestCase):

    def setUp(self):
        self.population = Mock()

        self.supply_demand_patcher = patch('api_implementation.simulator_api.SupplyDemand')
        self.supply_demand_mock = self.supply_demand_patcher.start()

        self.first_sd = Mock()
        self.first_sd.resource.name = 'Tools'
        self.first_sd.value = 3
        self.second_sd = Mock()
        self.second_sd.resource.name = 'Wheat'
        self.second_sd.value = 0.3
        self.supply_demand_mock.objects.filter.return_value = [self.first_sd, self.second_sd]

    def tearDown(self):
        self.supply_demand_patcher.stop()

    def test_from_population_copies_name(self):
        self.population.name = 'Farmers'

        sim_pop = SimPopulation.from_population(self.population)

        self.assertEquals(sim_pop.name, 'Farmers')

    def test_from_population_copies_qunatity(self):
        self.population.quantity = 10

        sim_pop = SimPopulation.from_population(self.population)

        self.assertEquals(sim_pop.quantity, 10)

    def test_from_population_gets_supplies_demands(self):
        SimPopulation.from_population(self.population)

        self.supply_demand_mock.objects.filter.assert_called_once_with(
            population=self.population)

    def test_from_population_copies_sd_resource_names(self):
        sim_pop = SimPopulation.from_population(self.population)

        first_sim_sd = sim_pop.supplies_demands[0]
        second_sim_sd = sim_pop.supplies_demands[1]

        self.assertEquals('Tools', first_sim_sd.resource)
        self.assertEquals('Wheat', second_sim_sd.resource)

    def test_from_population_copies_sd_values(self):
        sim_pop = SimPopulation.from_population(self.population)

        first_sim_sd = sim_pop.supplies_demands[0]
        second_sim_sd = sim_pop.supplies_demands[1]

        self.assertEquals(3, first_sim_sd.value)
        self.assertEquals(0.3, second_sim_sd.value)
