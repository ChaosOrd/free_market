
from .base import FunctionalTest
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from population.models import Resource



class CreatePopulationWithSupplyAndDemandFormDeletion(FunctionalTest):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Resource.objects.create(name='Milk')
        Resource.objects.create(name='Bread')
