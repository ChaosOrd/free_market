from django.test import TestCase
from population.forms import (NewPopulationForm, EMPTY_NAME_ERROR,
                              EMPTY_QUANTITY_ERROR, INVALID_QUANTITY_ERROR)
from unittest.mock import patch


class TestNewItemForm(TestCase):

    @patch('population.forms.Universe')
    @patch('population.forms.Population')
    def test_save_creates_new_population_and_universe(self, population, universe):
        new_pop_form = NewPopulationForm(data={'name': 'Farmers',
                                               'quantity': '100'})
        new_pop_form.is_valid()
        new_pop_form.save()

        population.create_new.assert_called_once_with(
            universe=universe.create_new.return_value,
            name='Farmers', quantity=100)

    @patch('population.forms.Universe')
    @patch('population.forms.Population')
    def test_save_returns_new_universe(self, population, universe):
        new_pop_form = NewPopulationForm(data={'name': 'Farmers',
                                               'quantity': '100'})
        new_pop_form.is_valid()
        self.assertEqual(new_pop_form.save(), universe.create_new.return_value)

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
