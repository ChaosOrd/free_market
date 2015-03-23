from .base import FunctionalTest
from population.models import Resource, Population, Universe, SupplyDemand


class CreatePopulationWithSupplyAndDemandTest(FunctionalTest):

    def setUp(self):
        super().setUp()
        self._create_resource_fixtures()
        self._create_universe_fixtures()
        self._create_population_fixtures()
        self._create_supply_demand_fixtures()

    def test_population_deletion(self):
        # Uncle Bob decides to check out the previously created universe
        universe_url = self.live_server_url + '/universe/1/'
        self.browser.get(universe_url)

        self.fail(msg='Continue the test')

    def _create_resource_fixtures(self):
        self.milk = Resource.objects.create(name='Milk')
        self.bread = Resource.objects.create(name='Bread')
        self.beer = Resource.objects.create(name='Beer')

    def _create_universe_fixtures(self):
        self.universe = Universe.objects.create()

    def _create_population_fixtures(self):
        self.first_pop = Population.objects.create(universe=self.universe,
                                                   name='Farmers', quantity=10)
        self.second_pop = Population.objects.create(universe=self.universe,
                                                    name='Miners', quantity=20)

    def _create_supply_demand_fixtures(self):
        SupplyDemand.objects.create(population=self.first_pop,
                                    resource=self.milk, value=0.5)
        SupplyDemand.objects.create(population=self.first_pop,
                                    resource=self.bread, value=1.3)
        SupplyDemand.objects.create(population=self.second_pop,
                                    resource=self.bread, value=-0.6)
        SupplyDemand.objects.create(population=self.second_pop,
                                    resource=self.beer, value=2.5)
