from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from population.models import Population, Universe


class TestPopulationModel(TestCase):
    def setUp(self):
        self.universe_owner = User.objects.create_user('sample_user')
        self.universe = Universe.objects.create(universe_name='sample',
                                                owner=self.universe_owner)

    def test_create_new_creates_new_population(self):
        population = Population.create_new(self.universe, 'Farmers', 10)

        self.assertEqual(Population.objects.count(), 1)
        new_pop = Population.objects.first()
        self.assertEqual(population, new_pop)

    def test_created_population_is_related_to_given_universe(self):
        Universe.objects.create(universe_name='other_universe',
                                owner=self.universe_owner)
        Population.create_new(self.universe, 'Minvers', 13)

        new_pop = Population.objects.first()
        self.assertEqual(new_pop.universe, self.universe)

    def test_can_not_save_pop_with_empty_name(self):
        with self.assertRaises(ValidationError):
            new_pop = Population.objects.create(universe=self.universe, name='',
                                                quantity=10)
            new_pop.full_clean()
