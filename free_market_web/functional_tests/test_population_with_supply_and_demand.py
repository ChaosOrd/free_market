from .base import FunctionalTest
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from population.models import Resource


class CreatePopulationWithSupplyAndDemandTest(FunctionalTest):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Resource.objects.create(name='Milk')
        Resource.objects.create(name='Bread')

    def test_can_create_a_population_with_demand_and_get_see_it_later(self):
        # Yulia have decided to create a universe with populations
        # that actually have consumption and production

        self.browser.get(self.server_url)
        self.browser.find_element_by_link_text('New universe').click()

        # First she creates a population of people with "Food" demand
        name_tb = self.browser.find_element_by_id('id_name')
        name_tb.send_keys('People\n')
        qty_tb = self.browser.find_element_by_id('id_quantity')
        qty_tb.send_keys('20\n')

        # The consumption input controls are not seen yet
        self.assertRaises(NoSuchElementException,
                          self.browser.find_element_by_id,
                          'id_sd_0-resource')

        self.assertRaises(NoSuchElementException,
                          self.browser.find_element_by_id,
                          'id_sd_0-value')

        # She clicks on add demand item
        self.browser.find_element_by_link_text('Add supply/demand').click()

        # She chooses the conusmed resource and hits enter

        resource_cb = self.browser.find_element_by_id('id_sd_0-resource')
        resource_select = Select(resource_cb)
        resource_select.select_by_visible_text('Milk')
        resource_cb.send_keys('\n')

        # The supply/demand value input box became focused
        demand_val_tb = self.browser.find_element_by_id('id_sd_0-value')
        self.assertEqual(self.browser.switch_to.active_element, demand_val_tb)

        # She inserts the demand value
        demand_val_tb.send_keys('-4.5\n')

        # The second consumption controls are not seen yet
        self.assertRaises(NoSuchElementException,
                          self.browser.find_element_by_id,
                          'id_sd_1-resource')

        self.assertRaises(NoSuchElementException,
                          self.browser.find_element_by_id,
                          'id_sd_1-value')

        # She clicks on add consumption once again
        self.browser.find_element_by_link_text('Add supply/demand').click()

        # She enteres the name of other and hits enter
        resource_cb = self.browser.find_element_by_id('id_sd_1-resource')
        resource_select = Select(resource_cb)
        resource_select.select_by_visible_text('Bread')
        resource_cb.send_keys('\n')

        # The supply/demand value input box became focused
        supply_val_tb = self.browser.find_element_by_id('id_sd_1-value')
        self.assertEqual(self.browser.switch_to.active_element, supply_val_tb)

        # She inserts the supply
        supply_val_tb.send_keys('0.3\n')

        # She hits the save button
        self.browser.find_element_by_id('id_save').click()

        # She sees that the population was created with consumption
        # and production details she inserted
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('People', page_text)
        self.assertIn('20', page_text)
        self.assertIn('Milk', page_text)
        self.assertIn('-4.5', page_text)
        self.assertIn('Bread', page_text)
        self.assertIn('0.3', page_text)
