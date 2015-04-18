UNIVERSE_TB_ID = 'id_universe_name'
POP_NAME_ID = 'id_name'
POP_QTY_ID = 'id_quantity'
SAVE_ID = 'id_save'


class UniverseTestMixin(object):

    def set_universe_name(self, universe_name):
        universe_name_tb = self._get_universe_name_tb()
        universe_name_tb.clear()
        universe_name_tb.send_keys(universe_name)

    def clear_universe_name(self):
        universe_name_tb = self._get_universe_name_tb()
        universe_name_tb.clear()

    def set_population_name(self, population_name):
        input_name_tb = self.browser.find_element_by_id(POP_NAME_ID)
        input_name_tb.clear()
        input_name_tb.send_keys(population_name)

    def set_population_quantity(self, qty):
        input_qty_tb = self.browser.find_element_by_id(POP_QTY_ID)
        input_qty_tb.clear()
        input_qty_tb.send_keys(qty)

    def assert_universe_name_equals(self, uninverse_name):
        universe_name_tb = self.browser.find_element_by_id(UNIVERSE_TB_ID)
        self.assertEqual(universe_name_tb.get_attribute('value'), uninverse_name)

    def assert_pop_quantity_equals(self, pop_quantity):
        quantity_tb = self.browser.find_element_by_id(POP_QTY_ID)
        self.assertEqual(quantity_tb.get_attribute('value'), pop_quantity)

    def assert_pop_name_equals(self, pop_name):
        pop_name_tb = self.browser.find_element_by_id(POP_NAME_ID)
        self.assertEqual(pop_name_tb.get_attribute('value'), pop_name)

    def click_on_save(self):
        self.browser.find_element_by_id(SAVE_ID).click()

    def click_on_new_universe(self):
        self.browser.find_element_by_link_text('New universe').click()

    def _get_universe_name_tb(self):
        return self.browser.find_element_by_id(UNIVERSE_TB_ID)
