from django.test import TestCase
from django.core.exceptions import ValidationError
from population.models import Population, Resource, SupplyDemand, Universe


class TestSupplyDemandModel(TestCase):

    def test_can_not_save_with_empty_population(self):
        resource_model = Resource.objects.create(name='Wool')

        with self.assertRaises(ValidationError):
            sd_model = SupplyDemand(resource=resource_model)
            sd_model.full_clean()

    def test_can_not_save_with_empty_resource(self):
        universe_model = Universe.objects.create()
        pop_model = Population.objects.create(
            name='Farmers', quantity=10, universe=universe_model)

        with self.assertRaises(ValidationError):
            sd_model = SupplyDemand(population=pop_model)
            sd_model.full_clean()

    def test_related_to_population(self):
        universe = Universe.create_new()
        population = Population.objects.create(universe=universe, name='bla',
                                               quantity=12)

        sd = SupplyDemand(population=population, value=1.3)
        self.assertEqual(sd.population, population)

    def test_related_to_resource(self):
        universe = Universe.create_new()
        population = Population.objects.create(universe=universe, name='bla',
                                               quantity=10)
        resource = Resource.objects.create(name='Weapons')

        sd = SupplyDemand(population=population, value=0.5, resource=resource)

        self.assertEqual(sd.resource, resource)

    def test_can_not_save_sd_with_no_pop(self):
        resource = Resource.objects.create(name='Wool')

        with self.assertRaises(ValidationError):
            sd = SupplyDemand(value=0.5, resource=resource)
            sd.full_clean()

    def test_can_not_save_sd_with_no_resource(self):
        universe = Universe.create_new()
        pop = Population.objects.create(name='Farmers', quantity=12,
                                        universe=universe)

        with self.assertRaises(ValidationError):
            sd = SupplyDemand(population=pop, value=2.3)
            sd.full_clean()

    def stest_can_not_save_sd_with_no_value(self):
        universe = Universe.create_new()
        pop = Population.objects.create(name='Farmers', quantity=12,
                                        universe=universe)
        resource = Resource.objects.create(name='Weapons')

        with self.assertRaises(ValidationError):
            sd = SupplyDemand(population=pop, resource=resource)
            sd.full_clean()
