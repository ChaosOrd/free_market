from ..base import FunctionalTest
from population.models import Resource, Population, Universe, SupplyDemand


class CreatePopulationWithSupplyAndDemandTest(FunctionalTest):

    def setUp(self):
        super().setUp()
        self._create_resource_fixtures()
        self._create_universe_fixtures()
        self._create_population_fixtures()
        self._create_supply_demand_fixtures()

    def _create_resource_fixtures(self):
        self.milk = Resource.objects.create(name='Milk')
        self.bread = Resource.objects.create(name='Bread')
        self.beer = Resource.objects.create(name='Beer')
        self.vodka = Resource.objects.create(name='Vodka')

    def _create_universe_fixtures(self):
        self.universe = Universe.objects.create(id=0)

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
                                    resource=self.beer, value=-0.6)
        SupplyDemand.objects.create(population=self.second_pop,
                                    resource=self.vodka, value=2.5)

    def test_population_deletion(self):
        # Uncle Bob decides to check out the previously created universe
        universe_url = self.live_server_url + '/population/universe/0/'
        self.browser.get(universe_url)

        body = self.browser.find_element_by_tag_name('body').text

        # He sees the previously created first item
        self.assertIn('Farmers', body)
        self.assertIn('Milk', body)
        self.assertIn('0.5', body)
        self.assertIn('Bread', body)
        self.assertIn('1.3', body)

        # And the second item
        self.assertIn('Miners', body)
        self.assertIn('Beer', body)
        self.assertIn('0.6', body)
        self.assertIn('Vodka', body)
        self.assertIn('2.5', body)

        # There are 2 delete links, one for each population
        delete_links = self.browser.find_elements_by_link_text('Delete')
        self.assertEqual(len(delete_links), 2)

        # He decides to delete the first population
        delete_links[0].click()

        self.browser.refresh()
        body = self.browser.find_element_by_tag_name('body').text

        # The first item does not exist
        self.assertNotIn('Farmers', body)
        self.assertNotIn('Milk', body)
        self.assertNotIn('0.5', body)
        self.assertNotIn('Bread', body)
        self.assertNotIn('1.3', body)

        # But the second item still present
        self.assertIn('Miners', body)
        self.assertIn('Beer', body)
        self.assertIn('0.6', body)
        self.assertIn('Vodka', body)
        self.assertIn('2.5', body)
