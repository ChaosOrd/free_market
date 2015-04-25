import unittest
from unittest import TestCase
from unittest.mock import Mock
from simulation.simulator import Person


class SimulatorTest(TestCase):

    def test_from_population_returns_list_of_persons(self):
        population = Mock()
        exchange = Mock()
        persons = Person.from_population(population, exchange)


if __name__ == '__main__':
    unittest.main()
