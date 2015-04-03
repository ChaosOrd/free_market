from .base_universe import UniverseTest


class PopCreationValidationErrorsTest(UniverseTest):

    def test_forms_validation(self):

        # Yulia decides to create a new population, bug forgets to give it
        # a name
        self.browser.get(self.server_url)
        self.browser.find_element_by_link_text('New universe').click()

        # She hits save without typing anything
        self.click_on_save()
        text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Universe name can not be empty', text)

        self.set_universe_name('Simple universe')
        self.set_population_quantity('50')
        self.click_on_save()

        # An error appeares indicating her failure
        text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Population name can not be empty', text)

        # The number she entered earlier still presents
        self.assert_pop_quantity_equals('50')

        # She gives it some name
        self.browser.find_element_by_id('id_name').send_keys('Loosers\n')

        # She clicks on save button and sees that the population is saved
        self.browser.find_element_by_id('id_save').click()

        text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Loosers', text)
        self.assertIn('50', text)

        # She decides to create one more, and now forgets to enter a quantity
        self.set_population_name('Rich people')

        self.click_on_save()

        # She sees another error
        text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Population quantity can not be empty', text)

        # The name she entered earlier still presents
        self.assert_pop_name_equals('Rich people')

        # She puts some nonsence instead of the number
        self.set_population_quantity('blablabla')

        self.browser.find_element_by_id('id_save').click()

        # The error text has changed
        text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Population quantity is invalid', text)

        # Finally she gets it right and enters a number
        self.set_population_quantity('3')

        self.click_on_save()

        # She sees her another population
        text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Loosers', text)
        self.assertIn('50', text)
        self.assertIn('Rich people', text)
        self.assertIn('3', text)
