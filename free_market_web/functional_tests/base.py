from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
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
        self.assertRaises(NoSuchElementException,
                          self.browser.find_element_by_id,
                          element_id)

    def assert_element_exists(self, element_id):
        try:
            self.browser.find_element_by_id(element_id)
        except NoSuchElementException:
            self.fail('Element {} not found'.format(element_id))

    def select_listbox_item(self, listbox, item_name):
        listbox_select = Select(listbox)
        listbox_select.select_by_visible_text(item_name)


    def get_body_text(self):
        return self.browser.find_element_by_tag_name('body').text
