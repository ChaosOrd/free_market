from django.http.request import HttpRequest
from django.test import TestCase
from unittest.mock import Mock, patch
from population.views import NewUniverseView


class TestNewUniverseView(TestCase):

    def setUp(self):
        self.request = HttpRequest()
        self.request.method = 'POST'
        self.create_class_mocks()
        self.create_instance_mocks()

    def create_class_mocks(self):
        self.universe_view = NewUniverseView()
        self.pop_form_patcher = patch('population.views.NewPopulationForm')
        self.pop_form_cls = self.pop_form_patcher.start()
        self.universe_patcher = patch('population.views.Universe')
        self.universe_cls = self.universe_patcher.start()
        self.sd_form_patcher = patch('population.views.SupplyDemandForm')
        self.sd_form_cls = self.sd_form_patcher.start()
        self.render_patcher = patch('population.views.render')
        self.render_mock = self.render_patcher.start()
        self.redirect_patcher = patch('population.views.redirect')
        self.redirect_mock = self.redirect_patcher.start()

    def create_instance_mocks(self):
        self.pop_form = self.pop_form_cls.return_value
        self.first_sd_form = Mock()
        self.second_sd_form = Mock()
        self.sd_form_cls.side_effect = [self.first_sd_form, self.second_sd_form]
        self.first_sd_post_data = Mock()
        self.second_sd_post_data = Mock()
        self.universe = self.universe_cls.objects.get.return_value

    def tearDown(self):
        self.tear_down_class_mocks()

    def tear_down_class_mocks(self):
        self.pop_form_patcher.stop()
        self.universe_patcher.stop()
        self.sd_form_patcher.stop()
        self.render_patcher.stop()
        self.redirect_patcher.stop()

    def test_get_request_renderes_universe_template(self):
        self.universe_view.get(self.request)

        self.render_mock.assert_called_once_with(
            self.request, 'new_universe.html', {'form': self.pop_form})

    def test_passes_POST_data_to_form(self):
        self.pop_form.is_valid.return_value = True

        self.universe_view.post(self.request)

        self.pop_form_cls.assert_called_once_with(data=self.request.POST)

    def test_passes_POST_data_to_sd_forms(self):
        self.request.POST['SupplyDemand'] = \
            [self.first_sd_post_data, self.second_sd_post_data]
        self.pop_form.is_valid.return_value = True
        self.first_sd_form.is_valid.return_value = True
        self.second_sd_form.is_valid.return_value = True

        self.universe_view.post(self.request)

        self.sd_form_cls.assert_called_with(data=self.request.POST)
        self.sd_form_cls.assert_called_with(data=self.request.POST)

    def test_saves_form_if_form_is_valid(self):
        self.pop_form.is_valid.return_value = True

        self.universe_view.post(self.request)

        self.pop_form.save.assert_called_once_with(for_universe=None,
                                                   sd_forms=[])

    def test_saves_pop_form_if_sd_forms_valid(self):
        self.request.POST['SupplyDemand'] = \
            [self.first_sd_post_data, self.second_sd_post_data]
        self.pop_form.is_valid.return_value = True
        self.first_sd_form.is_valid.return_value = True
        self.second_sd_form.is_valid.return_value = True

        self.universe_view.post(self.request)

        self.pop_form.save.assert_called_once_with(for_universe=None,
            sd_forms=[self.first_sd_form, self.second_sd_form])

    def test_redirects_to_form_save_return_value_if_form_valid(self):
        self.pop_form.is_valid.return_value = True

        self.universe_view.post(self.request)

        self.redirect_mock.assert_called_once_with(
            self.pop_form.save.return_value)

    def test_redirects_to_pop_form_if_sd_forms_valid(self):
        self.request.POST['SupplyDemand'] = \
            [self.first_sd_post_data, self.second_sd_post_data]
        self.pop_form.is_valid.return_value = True
        self.first_sd_form.is_valid.return_value = True
        self.second_sd_form.is_valid.return_value = True

        self.universe_view.post(self.request)

        self.redirect_mock.assert_called_once_with(
            self.pop_form.save.return_value)

    def test_does_not_save_if_form_is_not_valid(self):
        self.pop_form.is_valid.return_value = False

        self.universe_view.post(self.request)

        self.assertFalse(self.pop_form.save.called)

    def test_does_not_save_if_sd_form_is_not_valid(self):
        self.request.POST['SupplyDemand'] = \
            [self.first_sd_post_data, self.second_sd_post_data]
        self.pop_form.is_valid.return_value = True
        self.first_sd_form.is_valid.return_value = False
        self.second_sd_form.is_valid.return_value = True

        self.universe_view.post(self.request)

        self.assertFalse(self.pop_form.save.called)

    def test_passes_form_to_template_if_form_invalid(self):
        self.pop_form.is_valid.return_value = False

        self.universe_view.post(self.request)

        self.pop_form_cls.assert_called_once_with(data=self.request.POST)
        self.render_mock.assert_called_once_with(
            self.request, 'new_universe.html', {'form': self.pop_form})

    def test_passes_form_to_template_if_sd_form_invalid(self):
        self.request.POST['SupplyDemand'] = \
            [self.first_sd_post_data, self.second_sd_post_data]
        self.pop_form.is_valid.return_value = True
        self.first_sd_form.is_valid.return_value = False
        self.second_sd_form.is_valid.return_value = True

        self.universe_view.post(self.request)

        self.pop_form_cls.assert_called_once_with(data=self.request.POST)
        self.render_mock.assert_called_once_with(
            self.request, 'new_universe.html', {'form': self.pop_form})
