from django.test import TestCase
from population.forms import UniverseForm, EMPTY_UNIVERSE_NAME_ERROR
from unittest.mock import patch


class TestUniverseForm(TestCase):

    def setUp(self):
        self.universe_patcher = patch('population.forms.Universe')
        self.universe_cls = self.universe_patcher.start()

    def tearDown(self):
        self.universe_patcher.stop()

    def test_empty_name_validation(self):
        form = UniverseForm(data={'univese_name': ''})

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['universe_name'],
                         [EMPTY_UNIVERSE_NAME_ERROR])
