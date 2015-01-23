from .base import FunctionalTest


class CreateBasicPopulationTest(FunctionalTest):

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
        self.assert_element_does_not_exist('id_consumption_name_0')
        self.assert_element_does_not_exist('id_consumption_val_0')

        # She clicks on add demand item
        self.browser.find_element_by_link_text('Add consumption').click()

        # She enteres the name of the consumption and hits enter
        cons_name_tb = self.browser.find_element_by_id('id_consumption_name_0')
        cons_name_tb.send_keys('Milk\n')

        # The consumption value input box became focused
        cons_val_tb = self.browser.find_element_by_id('id_consumption_val_0')
        self.assertEqual(self.browser.switch_to.active_element, cons_val_tb)

        # She inserts the consumption value
        cons_val_tb.send_keys('4\n')

        # The second consumption controls are not seen yet
        cons_name_tb = self.browser.find_element_by_id('id_consumption_name_1')
        cons_val_tb = self.browser.find_element_by_name('id_consumption_val_1')
        self.assertIs(None, cons_name_tb)
        self.assertIs(None, cons_val_tb)

        # She clicks on add consumption once again
        self.browser.find_element_by_link_text('Add consumption').click()

        # She enteres the name of other and hits enter
        cons_name_tb = self.browser.find_element_by_id('id_consumption_name_1')
        cons_name_tb.send_keys('Bread\n')

        # The consumption value input box became focused
        cons_val_tb = self.browser.find_element_by_id('id_consumption_val_1')
        self.assertEqual(self.browser.switch_to.active_element, cons_val_tb)

        # She inserts the consumption value
        cons_val_tb.send_keys('10\n')

        # Next she decides to add a production

        # Before she clicked on add production, the inputs did not exist
        self.assert_element_does_not_exist('id_consumption_name_1')
        self.assert_element_does_not_exist('id_consumption_val_1')

        self.browser.find_element_by_link_text('Add production').click()

        # She wirtes the production details and hits save
        prod_name_tb = self.browser.find_element_by_id('id_production_name_0')
        prod_name_tb.send_keys('Wool\n')
        prod_val_tb = self.browser.find_element_by_id('id_production_name_0')
        prod_val_tb.send_keys('0.1\n')

        self.browser.find_element_by_id('id_save').click()

        self.fail('Continue the test')

        # She sees that the population was created with consumption
        # and production details she inserted
