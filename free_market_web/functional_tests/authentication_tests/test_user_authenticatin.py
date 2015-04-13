from ..base import FunctionalTest


class SignUpTest(FunctionalTest):

    def get_password1_tb(self):
        return self.browser.find_element_by_id('id_password1')

    def get_password2_tb(self):
        return self.browser.find_element_by_id('id_password2')

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

        ## She enters her email
        # self.browser.find_element_by_id('id_email').send_keys('yulia@gmail.com')

        # She enters the username she wants to use
        self.browser.find_element_by_id('id_username').send_keys('Yulia')

        # She enters the password she wants to use twice, but makes a typo
        self.fill_password1_tb('Bfc#hgoro')
        self.fill_password2_tb('Bfc#hgora')

        # She clicks on sign in link and sees an error message
        self.submit()

        self.assertIn("The two password fields didn't match.",
                      self.get_body_text())

        # Two passwords she previously entererd disappeared
        self.assertEquals(self.get_password1_tb().text, '')
        self.assertEquals(self.get_password2_tb().text, '')

        # She fills the passwords once again, this time right and clicks
        # the submit link
        self.browser.find_element_by_id('id_username').send_keys('Yulia')
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
        self.browser.find_element_by_id('id_username').send_keys('Yulia')
        self.browser.find_element_by_id('id_password').send_keys('Bfc#hgoro')
        self.submit()

        # She sees that she has successfully logged in
        body_text = self.get_body_text()
        self.assertIn('Yulia', body_text)
        self.assertIn('Sign out', body_text)
