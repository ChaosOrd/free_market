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
    name = models.TextField(verbose_name='name')
    quantity = models.IntegerField(verbose_name='quantity')

    @staticmethod
    def create_new(universe, name, quantity):
        new_pop = Population.objects.create(universe=universe, name=name,
                                            quantity=quantity)
        return new_pop


class Resource(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


class SupplyDemand(models.Model):
    population = models.ForeignKey(Population)
    resource = models.ForeignKey(Resource)
    value = models.FloatField()
