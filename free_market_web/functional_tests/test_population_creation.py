from .base import FunctionalTest
from selenium import webdriver


class CreateBasicPopulationTest(FunctionalTest):

    def test_can_create_a_population_and_get_see_it_later(self):
        # Yulia found out about a web site that simulates a free marked
        # and decided to try it out
        self.browser.get(self.server_url)

        # She sees the custom new universe link and decides to give it a try
        self.browser.find_element_by_link_text('New universe').click()

        # She sees an input box with a default population name
        input_name_tb = self.browser.find_element_by_id('id_name')

        # The name text box is focused
        self.assertEqual(self.browser.switch_to.active_element, input_name_tb)

        # She types a population name
        input_name_tb.send_keys('Farmers\n')

        # The next input box Yulia sees is the population quantity
        input_qty_tb = self.browser.find_element_by_id('id_quantity')

        # Since Yulia pressed enter in a previous element, now the quantity
        # text box is focused
        self.assertEqual(self.browser.switch_to.active_element, input_qty_tb)

        # She types a small number and since she pressed enter in a previous
        input_qty_tb.send_keys('20')

        # Finally she presses the save link
        self.browser.find_element_by_id('id_save').click()

        # She sees the info of the population she previously created
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Farmers', page_text)
        self.assertIn('20', page_text)

        # The input form is still present so she decides to add another pop
        input_name_tb = self.browser.find_element_by_id('id_name')
        # The name textbox is focused
        self.assertEqual(self.browser.switch_to.active_element, input_name_tb)
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
