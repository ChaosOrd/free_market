from ..base import FunctionalTest
from ..base_authentication import (AuthenticationTestMixin,
                                   requires_logged_in_user)
from django.contrib.auth.models import User
from population.models import Population, Resource, SupplyDemand, Universe


class UniversePlayingTest(FunctionalTest, AuthenticationTestMixin):

    def setUp(self):
        super().setUp()
        create_universe()

    def create_universe(self):
        user = User.objects.create_user(username='sample_user',
                                        password='sample_pass')
        Universe.objects.create(universe_name='Simple universe',
                                owner=user)

    def test_simple_universe_playing(self):
        pass
