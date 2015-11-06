from typing import Iterable
from unittest import TestCase
from unittest.mock import MagicMock
from api.simulator_api import PopulationBase, SupplyDemandBase

__author__ = 'chaosord'


class PopulationImplementation(PopulationBase):
    def __init__(self, supplies_demands):
        self.__supplies_demands = supplies_demands

    @property
    def quantity(self) -> float:
        return 10

    @property
    def name(self) -> str:
        return 'SamplePopulation'

    @property
    def supplies_demands(self) -> Iterable[SupplyDemandBase]:
        return self.__supplies_demands


class TestPopulationBase(TestCase):

    def test_to_dict_returns_correct_data(self):
        first_sd = MagicMock()
        second_sd = MagicMock()
        supplies_demands = [first_sd, second_sd]

        population = PopulationImplementation(supplies_demands)

        result = population.to_dict()
        self.assertEquals(result, {'name': 'SamplePopulation', 'supplies_demands': [first_sd.to_dict.return_value,
                                                                                    second_sd.to_dict.return_value]})
