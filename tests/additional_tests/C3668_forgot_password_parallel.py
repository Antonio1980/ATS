import time
import pytest
from queue import Queue
from src.base import logger
from threading import Thread
from src.base.enums import Browsers
from src.base.instruments import Instruments
from src.base.customer.customer import Customer
from src.base.log_decorator import automation_logger
from src.drivers.webdriver_factory import WebDriverFactory
from tests.platform_tests_base.home_page import HomePage
from tests.platform_tests_base.signin_page import SignInPage
from tests.platform_tests_base import wtp_signin_page_url
from tests.platform_tests_base.signup_page import SignUpPage
from tests.platform_tests_base.forgot_password_page import ForgotPasswordPage


q = Queue(maxsize=0)

mac_chrome_details = ('Chrome', '68.0', 'OS X', 'Sierra', '1920x1080')
mac_safari_details = ('Safari', '10.1', 'OS X', 'Sierra', '1920x1080')
win_chrome_details = ('Chrome', '68.0', 'Windows', '10', '2048x1536')
win_firefox_details = ('Firefox', '58.0', 'Windows', '10', '2048x1536')
win_edge_details = ('Edge', '17.0', 'Windows', '10', '2048x1536')

browsers = [mac_chrome_details, mac_safari_details, win_chrome_details, win_firefox_details, win_edge_details, ]

for browser_ in browsers:
    q.put(browser_)
num_threads = q.qsize()


@pytest.mark.skip
@pytest.mark.advanced
@automation_logger(logger)
def test_forgot_password_full_flow(queue):
    driver = None
    test_case = '3668'
    customer = Customer()
    home_page = HomePage()
    signin_page = SignInPage()
    signup_page = SignUpPage()
    password = customer.password
    new_password = password + "Qa"
    forgot_password_page = ForgotPasswordPage()
    element = "//*[@class='userEmail'][contains(text(),'{0}')]".format(customer.email)
    WebDriverFactory.start_selenium_server(Browsers.CHROME.value)

    while queue.empty() is False:
        try:
            _browser = queue.get()
            driver = WebDriverFactory.get_remote_driver(_browser)
            assert home_page.open_signup_page(driver)
            assert signup_page.fill_signup_form(driver, customer.username, customer.email, customer.password, element)
            assert signin_page.go_by_token_url(driver, wtp_signin_page_url)
            # Option 1- forgot password, Option 2- register link
            assert signin_page.click_on_link(driver, 1)
            assert forgot_password_page.fill_email_address_form(driver, customer.email)
            verification_url = Instruments.get_mail_gun_item(customer)
            assert forgot_password_page.go_by_token_url(driver, verification_url)
            assert forgot_password_page.set_new_password(driver, new_password, verification_url)
            logger.logger.info("=============== TEST CASE - {0} IS PASSED !!! ===============".format(test_case))

        finally:
            driver.quit()
            time.sleep(1)
            queue.task_done()


for i in range(num_threads):
    worker = Thread(target=test_forgot_password_full_flow, args=(q, ))
    worker.setDaemon(True)
    worker.start()

q.join()
