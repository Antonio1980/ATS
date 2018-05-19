from tests.base.browser import Browser
from tests.locators.home_page_locators import HomePageLocators
from tests.locators.login_page_locators import LogInPageLocators


class HomePage(Browser):
    @classmethod
    def logout(self, delay):
        self.driver_wait(delay)
        assert self.driver_wait_element_presented(delay + 1, HomePageLocators.HOME_PAGE_LOGO)
        self.search_and_click(delay + 10, HomePageLocators.SETTINGS_DROPDOWN)
        # time.sleep(10)
        self.search_and_click(delay + 5, HomePageLocators.LANGUAGE_ICON)
        self.search_and_click(delay + 3, HomePageLocators.LOGOUT_LINK)
        assert self.driver_wait_element_presented(delay + 1, LogInPageLocators.CRM_LOGO)
        self.driver_wait(delay)
