from django.contrib.auth.models import User


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

    def log_in(self, username, password):
        self._create_user(username, password)
        self.login_user(username, password)

    def _create_user(self, username, password):
        user = User.objects.create_user(username, password=password)
        user.save()

    def login_user(self, username, password):
        self.browser.get(self.server_url)
        self.browser.find_element_by_link_text('Log in').click()
        self.fill_username_tb(username)
        self.fill_password_tb(password)
        self.submit()

def requires_logged_in_user(func, username='DefaultUsername',
                 password='DefaultPassword'):

    def wrapper(self, *args, **kwargs):
        self.log_in(username, password)
        func(self, *args, **kwargs)

    return wrapper
