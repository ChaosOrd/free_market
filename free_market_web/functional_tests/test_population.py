from .base import FunctionalTest


class PopulationTest(FunctionalTest):

    def test_can_create_a_population_and_get_see_it_later(self):
        # Yulia found out about a web site that simulates a free marked
        # and decided to try it out
        self.browser.get(self.server_url)

        # She sees the custom polulation link and decides to give it a try
        self.browser.find_element_by_link_text('Custom population').click()

        # She sees an input box with a default population name
        input_name_tb = self.browser.find_element_by_id('id_name')

        # The name text box is focused
        self.assertEqual(self.browser.switch_to_active_element(), input_name_tb)

        # She types a population name
        input_name_tb.send_keys('Farmers\n')

        # The next input box Yulia sees is the population quantity
        input_qty_tb = self.browser.find_element_by_id('id_quantity')
        self.assertEqual(input_qty_tb.text, '')

        # Since Yulia pressed enter in a previous element, now the quantity
        # text box is focused
        self.assertEqual(self.browser.switch_to_active_element(), input_qty_tb)

        # She types a small number and since she pressed enter in a previous
        input_qty_tb.send_keys('20')

        # Finally she presses the save link
        self.browser.find_element_by_id('id_save').click()

        # She sees the info of the population she previously created
        page_text = self.browser.find_element_by_tag_name('body')
        self.assertIn('Farmers', page_text)
        self.assertIn('20', page_text)

        self.fail('Continue the test. She needs to enter another population')
