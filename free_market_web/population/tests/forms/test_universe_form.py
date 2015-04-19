from django.test import TestCase
from population.forms import UniverseForm, EMPTY_UNIVERSE_NAME_ERROR
from unittest.mock import Mock, patch


class TestUniverseForm(TestCase):

    def setUp(self):
        self.universe_patcher = patch('population.forms.Universe')
        self.universe_cls = self.universe_patcher.start()
        self.owner = Mock()

    def tearDown(self):
        self.universe_patcher.stop()

    def test_empty_name_validation(self):
        form = UniverseForm(data={'univese_name': ''})

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['universe_name'],
                         [EMPTY_UNIVERSE_NAME_ERROR])

    def test_init_sets_owner_field(self):
        owner = Mock()

        form = UniverseForm(data={}, owner=owner)

        self.assertEqual(form.owner, owner)

    def test_validation_sets_owner_in_clean_data(self):
        owner = Mock()
        form = UniverseForm(data={}, owner=owner)

        form.is_valid()

        self.assertEqual(form.cleaned_data['owner'], owner)

    """
    def test_save_creates_universe_if_no_instance_provided_to_model(self):
        form = UniverseForm(data={'universe_name': 'My universe'})
        form.is_valid()

        form.save(owner=self.owner)

        self.universe_cls.objects.create.assert_called_once_with(
            universe_name='My universe', owner=self.owner)

    def test_save_updates_universe_if_instance_provided(self):
        universe_instance = Mock()
        form = UniverseForm(data={'universe_name': 'My universe'},
                            instance=universe_instance)
        form.is_valid()

        form.save(owner=self.owner)

        universe_instance.update.assert_called_once_with(
            universe_name='My universe', owner=self.owner)

    def test_save_returns_new_universe_model_if_instance_not_provided(self):
        form = UniverseForm(data={'universe_name': 'My universe'})
        form.is_valid()

        universe = form.save(owner=self.owner)

        self.assertEqual(universe, self.universe_cls.objects.create.return_value)
        """
