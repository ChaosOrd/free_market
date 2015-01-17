from django.db import models
from django.core.urlresolvers import reverse


class Universe(models.Model):

    @staticmethod
    def create_new():
        return Universe.objects.create()

    def get_absolute_url(self):
        return reverse('universe', args=[self.id])


class Population(models.Model):

    universe = models.ForeignKey(Universe)
    name = models.TextField()
    quantity = models.IntegerField()

    @staticmethod
    def create_new(universe, name, quantity):
        new_pop = Population.objects.create(universe=universe, name=name,
                                            quantity=quantity)
        return new_pop
