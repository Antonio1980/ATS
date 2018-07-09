from tests.tests_me_admin.locators.home_page_locators import HomePageLocators
from tests.tests_me_admin.locators.login_page_locators import LogInPageLocators
from tests.tests_me_admin.pages.base_page import BasePage


class HomePage(BasePage):
    def __init__(self):
        super(HomePage, self).__init__()
        self_url = "/xai"
        self.home_page_url = self.me_base_url + self_url

    def logout(self, driver, delay):
        try:
            assert self.get_cur_url(driver) == self.home_page_url
            self.wait_element_visible(driver, HomePageLocators.HOME_PAGE_LOGO, delay + 1)
            settings_dropdown = self.find_element(driver, HomePageLocators.SETTINGS_DROPDOWN)
            self.click_on_element(settings_dropdown)
            self.driver_wait(driver, delay + 3)
            logoff_button = self.find_element(driver, HomePageLocators.LOGOFF_BUTTON)
            self.click_on_element(logoff_button)
            self.driver_wait(driver, delay + 3)
            confirm_button = self.find_element(driver, HomePageLocators.LOGOFF_CONFIRM_BUTTON)
            self.click_on_element(confirm_button)
            self.driver_wait(driver, delay + 3)
        finally:
            if self.wait_element_visible(driver, LogInPageLocators.NASDAQ_LOGO, delay + 1):
                return True
            else:
                return False

