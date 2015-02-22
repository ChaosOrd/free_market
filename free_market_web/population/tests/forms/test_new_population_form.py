from django.test import TestCase
from population.forms import (NewPopulationForm, EMPTY_NAME_ERROR,
                              EMPTY_QUANTITY_ERROR, INVALID_QUANTITY_ERROR)
from unittest.mock import Mock, patch


class TestNewPopulationForm(TestCase):

    def setUp(self):
        self.universe_patcher = patch('population.forms.Universe')
        self.universe = self.universe_patcher.start()
        self.population_patcher = patch('population.forms.Population')
        self.population = self.population_patcher.start()

    def tearDown(self):
        self.universe_patcher.stop()
        self.population_patcher.stop()

    def test_save_creates_new_population_and_universe(self):
        new_pop_form = NewPopulationForm(data={'name': 'Farmers',
                                               'quantity': '100'})
        new_pop_form.is_valid()
        new_pop_form.save(sd_forms=[])

        self.population.create_new.assert_called_once_with(
            universe=self.universe.create_new.return_value,
            name='Farmers', quantity=100)

    def test_save_returns_new_universe_if_no_universe_passed(self):
        new_pop_form = NewPopulationForm(data={'name': 'Farmers',
                                               'quantity': '100'})
        new_pop_form.is_valid()
        self.assertEqual(new_pop_form.save(sd_forms=[]),
                         self.universe.create_new.return_value)

    def test_save_returns_existing_universe_if_universe_pased(self):
        universe_obj = self.universe.objects.get.return_value
        new_pop_form = NewPopulationForm(data={'name': 'Farmers',
                                               'quantity': '100'})
        new_pop_form.is_valid()
        returned_universe = new_pop_form.save(sd_forms=[], for_universe=1)

        self.universe.objects.get.assert_called_once_with(id=1)
        self.assertEqual(returned_universe, universe_obj)

    def test_save_saves_all_sd_forms(self):
        first_sd_form = Mock()
        second_sd_form = Mock()
        new_pop_form = NewPopulationForm(
            data={'name': 'Programmers', 'quantity': 5})
        new_pop_obj = self.population.create_new.return_value

        new_pop_form.is_valid()
        new_pop_form.save(sd_forms=[first_sd_form, second_sd_form],
                          for_universe=1)

        first_sd_form.save.assert_called_once_with(
            for_population=new_pop_obj)

    def test_form_validation_for_blank_name(self):
        new_pop_form = NewPopulationForm(data={'name': '',
                                               'quantity': 100})

        self.assertFalse(new_pop_form.is_valid())
        self.assertEqual(new_pop_form.errors['name'], [EMPTY_NAME_ERROR])

    def test_form_validation_for_blank_quantity(self):
        new_pop_form = NewPopulationForm(data={'name': 'Farmers',
                                               'quantity': ''})

        self.assertFalse(new_pop_form.is_valid())
        self.assertEqual(new_pop_form.errors['quantity'],
                         [EMPTY_QUANTITY_ERROR])

    def test_form_validation_for_not_numeric_quantity(self):
        new_pop_form = NewPopulationForm(data={'name': 'Farmers',
                                               'quantity': 'Many'})

        self.assertFalse(new_pop_form.is_valid())
        self.assertEqual(new_pop_form.errors['quantity'],
                         [INVALID_QUANTITY_ERROR])

    def test_form_validation_for_non_integer_quantity(self):
        new_pop_form = NewPopulationForm(data={'name': 'Farmers',
                                               'quantity': '4.5'})

        self.assertFalse(new_pop_form.is_valid())
        self.assertEqual(new_pop_form.errors['quantity'],
                         [INVALID_QUANTITY_ERROR])
