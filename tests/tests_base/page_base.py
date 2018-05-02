# !/usr/bin/env python
# -*- coding: utf8 -*-

from tests_resources.locators.login_page_locators import LOCATOR_1


class PageBase:
    def __init__(self, driver):
        self.driver = driver

    def go_to_home(self, home_url):
        self.driver.get(home_url)
        return self

    def go_to_page(self, url):
        self.driver.get(url)
        return self

    def run_search(self, url, query):
        self.driver.get(url)
        self.driver.find_element_by_id(LOCATOR_1['search_box']).send_keys(query)
        self.driver.find_element_by_id(LOCATOR_1['search_button']).click()

    def tear_down(self):
        self.driver.close()
