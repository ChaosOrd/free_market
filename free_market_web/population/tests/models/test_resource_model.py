from django.test import TestCase
from django.core.exceptions import ValidationError
from population.models import Population, Resource, Universe


class TestResourceModel(TestCase):

    def test_can_not_create_resource_with_empty_name(self):
        with self.assertRaises(ValidationError):
            resource_model = Resource.objects.create()
            resource_model.full_clean()
