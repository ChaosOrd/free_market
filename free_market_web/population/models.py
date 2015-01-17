from django.db import models


class Population(models.Model):
    name = models.TextField()
    quantity = models.IntegerField()

    def create_new(name, quantity):
        pass
