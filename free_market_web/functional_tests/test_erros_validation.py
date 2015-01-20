from .base import FunctionalTest


class PopCreationValidationErrorsTest(FunctionalTest):

    def test_forms_validation(self):

        # Yulia decides to create a new population, bug forgets to give it
        # a name
        self.browser.get(self.server_url)
        self.browser.find_element_by_link_text('New universe').click()
        input_qty_tb = self.browser.find_element_by_id('id_quantity')
        input_qty_tb.send_keys('50\n')
        save_btn = self.browser.find_element_by_id('id_save')
        save_btn.send_keys('\n')

        # An error appeares indicating her failure
        text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Population name can not be empty', text)

        # The number she entered earlier still presents
        qty_tb = self.browser.find_element_by_id('id_quantity')
        self.assertEqual(qty_tb.get_attribute('text'), '50')

        # She gives it some name
        self.browser.find_element_by_id('id_name').send_keys('Loosers\n')

        # She clicks on save button and sees that the population is saved
        self.browser.find_element_by_id('id_save').click()

        text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Loosers', text)
        self.assertIn('50', text)

        # She decides to create one more, and now forgets to enter a quantity
        name_tb = self.browser.find_element_by_id('id_name')
        name_tb.send_keys('Rich people\n')

        self.browser.find_element_by_id('id_save').click()

        # She sees another error
        text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Population quantity can not be empty', text)

        # She puts some nonsence instead of the number
        name_tb = self.browser.find_element_by_id('id_quantity')
        name_tb.send_keys('blablabla\n')
        self.browser.find_element_by_id('id_save').click()

        # The error text has changed
        text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Population quantity is invalid', text)

        # Finally she gets it right and enters a number
        qty_tb = self.browser.find_element_by_id('id_quantity')
        qty_tb.send_keys('3\n')

        self.browser.find_element_by_id('id_save').click()

        # She sees her another population
        text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Loosers', text)
        self.assertIn('50', text)
        self.assertIn('Rich people', text)
        self.assertIn('3', text)
