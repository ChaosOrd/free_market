class AuthenticationTestMixin(object):

    def get_username_tb(self):
        return self.browser.find_element_by_id('id_username')

    def get_password_tb(self):
        return self.browser.find_element_by_id('id_password')

    def get_password1_tb(self):
        return self.browser.find_element_by_id('id_password1')

    def get_password2_tb(self):
        return self.browser.find_element_by_id('id_password2')

    def fill_username_tb(self, value):
        self.get_username_tb().send_keys(value)

    def fill_password_tb(self, value):
        self.get_password_tb().send_keys(value)

    def fill_password1_tb(self, value):
        self.get_password1_tb().send_keys(value)

    def fill_password2_tb(self, value):
        self.get_password2_tb().send_keys(value)

    def submit(self):
        self.browser.find_element_by_id('id_submit').click()
