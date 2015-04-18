from ..base import FunctionalTest


class PagesRequiringAuthenticatonTest(FunctionalTest):

    @property
    def login_url(self):
        return self.server_url + '/accounts/log_in/'

    def assert_page_redirects_to_login(self, page_route):
        page_url = self.server_url + page_route
        self.browser.get(page_url)

        self.assertEqual(self.browser.current_url,
                         '{}?next={}'.format(self.login_url, page_route))

    def test_pages_requiring_authentication(self):
        new_universe = '/population/new_universe/'
        self.assert_page_redirects_to_login(new_universe)

        my_universes = '/population/my_universes/'
        self.assert_page_redirects_to_login(my_universes)
