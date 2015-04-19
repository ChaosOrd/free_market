from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.db.utils import IntegrityError
from population.models import Universe


class TestUniverseModel(TestCase):

    def setUp(self):
        self.owner = User.objects.create_user(username='test_user')

    def test_can_create_universe(self):
        new_universe = Universe.objects.create(universe_name='Test',
                                               owner=self.owner)

        self.assertEqual(Universe.objects.count(), 1)
        self.assertEqual(Universe.objects.first(), new_universe)

    def test_can_not_save_universe_with_empty_name(self):
        with self.assertRaises(ValidationError):
            universe = Universe.objects.create(universe_name='',
                                               owner=self.owner)
            universe.full_clean()

    def test_can_not_save_universe_with_empty_owner(self):
        with self.assertRaises(IntegrityError):
            universe = Universe.objects.create(universe_name='My universe')
            universe.full_clean()

    def test_get_absolute_url(self):
        universe = Universe.objects.create(universe_name='My universe',
                                           owner=self.owner)

        self.assertEqual(universe.get_absolute_url(),
                         '/population/universe/%d/' % universe.id)
