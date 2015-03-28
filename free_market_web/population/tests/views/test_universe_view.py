from .base import BaseUniverseTestCase
from population.views import (BaseUniverseView, ExistingUniverseView,
                              NewUniverseView)


class TestBaseUniverseView(BaseUniverseTestCase):

    def create_class_mocks(self):
        super().create_class_mocks()
        self.universe_view = BaseUniverseView()

    def test_post_passes_POST_data_to_pop_form(self):
        self.universe_view.post(self.request, 1)

        self.pop_form_cls.assert_called_once_with(data=self.request.POST)

    def test_post_passes_POST_data_to_universe_form(self):
        self.universe_view.post(self.request)

        self.universe_form_cls.assert_called_once_with(data=self.request.POST)

    def test_saves_population_if_forms_valid(self):
        self.pop_form.is_valid.return_value = True
        self.universe_form.is_valid.return_value = True

        self.universe_view.post(self.request, 1)

        self.pop_form.save.assert_called_once_with(for_universe=1)

    def test_saves_universe_if_forms_valid(self):
        self.pop_form.is_valid.return_value = True
        self.universe_form.is_valid.return_value = True

        self.universe_view.post(self.request, 1)

        self.universe_form.save.assert_called_once_with()

    def test_redirects_to_form_return_value_if_forms_valid(self):
        self.pop_form.is_valid.return_value = True
        self.universe_form.is_valid.return_value = True

        self.universe_view.post(self.request, 1)

        self.redirect_mock.assert_called_once_with(
            self.pop_form.save.return_value)

    def test_redirects_to_pop_form_if_all_sd_forms_valid(self):
        self.pop_form.is_valid.return_value = True
        self.universe_form.is_valid.return_value = True
        self.first_sd_form.is_valid.return_value = True
        self.second_sd_form.is_valid.return_value = True

        self.universe_view.post(self.request, 1)

        self.redirect_mock.assert_called_once_with(
            self.pop_form.save.return_value)

    def test_does_not_save_if_pop_form_is_invalid(self):
        self.pop_form.is_valid.return_value = False

        self.universe_view.post(self.request, 1)

        self.assertFalse(self.pop_form.save.called)

    def test_does_not_save_if_universe_form_is_invalid(self):
        self.universe_form.is_valid.return_value = False

        self.universe_view.post(self.request)

        self.assertFalse(self.pop_form.save.called)

    def test_passes_form_to_template_if_form_invalid(self):
        self.pop_form.is_valid.return_value = False

        self.universe_view.post(self.request, 2)

        self.pop_form_cls.assert_called_once_with(data=self.request.POST)

    def test_passes_form_to_template_if_sd_form_invalid(self):
        self.request.POST = self.post_with_prefixes
        self.pop_form.is_valid.return_value = True
        self.first_sd_form.is_valid.return_value = True
        self.second_sd_form.is_valid.return_value = False

        self.universe_view.post(self.request, 2)

        self.pop_form_cls.assert_called_once_with(data=self.request.POST)


class TestExistingUniverseView(BaseUniverseTestCase):

    def create_class_mocks(self):
        super().create_class_mocks()
        self.universe_view = ExistingUniverseView()

    def test_renderes_universe_template_if_form_invalid(self):
        self.pop_form.is_valid.return_value = False

        self.universe_view.post(self.request, 2)

        self.universe_cls.objects.get.assert_called_once_with(id=2)
        self.render_mock.assert_called_once_with(self.request, 'universe.html',
                                                 {'form': self.pop_form,
                                                  'universe': self.universe})

    def test_get_request_renderes_universe_template(self):
        self.universe_view.get(self.request, 1)

        self.universe_cls.objects.get.assert_called_once_with(id=1)
        self.render_mock.assert_called_once_with(
            self.request, 'universe.html', {'universe': self.universe,
                                            'form': self.pop_form})


class TestNewUniverseView(BaseUniverseTestCase):

    def create_class_mocks(self):
        super().create_class_mocks()
        self.universe_view = NewUniverseView()

    def test_renderes_universe_template_if_form_invalid(self):
        self.pop_form.is_valid.return_value = False

        self.universe_view.post(self.request, 2)

        self.universe_cls.objects.get.assert_called_once_with(id=2)
        self.render_mock.assert_called_once_with(
            self.request, 'new_universe.html', {'form': self.pop_form,
                                                'universe': self.universe})

    def test_get_request_renderes_universe_template(self):
        self.universe_view.get(self.request, 1)

        self.universe_cls.objects.get.assert_called_once_with(id=1)
        self.render_mock.assert_called_once_with(
            self.request, 'new_universe.html', {'universe': self.universe,
                                                'form': self.pop_form})
