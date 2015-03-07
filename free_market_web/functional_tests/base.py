from selenium import webdriver
from selenium.webdriver.support.ui import Select
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class FunctionalTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.server_url = cls.live_server_url

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        super().tearDown()
        self.browser.quit()

    def assert_element_does_not_exist(self, element_id):
        element = self.browser.find_element_by_name(element_id)
        self.assertIs(None, element)

    def select_listbox_item(self, listbox, item_name):
        listbox_select = Select(listbox)
        listbox_select.select_by_visible_text(item_name)

