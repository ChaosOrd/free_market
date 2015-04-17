from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .base_authentication import AuthenticationTestMixin
from ..base import FunctionalTest
from ..universe_tests.base_universe import UniverseTestMixin

USERNAME1 = 'Yulia'
PASSWORD1 = 'sample_pass'

USERNAME2 = 'Pavel'
PASSWORD2 = 'sample_pass2'


class MyUniversesTest(FunctionalTest, AuthenticationTestMixin, UniverseTestMixin):

    def setUp(self):
        super().setUp()
        yulia = User.objects.create_user(username=USERNAME1, password=PASSWORD1)
        yulia.save()

        pavel = User.objects.create_user(username=USERNAME2, password=PASSWORD2)
        pavel.save()

    def test_authenticated_user_sees_his_universes(self):
        # Yulia has found the option to see the universes
        # she has created earlier

        self.browser.get(self.server_url)

        # She loggs in
        self.browser.find_element_by_link_text('Log in').click()
        self.fill_username_tb(USERNAME1)
        self.fill_password_tb(PASSWORD1)
        self.submit()

        # She creates a universe
        self.set_universe_name('Test universe')
        self.set_population_name('Farmers')
        self.set_population_quantity('10')
        self.browser.find_element_by_id('id_save').click()

        # She goes back to home page
        self.browser.get(self.server_url)

        self.browser.find_element_by_link_text('My universes').click()

        body_text = self.get_body_text()

        # She sees the univeres she has created before and clicks on it
        self.browser.find_element_by_link_text('Test universe').click()

        # She sees the universe she created before
        body_text = self.get_body_text()
        self.assertIn('Farmers', body_text)
        self.assertIn('10', body_text)

        # Yulia logs out
        self.browser.find_element_by_link_text('Log out').click()

        # And Pavel logs in
        self.browser.find_element_by_link_text('Log in').click()
        self.fill_username_tb(USERNAME2)
        self.fill_password_tb(PASSWORD2)
        self.submit()

        # Pavel creates own universe
        self.set_universe_name("Pavel's universe")
        self.set_population_name('Munchkins')
        self.set_population_quantity('14')
        self.browser.find_element_by_id('id_save').click()

        # He goes back to home page and creates another universe
        self.set_universe_name("Finite supply universe")
        self.set_population_name('Laborers')
        self.set_population_quantity('112')
        self.browser.find_element_by_id('id_save').click()

        # He goes back to the main meny and checks his universes
        self.browser.find_element_by_id('My universes').click()

        # He sees the universes he has created
        body_text = self.get_body_text()
        self.assertIn("Pavel's universe", body_text)
        self.assertIn('Finite supply universe', body_text)

        # But not the universes of previous user
        self.assertNotIn('Farmers', body_text)
        self.assertNotIn('10', body_text)

        # He clicks on one of his universes
        self.browser.find_element_by_link_text('Finite supply universe').click()
        body_text = self.get_body_text()

        # He sees the details of the universe he has created before
        self.assertIn('Laborers', body_text)
        self.assertIn('112', body_text)
