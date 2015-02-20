from django.test import TestCase
from population.forms import (NewPopulationForm, EMPTY_NAME_ERROR,
                              EMPTY_QUANTITY_ERROR, INVALID_QUANTITY_ERROR)
from unittest.mock import patch


class TestSupplyDemandForm(TestCase):

    def test_save_creates_a_supply_and_demand(self):
        pass
