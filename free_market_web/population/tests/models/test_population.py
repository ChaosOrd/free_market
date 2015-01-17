from django.test import TestCase
from django.core.exceptions import ValidationError
from population.models import Population, Universe


class TestPopulationModel(TestCase):

    def test_create_new_creates_new_population(self):
        universe = Universe.create_new()
        population = Population.create_new(universe, 'Farmers', 10)

        self.assertEqual(Population.objects.count(), 1)
        new_pop = Population.objects.first()
        self.assertEqual(population, new_pop)

    def test_created_population_is_related_to_given_universe(self):
        universe = Universe.create_new()
        other_universe = Universe.create_new()
        Population.create_new(universe, 'Minvers', 13)

        new_pop = Population.objects.first()
        self.assertEqual(new_pop.universe, universe)

    def test_can_not_save_pop_with_empty_name(self):
        universe = Universe.create_new()

        with self.assertRaises(ValidationError):
            new_pop = Population.objects.create(universe=universe, name='',
                                                quantity=10)
            new_pop.full_clean()
