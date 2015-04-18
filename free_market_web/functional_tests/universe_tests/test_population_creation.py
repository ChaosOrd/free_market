from ..base import FunctionalTest
from .base_universe import UniverseTestMixin
from ..base_authentication import (AuthenticationTestMixin, requires_logged_in_user)
from selenium import webdriver

from django.contrib.auth.models import User
from django.test import Client

class CreateBasicPopulationTest(FunctionalTest, UniverseTestMixin,
                                AuthenticationTestMixin):

    @requires_logged_in_user
    def test_can_create_a_population_and_get_see_it_later(self):
        # Yulia found out about a web site that simulates a free marked
        # and decided to try it out
        self.browser.get(self.server_url)

        # She sees the custom new universe link and decides to give it a try
        self.browser.find_element_by_link_text('New universe').click()

        self.set_universe_name('Simple universe')

        # She types a population name
        self.set_population_name('Farmers')

        # Then she inserts a quantity
        self.set_population_quantity('20')

        # Finally she presses the save link
        self.browser.find_element_by_id('id_save').click()

        # She sees the info of the population she previously created
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Farmers', page_text)
        self.assertIn('20', page_text)

        # The input box with the universe name still presents but it is alredy
        # filled with the name she previously gave
        self.assert_universe_name_equals('Simple universe')

        # She changes the universe name
        self.set_universe_name('Complicated universe')

        # She decides to add another pop
        self.set_population_name('Miners')
        self.set_population_quantity('50')

        self.browser.find_element_by_id('id_save').click()

        # The first population is still there along with the second
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Farmers', page_text)
        self.assertIn('20', page_text)
        self.assertIn('Miners', page_text)
        self.assertIn('50', page_text)

        # The universe name text box now contains the updated name
        self.assert_universe_name_equals('Complicated universe')

        # Pavel enters the site and creates his population'
        self.browser.get(self.server_url)
        self.browser.find_element_by_link_text('New universe').click()
        self.set_universe_name('My universe')
        self.set_population_name('Smart guys')
        self.set_population_quantity('4')
        self.browser.find_element_by_id('id_save').click()

        # He sees the population he created and does not sees Yulia's
        # populations
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assert_universe_name_equals('My universe')
        self.assertIn('Smart guys', page_text)
        self.assertIn('4', page_text)
        self.assertNotIn('Farmers', page_text)
        self.assertNotIn('Miners', page_text)
