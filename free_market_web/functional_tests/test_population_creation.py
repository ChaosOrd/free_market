from .base import FunctionalTest
from selenium import webdriver


class CreateBasicPopulationTest(FunctionalTest):

    def _set_universe_name(self, universe_name):
        universe_name_tb = self.browser.find_element_by_id('id_universe_name')
        universe_name_tb.send_keys(universe_name)

    def _set_population_name(self, population_name):
        input_name_tb = self.browser.find_element_by_id('id_name')
        input_name_tb.send_keys(population_name)

    def _set_population_quantity(self, qty):
        input_qty_tb = self.browser.find_element_by_id('id_quantity')
        input_qty_tb.send_keys(qty)

    def test_can_create_a_population_and_get_see_it_later(self):
        # Yulia found out about a web site that simulates a free marked
        # and decided to try it out
        self.browser.get(self.server_url)

        # She sees the custom new universe link and decides to give it a try
        self.browser.find_element_by_link_text('New universe').click()

        self._set_universe_name('Simple universe')

        # She types a population name
        self._set_population_name('Farmers')

        # Then she inserts a quantity
        self._set_population_quantity('20')

        # Finally she presses the save link
        self.browser.find_element_by_id('id_save').click()

        # She sees the info of the population she previously created
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Farmers', page_text)
        self.assertIn('20', page_text)

        # The input box with the universe name still presents but it is alredy
        # filled with the name she previously gave
        universe_name_tb = self.browser.find_element_by_id('id_universe_name')
        self.assertEqual(universe_name_tb.get_attribute('value'),
                         'Simple universe')

        # The name textbox is focused
        self.assertEqual(self.browser.switch_to.active_element,
                         universe_name_tb)

        # She changes the universe name
        universe_name_tb.clear()
        universe_name_tb.send_keys('Complicated universe')

        # She decides to add another pop
        input_name_tb = self.browser.find_element_by_id('id_name')

        input_name_tb.send_keys('Miners\n')
        input_qty_tb = self.browser.find_element_by_id('id_quantity')

        # The next text box is still automatically being focused after sher
        # pressed enter key. She types the population quantity
        self.assertEqual(self.browser.switch_to.active_element, input_qty_tb)
        input_qty_tb.send_keys('50\n')

        # The save button is still there and it is focused
        save_btn = self.browser.find_element_by_id('id_save')
        self.assertEqual(self.browser.switch_to.active_element, save_btn)
        save_btn.send_keys('\n')

        # The first population is still there along with the second
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Farmers', page_text)
        self.assertIn('20', page_text)
        self.assertIn('Miners', page_text)
        self.assertIn('50', page_text)

        # The universe name text box now contains the updated name
        universe_name_tb = self.browser.find_element_by_id('id_universe_name')
        self.assertEqual(universe_name_tb.get_attribute('value'),
                         'Complicated universe')

        # She closes the browser
        self.browser.close()
        self.browser = webdriver.Firefox()

        # Pavel enters the site and creates his population'
        self.browser.get(self.server_url)
        self.browser.find_element_by_link_text('New universe').click()
        self.browser.find_element_by_id('id_name').send_keys('Smart guys\n')
        self.browser.find_element_by_id('id_quantity').send_keys('4')
        self.browser.find_element_by_id('id_save').click()

        # He sees the population he created and does not sees Yulia's
        # populations
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Smart guys', page_text)
        self.assertIn('4', page_text)
        self.assertNotIn('Farmers', page_text)
        self.assertNotIn('Miners', page_text)
