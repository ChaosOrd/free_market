from ..base import FunctionalTest


class SignUpTest(FunctionalTest):

    def get_username_tb(self):
        return self.browser.find_element_by_id('id_username')

    def get_password1_tb(self):
        return self.browser.find_element_by_id('id_password1')

    def get_password2_tb(self):
        return self.browser.find_element_by_id('id_password2')

    def fill_username_tb(self, value):
        return self.get_username_tb().send_keys(value)

    def fill_password1_tb(self, value):
        self.get_password1_tb().send_keys(value)

    def fill_password2_tb(self, value):
        self.get_password2_tb().send_keys(value)

    def submit(self):
        self.browser.find_element_by_id('id_submit').click()

    def test_basic_account_creation_and_loggin_in(self):

        # Yulia have decided that she wants to create an account
        # She clicks on Sign up link
        self.browser.get(self.server_url)
        self.browser.find_element_by_link_text('Sign up').click()

        # She enters her email
        # self.browser.find_element_by_id('id_email').send_keys('yulia@gmail.com')

        # She enters the username she wants to use
        self.fill_username_tb('Yulia')

        # She enters the password she wants to use twice, but makes a typo
        self.fill_password1_tb('Bfc#hgoro')
        self.fill_password2_tb('Bfc#hgora')

        # She clicks on sign in link and sees an error message
        self.submit()

        self.assertIn("The two password fields didn't match.",
                      self.get_body_text())

        # Two passwords she previously entererd disappeared
        self.assertEquals(self.get_password1_tb().get_attribute('value'), '')
        self.assertEquals(self.get_password2_tb().get_attribute('value'), '')

        # But the user name remained
        self.assertEquals(self.get_username_tb().get_attribute('value'), 'Yulia')

        # She fills the passwords once again, this time right and clicks
        # the submit link
        self.fill_password1_tb('Bfc#hgoro')
        self.fill_password2_tb('Bfc#hgoro')
        self.submit()

        # She notices that the website now recognises her
        body_text = self.get_body_text()
        self.assertIn('You have signed up successfully. You can now proceed logging in.', body_text)

        # Yulia decides to check if the login was created
        # She clicks on log in link
        self.browser.find_element_by_link_text('Log in').click()

        # She enters her credentials and submits the form
        self.fill_username_tb('Yulia')
        self.browser.find_element_by_id('id_password').send_keys('Bfc#hgoro')
        self.submit()

        # She sees that she has successfully logged in
        body_text = self.get_body_text()
        self.assertIn('Yulia', body_text)
        self.assertIn('Log out', body_text)

        # She tries to log out next
        self.browser.find_element_by_link_text('Log out').click()

        # The log out operation was successful and the log in link is back
        body_text = self.get_body_text()
        self.assertIn('Log in', body_text)
        self.assertIn('Sign up', body_text)
