from tests.tests_crm_bo.pages.base_page import BasePage
from tests.tests_crm_bo.locators.home_page_locators import HomePageLocators
from tests.tests_crm_bo.locators.customer_page_locators import CustomerPageLocators
from tests.tests_crm_bo.pages import home_page_url, user_management_page_url, customer_admin_url


class HomePage(BasePage):
    def __init__(self):
        super(HomePage, self).__init__()
        self.locators = HomePageLocators()

    def logout(self, driver, delay):
        try:
            assert self.find_element_by(driver, self.locators.HOME_PAGE_LOGO_ID, "id")
            self.click_on_element_by_locator(driver, self.locators.SETTINGS_DROPDOWN, delay + 5)
            self.click_on_element_by_locator(driver, self.locators.LANGUAGE_ICON, delay + 5)
            self.click_on_element_by_locator(driver, self.locators.LOGOUT_LINK, delay + 3)
        finally:
            if self.wait_element_presented(driver, self.base_locators.CRM_LOGO, delay + 1):
                return True
            else:
                return False

    def choose_customer_by_option(self, driver, customer, option):
        delay = 5
        customer_option = None
        try:
            assert self.get_cur_url(driver) == home_page_url
            customer_field = self.find_element(driver, self.locators.CUSTOMER_DROPDOWN)
            self.click_on_element(customer_field)
            if option == 1:
                customer_option = self.find_element(driver, self.locators.CUSTOMER_ID_OPTION)
            elif option == 2:
                customer_option = self.find_element(driver, self.locators.CUSTOMER_ID_OPTION)
            elif option == 3:
                customer_option = self.find_element(driver, self.locators.CUSTOMER_ID_OPTION)
            if customer_option is not None:
                self.click_on_element(customer_option)
            customer_name_field = self.find_element_by(driver, self.locators.CUSTOMER_NAME_FIELD_ID, "id")
            self.click_on_element(customer_field)
            self.send_keys(customer_name_field, customer)
            show_button = self.find_element_by(driver, self.locators.SHOW_RESULTS_BUTTON_ID, "id")
            self.click_on_element(show_button)
            assert self.wait_element_visible(driver, CustomerPageLocators.CUSTOMER_ID_TEXT, delay + 1)
        finally:
            cur_url = self.get_cur_url(driver)
            if customer_admin_url == cur_url:
                return True
            else:
                return False

    def go_to_management_inset_with_users_option(self, driver):
        delay = 5
        try:
            assert home_page_url == self.get_cur_url(driver)
            management_dropdown = self.find_element(driver, self.locators.MANAGEMENT_DROPDOWN)
            self.click_on_element(management_dropdown)
            users_option = self.find_element(driver, self.locators.MANAGEMENT_USERS_OPTION)
            self.click_on_element(users_option)
        finally:
            cur_url = self.get_cur_url(driver)
            if user_management_page_url == cur_url:
                return True
            else:
                return False
