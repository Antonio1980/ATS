from src.base.browser import Browser
from tests.crm.locators.home_page_locators import HomePageLocators
from tests.crm.locators.login_page_locators import LogInPageLocators


class HomePage(Browser):
    @classmethod
    def logout(self, delay):
        self.driver_wait(delay)
        assert self.wait_element_presented(delay + 1, HomePageLocators.HOME_PAGE_LOGO)
        self.click_on_element(delay + 10, HomePageLocators.SETTINGS_DROPDOWN)
        # time.sleep(10)
        self.click_on_element(delay + 5, HomePageLocators.LANGUAGE_ICON)
        self.click_on_element(delay + 3, HomePageLocators.LOGOUT_LINK)
        assert self.wait_element_presented(delay + 1, LogInPageLocators.CRM_LOGO)
        self.driver_wait(delay)
