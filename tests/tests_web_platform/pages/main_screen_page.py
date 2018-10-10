from tests.tests_web_platform.locators import main_screen_locators
from tests.tests_web_platform.pages import BasePage


class MainScreenPage(BasePage):
    def __init__(self):
        super(MainScreenPage, self).__init__()
        self.locators = main_screen_locators
        self.script_signin_button = "return $('#dx_header .loginButtons').is(':visible');"
        self.script_signup_button = "return $('#dx_header .signUpLink').is(':visible');"
