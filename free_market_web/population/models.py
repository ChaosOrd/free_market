from django.db import models


class Universe(models.Model):

    @staticmethod
    def create_new():
        return Universe.objects.create()


class Population(models.Model):

    universe = models.ForeignKey(Universe)
    name = models.TextField()
    quantity = models.IntegerField()

    @staticmethod
    def create_new(universe, name, quantity):
        new_pop = Population.objects.create(universe=universe, name=name,
                                            quantity=quantity)
        return new_pop
