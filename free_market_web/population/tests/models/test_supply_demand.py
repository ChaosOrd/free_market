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
        self.fail()

    def test_related_to_resource(self):
        self.fail()
