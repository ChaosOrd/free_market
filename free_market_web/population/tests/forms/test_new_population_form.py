from django.test import TestCase
from django.http import QueryDict
from population.forms import (NewPopulationForm, EMPTY_NAME_ERROR,
                              EMPTY_QUANTITY_ERROR, INVALID_QUANTITY_ERROR)
from unittest.mock import Mock, patch


class TestNewPopulationForm(TestCase):

    def setUp(self):
        self.population_patcher = patch('population.forms.Population')
        self.population = self.population_patcher.start()
        self.universe = Mock()
        self.sd_form_patcher = patch('population.forms.SupplyDemandForm')
        self.sd_form_cls = self.sd_form_patcher.start()
        self.first_sd_form_obj = Mock()
        self.first_sd_form_obj.is_valid.return_value = True
        self.second_sd_form_obj = Mock()
        self.second_sd_form_obj.is_valid.return_value = True
        self.sd_form_cls.side_effect = [self.first_sd_form_obj,
                                        self.second_sd_form_obj]
        self.post_data = QueryDict('').copy()

    def tearDown(self):
        self.population_patcher.stop()
        self.sd_form_patcher.stop()

    def test_save_creates_sd_forms_according_to_post_data(self):
        self.post_data.update(name='Farmers', quantity='100',
                              sd_prefix='sd_0')
        self.post_data.update(sd_prefix='sd_1')

        new_pop_form = NewPopulationForm(data=self.post_data)

        self.sd_form_cls.assert_any_call(prefix='sd_0', data=self.post_data)
        self.sd_form_cls.assert_any_call(prefix='sd_1', data=self.post_data)

    def test_can_be_created_with_no_arguments_passed_to_consturctor(self):
        new_pop_form = NewPopulationForm()

    def test_constructor_creates_a_list_of_sd_forms(self):
        self.post_data.update(name='Farmers', quantity='100', sd_prefix='sd_0')
        self.post_data.update(sd_prefix='sd_1')

        new_pop_form = NewPopulationForm(data=self.post_data)

        self.assertEqual(new_pop_form.sd_forms,
                         [self.first_sd_form_obj, self.second_sd_form_obj])

    def test_save_creates_new_population(self):
        self.post_data.update(name='Farmers', quantity='100')
        new_pop_form = NewPopulationForm(data=self.post_data)
        new_pop_form.is_valid()
        new_pop_form.save(for_universe=self.universe)

        self.population.create_new.assert_called_once_with(
            universe=self.universe,
            name='Farmers', quantity=100)

    def test_save_saves_all_sd_forms(self):
        self.post_data.update(name='Programmers', quantity='5', sd_prefix='sd_0')
        self.post_data.update(sd_prefix='sd_1')
        new_pop_form = NewPopulationForm(data=self.post_data)
        new_pop_obj = self.population.create_new.return_value

        new_pop_form.is_valid()
        new_pop_form.save(for_universe=1)

        self.first_sd_form_obj.save.assert_called_once_with(
            for_population=new_pop_obj)
        self.second_sd_form_obj.save.assert_called_once_with(
            for_population=new_pop_obj)

    def test_is_valid_returns_true_if_all_data_valid(self):
        self.post_data.update(name='Programmers', quantity='5', sd_prefix='sd_0')
        self.post_data.update(sd_prefix='sd_1')
        new_pop_form = NewPopulationForm(data=self.post_data)
        new_pop_obj = self.population.create_new.return_value

        self.assertTrue(new_pop_form.is_valid())

    def test_is_valid_returns_false_if_one_of_sd_forms_is_invalid(self):
        self.second_sd_form_obj.is_valid.return_value = False
        self.post_data.update(name='Programmers', quantity='5', sd_prefix='sd_0')
        self.post_data.update(sd_prefix='sd_1')
        new_pop_form = NewPopulationForm(data=self.post_data)
        new_pop_obj = self.population.create_new.return_value

        self.assertFalse(new_pop_form.is_valid())

    def test_form_validation_for_blank_name(self):
        self.post_data.update(name='', quantity='100')
        new_pop_form = NewPopulationForm(data=self.post_data)

        self.assertFalse(new_pop_form.is_valid())
        self.assertEqual(new_pop_form.errors['name'], [EMPTY_NAME_ERROR])

    def test_form_validation_for_blank_quantity(self):
        self.post_data.update(name='Farmers', quantity='')
        new_pop_form = NewPopulationForm(data=self.post_data)

        self.assertFalse(new_pop_form.is_valid())
        self.assertEqual(new_pop_form.errors['quantity'],
                         [EMPTY_QUANTITY_ERROR])

    def test_form_validation_for_not_numeric_quantity(self):
        self.post_data.update(name='Farmers', quantity='Many')
        new_pop_form = NewPopulationForm(data=self.post_data)

        self.assertFalse(new_pop_form.is_valid())
        self.assertEqual(new_pop_form.errors['quantity'],
                         [INVALID_QUANTITY_ERROR])

    def test_form_validation_for_non_integer_quantity(self):
        self.post_data.update(name='Farmers', quantity='4.5')
        new_pop_form = NewPopulationForm(data=self.post_data)

        self.assertFalse(new_pop_form.is_valid())
        self.assertEqual(new_pop_form.errors['quantity'],
                         [INVALID_QUANTITY_ERROR])
