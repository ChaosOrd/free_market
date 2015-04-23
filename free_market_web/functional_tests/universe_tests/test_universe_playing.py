from ..base import FunctionalTest
from ..base_authentication import (AuthenticationTestMixin,
                                   requires_logged_in_user)
from django.contrib.auth.models import User
from population.models import Population, Resource, SupplyDemand, Universe


class UniversePlayingTest(FunctionalTest, AuthenticationTestMixin):

    def setUp(self):
        super().setUp()
        self.create_universe()
        self.create_resources()
        self.create_populations()
        self.create_supplies_and_demands()

    def create_universe(self):
        user = User.objects.create_user(username='sample_user',
                                        password='sample_pass')
        self.universe = Universe.objects.create(universe_name='Simple universe',
                                                owner=user)

    def create_resources(self):
        self.bread = Resource.objects.create(name='Bread')
        self.tools = Resource.objects.create(name='Tools')

    def create_populations(self):
        self.farmers = Population.objects.create(universe=self.universe,
                                                 name='Farmers', quantity=10)
        self.laborers = Population.objects.create(universe=self.universe,
                                                  name='Laborers', quantity=15)

    def create_supplies_and_demands(self):
        self.bread_demand = SupplyDemand.objects.create(population=self.laborers,
                                                        value=-1,
                                                        resource=self.bread,)
        self.bread_supply = SupplyDemand.objects.create(population=self.farmers,
                                                        value=1.5,
                                                        resource=self.bread)
        self.toos_demand = SupplyDemand.objects.create(population=self.farmers,
                                                       value=-2,
                                                       resource=self.tools)
        self.tools_supply = SupplyDemand.objects.create(population=self.laborers,
                                                        value=2,
                                                        resource=self.tools)

    @requires_logged_in_user(username='sample_user', password='sample_pass',
                             create_user=False)
    def test_simple_universe_playing(self):
        pass
