from .base_universe import UniverseTestMixin
from ..base import FunctionalTest
from population.models import Resource


class CreatePopulationWithSupplyAndDemandTest(FunctionalTest, UniverseTestMixin):

    def setUp(self):
        super().setUp()
        Resource.objects.create(name='Milk')
        Resource.objects.create(name='Bread')
        Resource.objects.create(name='Beer')

    def select_sd_resource_name(self, name, sd_idx):
        resource_cb = self.get_sd_resource_widget(sd_index=sd_idx)
        self.select_listbox_item(resource_cb, name)

    def set_sd_value(self, value, sd_idx):
        sd_value_tb = self.get_sd_value_widget(sd_idx)
        sd_value_tb.clear()
        sd_value_tb.send_keys(value)

    def get_sd_resource_widget(self, sd_index):
        resource_element_id = self.get_sd_resource_id(sd_index)
        return self.browser.find_element_by_id(resource_element_id)

    def get_sd_value_widget(self, sd_index):
        value_element_id = self.get_sd_value_id(sd_index)
        return self.browser.find_element_by_id(value_element_id)

    def get_sd_resource_id(self, sd_index):
        return'id_sd_{}-resource'.format(sd_index)

    def get_sd_value_id(self, sd_index):
        return 'id_sd_{}-value'.format(sd_index)

    def test_can_create_a_population_with_demand_and_get_see_it_later(self):
        # Yulia have decided to create a universe with populations
        # that actually have consumption and production

        self.browser.get(self.server_url)
        self.browser.find_element_by_link_text('New universe').click()

        self.set_universe_name('Simple universe')

        # First she creates a population of people with "Food" demand
        self.set_population_name('People')
        self.set_population_quantity('20')

        # The supply demand input controls are not seen yet
        self.assert_element_does_not_exist(self.get_sd_value_id(0))
        self.assert_element_does_not_exist(self.get_sd_resource_id(0))

        # She clicks on add demand item
        self.browser.find_element_by_link_text('Add supply/demand').click()

        # She chooses the conusmed resource
        self.select_sd_resource_name('Milk', 0)

        # She inserts the demand value
        self.set_sd_value('-4.5', 0)

        # The second supply demand controls are not seen yet
        self.assert_element_does_not_exist(self.get_sd_resource_id(1))
        self.assert_element_does_not_exist(self.get_sd_value_id(1))

        # She clicks on add consumption once again
        self.browser.find_element_by_link_text('Add supply/demand').click()

        # She sees that there are new form fields are added
        self.assert_element_exists(self.get_sd_resource_id(1))
        self.assert_element_exists(self.get_sd_value_id(1))

        # She notices that there is a remove option and decides to give
        # it a try
        self.browser.find_element_by_id('id_sd_1-remove').click()

        # The input controls dissapeared
        self.assert_element_does_not_exist(self.get_sd_resource_id(1))
        self.assert_element_does_not_exist(self.get_sd_value_id(1))

        # She clicks on the "Add supply/demand" once again
        self.browser.find_element_by_link_text('Add supply/demand').click()

        # She enteres the name of other and hits enter
        self.select_sd_resource_name('Bread', 2)

        # She inserts the supply
        self.set_sd_value('0.3', 2)

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

    def test_form_validation_with_supply_and_demand(self):

        # Uncle Bob wants to create a new universe
        self.browser.get(self.server_url)
        self.browser.find_element_by_link_text('New universe').click()

        self.set_universe_name('Simple universe')

        # He types the population details
        self.set_population_name('Clean coders')
        self.set_population_quantity('6')

        # He decides to add it a supply but forgets to choose a resource
        self.browser.find_element_by_link_text('Add supply/demand').click()
        self.set_sd_value('0.4', 0)
        self.browser.find_element_by_id('id_save').click()

        # He sees an informative error message
        text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Supply/Demand resource can not be empty', text)

        # Uncle Bob selects the missing resource and clicks save
        resource_cb = self.get_sd_resource_widget(0)
        self.select_listbox_item(resource_cb, 'Bread')
        self.browser.find_element_by_id('id_save').click()

        # The population was successfully added
        text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Clean coders', text)
        self.assertIn('6', text)
        self.assertIn('Bread', text)
        self.assertIn('0.4', text)

        # He decides to add another population

        # He types the population details
        self.set_population_name('Code monkeys')
        self.set_population_quantity('3')

        # He decides to add it a supply but forgets to insert a value
        self.browser.find_element_by_link_text('Add supply/demand').click()
        self.select_sd_resource_name('Beer', 0)
        self.browser.find_element_by_id('id_save').click()

        # He sees another error message
        text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Supply/Demand value can not be empty', text)

        # He enters some junk and hits save
        self.set_sd_value('zero seven', 0)
        self.browser.find_element_by_id('id_save').click()

        # The error message has changed
        text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Supply/Demand value is invalid', text)

        # He rewrites value and hits save
        self.set_sd_value('0.7', 0)
        self.browser.find_element_by_id('id_save').click()

        # He sees the new population along with the old population data
        text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Clean coders', text)
        self.assertIn('3', text)
        self.assertIn('Bread', text)
        self.assertIn('0.4', text)
        self.assertIn('Code monkeys', text)
        self.assertIn('6', text)
        self.assertIn('Bread', text)
        self.assertIn('0.7', text)
