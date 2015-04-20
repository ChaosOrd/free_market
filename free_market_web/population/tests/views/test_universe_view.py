from .base import BaseUniverseTestCase
from django.core.exceptions import PermissionDenied
from population.views import (BaseUniverseView, ExistingUniverseView,
                              NewUniverseView)
from unittest.mock import Mock


class TestBaseUniverseView(BaseUniverseTestCase):

    def setUp(self):
        super().setUp()
        self.universe_view.pop_form.is_valid.return_value = True
        self.universe_view.universe_form.is_valid.return_value = True

    def create_class_mocks(self):
        super().create_class_mocks()
        self.universe_view = BaseUniverseView()
        self.universe_view.pop_form = Mock()
        self.universe_view.universe_form = Mock()

    def test_save_forms_data_saves_population_if_forms_valid(self):
        universe = self.universe_view.universe_form.save.return_value

        self.universe_view.save_forms_data(self.request)

        self.universe_view.pop_form.save.assert_called_once_with(for_universe=universe)

    def test_save_forms_data_saves_universe_form_if_forms_valid(self):
        self.universe_view.save_forms_data(self.request)

        self.universe_view.universe_form.save.assert_called_once_with(commit=False)

    def test_save_forms_data_saves_universe_if_forms_valid(self):
        self.universe_view.save_forms_data(self.request)

        universe_form = self.universe_view.universe_form
        universe_form.save.return_value.save.assert_called_once_with()

    def test_save_forms_data_sets_universe_owner_if_forms_valid(self):
        self.universe_view.save_forms_data(self.request)
        universe_form = self.universe_view.universe_form
        saved_universe = universe_form.save.return_value

        self.assertEqual(saved_universe.owner, self.request.user)

    def test_save_forms_redirects_to_universe_value_if_forms_valid(self):
        self.universe_view.save_forms_data(self.request)

        self.redirect_mock.assert_called_once_with(
            self.universe_view.universe_form.save.return_value)

    def test_save_forms_redirects_to_universe_form_if_all_sd_forms_valid(self):
        self.universe_view.save_forms_data(self.request)

        self.redirect_mock.assert_called_once_with(
            self.universe_view.universe_form.save.return_value)

    def test_save_forms_does_not_save_if_pop_form_is_invalid(self):
        self.universe_view.pop_form.is_valid.return_value = False

        self.universe_view.save_forms_data(self.request)

        self.assertFalse(self.universe_view.pop_form.save.called)
        self.assertFalse(self.universe_view.universe_form.save.called)

    def test_save_forms_does_not_save_if_universe_form_is_invalid(self):
        self.universe_view.universe_form.is_valid.return_value = False

        self.universe_view.save_forms_data(self.request)

        self.assertFalse(self.pop_form.save.called)
        self.assertFalse(self.universe_view.universe_form.save.called)


class TestExistingUniverseView(BaseUniverseTestCase):

    def setUp(self):
        super().setUp()
        self.universe.owner = self.request.user

    def create_class_mocks(self):
        super().create_class_mocks()
        self.universe_view = ExistingUniverseView()

    def test_post_passes_POST_data_to_pop_form(self):
        self.universe_view.post(self.request, 1)

        self.pop_form_cls.assert_called_once_with(data=self.request.POST)

    def test_post_passes_data_to_universe_form(self):
        self.universe_view.post(self.request, 1)

        self.universe_form_cls.assert_called_once_with(data=self.request.POST,
                                                       instance=self.universe)

    def test_renderes_universe_template_if_form_invalid(self):
        self.pop_form.is_valid.return_value = False

        self.universe_view.post(self.request, 2)

        self.universe_cls.objects.get.assert_called_once_with(id=2)
        self.render_mock.assert_called_once_with(self.request, 'universe.html',
                                                 {'pop_form': self.pop_form,
                                                  'universe_form': self.universe_form})

    def test_post_raises_permission_denied_if_universe_owned_by_other(self):
        other_user = Mock()
        self.universe.owner = other_user

        with self.assertRaises(PermissionDenied):
            self.universe_view.post(self.request, 2)

    def test_get_request_renderes_universe_template(self):
        self.universe_view.get(self.request, 1)

        self.universe_cls.objects.get.assert_called_once_with(id=1)
        self.render_mock.assert_called_once_with(
            self.request, 'universe.html', {'pop_form': self.pop_form,
                                            'universe_form': self.universe_form})

    def test_get_request_retreives_universe_by_id(self):
        self.universe_view.get(self.request, 1)

        self.universe_cls.objects.get.assert_called_once_with(id=1)

    def test_get_request_creates_universe_form_with_instance_data(self):
        self.universe_view.get(self.request, 1)

        self.universe_form_cls.assert_called_once_with(instance=self.universe)

    def test_get_raises_permission_denied_if_not_owned_by_me(self):
        self.universe.owner = Mock()

        with self.assertRaises(PermissionDenied):
            self.universe_view.get(self.request, 1)

    def test_post_returns_save_forms_data_return_value(self):
        self.universe_view.save_forms_data = Mock()

        return_value = self.universe_view.post(self.request, 1)

        self.assertEqual(return_value, self.universe_view.save_forms_data.return_value)


class TestNewUniverseView(BaseUniverseTestCase):

    def create_class_mocks(self):
        super().create_class_mocks()
        self.universe_view = NewUniverseView()

    def test_post_renderes_universe_template_if_form_invalid(self):
        self.pop_form.is_valid.return_value = False

        self.universe_view.post(self.request)

        self.render_mock.assert_called_once_with(
            self.request, 'new_universe.html', {'pop_form': self.pop_form,
                                                'universe_form': self.universe_form})

    def test_get_creates_universe_form(self):
        self.universe_view.get(self.request)

        self.universe_form_cls.assert_called_once_with()

    def test_get_request_renderes_universe_template(self):
        self.universe_view.get(self.request)

        self.render_mock.assert_called_once_with(
            self.request, 'new_universe.html', {'pop_form': self.pop_form,
                                                'universe_form': self.universe_form})

    def test_post_passes_data_to_universe_form(self):
        self.universe_view.post(self.request)

        self.universe_form_cls.assert_called_once_with(data=self.request.POST)

    def test_post_returns_save_forms_data_return_value(self):
        self.universe_view.save_forms_data = Mock()

        return_value = self.universe_view.post(self.request)

        self.assertEqual(return_value, self.universe_view.save_forms_data.return_value)
