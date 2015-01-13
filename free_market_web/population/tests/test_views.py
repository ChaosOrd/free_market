from django.test import TestCase


class HomePageTest(TestCase):

    def test_home_page_renderes_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class CustomPopulationTest(TestCase):

    def test_custom_population_renders_custom_population(self):
        response = self.client.get('/custom_population/')
        self.assertTemplateUsed(response, 'custom_population.html')
