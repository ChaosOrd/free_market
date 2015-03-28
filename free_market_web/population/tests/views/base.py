from django.http.request import HttpRequest
from django.test import TestCase
from django.http import QueryDict
from unittest.mock import Mock, patch


class BaseUniverseTestCase(TestCase):

    def setUp(self):
        self.request = HttpRequest()
        self.create_class_mocks()
        self.create_instance_mocks()

    def create_class_mocks(self):
        self.pop_form_patcher = patch('population.views.NewPopulationForm')
        self.pop_form_cls = self.pop_form_patcher.start()
        self.universe_form_patcher = patch('population.views.UniverseForm')
        self.universe_form_cls = self.universe_form_patcher.start()
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
        self.universe_form = self.universe_form_cls.return_value
        self.first_sd_form = Mock()
        self.second_sd_form = Mock()
        self.sd_form_cls.side_effect = [self.first_sd_form, self.second_sd_form]
        self.sd_prefixes = ['sd_0', 'sd_1']
        self.post_with_prefixes = QueryDict('sd_prefix={}&sd_prefix={}'.format(
            self.sd_prefixes[0], self.sd_prefixes[1]))
        self.universe = self.universe_cls.objects.get.return_value

    def tearDown(self):
        self.tear_down_class_mocks()

    def tear_down_class_mocks(self):
        self.pop_form_patcher.stop()
        self.universe_form_patcher.stop()
        self.universe_patcher.stop()
        self.sd_form_patcher.stop()
        self.render_patcher.stop()
