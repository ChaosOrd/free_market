from django.test import TestCase
from population.models import Universe


class TestUniverseModel(TestCase):

    def test_can_create_universe(self):
        new_universe = Universe.objects.create()
        self.assertEqual(Universe.objects.count(), 1)
        self.assertEqual(Universe.objects.first(), new_universe)

    def test_get_absolute_url(self):
        universe = Universe.objects.create()
        self.assertEqual(universe.get_absolute_url(),
                         '/population/universe/%d/' % universe.id)
