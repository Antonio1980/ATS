import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.customer.customer import Customer
from src.base.log_decorator import automation_logger
from tests.platform_tests_base.home_page import HomePage
from tests.platform_tests_base.market_order_panel_page import MarketOrderPanelPage

test_case = '3356'


@allure.feature('Order Book')
@allure.story('Bests orders presented at the Trading Platform for all.')
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='First 30 orders are presented - Buy')
@allure.severity(allure.severity_level.NORMAL)
@allure.title('ORDER BOOK TEST')
@allure.description("""
    Verify that guest user able to see best 30 BUY Orders at the Trading Platform.
    """)
@allure.testcase(BaseConfig.GITLAB_URL + "/order_book_tests/C3356_bests_30_buy_orders_presented_test.py",
                 "TestBestOrdersBuyPresented")
@pytest.mark.usefixtures("r_time_count", "market_maker", "web_driver")
@pytest.mark.order_book
@pytest.mark.smoke
@pytest.mark.ui
class TestBestOrdersBuyPresented(object):

    home_page = HomePage()
    customer = Customer()
    market_order_panel = MarketOrderPanelPage()
    locators = market_order_panel.locators
    browser = customer.get_browser_functionality()

    @allure.step("Starting with: test_best_buy_orders_presented")
    @automation_logger(logger)
    def test_best_buy_orders_presented(self, web_driver):
        logger.logger.info("TEST CASE N: {0}".format(test_case))
        result = 0
        delay = float(BaseConfig.UI_DELAY)
        try:
            assert self.home_page.open_home_page(web_driver), "Home page is not opened"
            usd_title_menu = self.browser.wait_element_clickable(web_driver, self.locators.USD, delay)
            self.browser.click_on_element(usd_title_menu)
            btc_from_dropdown = self.browser.wait_element_presented(web_driver,
                                                                    self.locators.USD_OPTION_FROM_USD_DROPDOWN, delay)
            self.browser.click_on_element(btc_from_dropdown)

            self.browser.execute_js(web_driver, '''$('li[data-instrumentId=1007]').click()''')

            assert self.browser.wait_element_presented(
                web_driver, self.locators.BTC_USD_TITLE_ON_INSTRUMENT_QUICK_INFO_PANEL, delay), \
                "BTC_USD_TITLE is not found"
            best_price_and_quantity = Instruments.get_orders_best_price_and_quantity(1007, "sell", 2)
            items = self.browser.find_elements(web_driver, self.locators.ORDER_BOOK_ENTITIES_BUYERS)
            order_book_entities = []
            for i in items:
                _ = float(self.browser.get_attribute_from_element(i, "title"))
                order_book_entities.append(_)
            best_price = []
            for x in best_price_and_quantity:
                _ = x[0]
                best_price.append(_)
            order_book_entities_length = len(order_book_entities)
            best_price_cut = best_price[:order_book_entities_length]
            assert order_book_entities == best_price_cut, "Order Book is not equal best prices"
            logger.logger.info("TEST CASE - {0} IS PASSED !!!".format(test_case))
            result = 1
        finally:
            Instruments.update_test_case(BaseConfig.TESTRAIL_RUN, test_case, result)
