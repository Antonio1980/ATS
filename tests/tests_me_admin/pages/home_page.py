from selenium.common.exceptions import TimeoutException
from tests.tests_me_admin.pages.base_page import BasePage
from tests.tests_me_admin.locators import home_page_locators
from tests.tests_me_admin.locators import login_page_locators


class HomePage(BasePage):
    def __init__(self):
        super().__init__(self)
        self_url = "/xai"
        self.home_page_url = self.me_base_url + self_url
        self.locators = home_page_locators

    def logout(self, driver, delay):
        try:
            assert self.get_cur_url(driver) == self.home_page_url
            assert self.wait_element_visible(driver, self.locators.HOME_PAGE_LOGO, delay)
            settings_dropdown = self.find_element(driver, self.locators.SETTINGS_DROPDOWN)
            self.click_on_element(settings_dropdown)
            logoff_button = self.search_element(driver, self.locators.LOGOFF_BUTTON, delay)
            self.click_on_element(logoff_button)
            confirm_button = self.search_element(driver, self.locators.LOGOFF_CONFIRM_BUTTON, delay)
            self.click_on_element(confirm_button)
        finally:
            try:
                self.wait_element_visible(driver, login_page_locators.NASDAQ_LOGO, delay)
                return True
            except TimeoutException:
                return False

