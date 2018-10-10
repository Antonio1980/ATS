# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from ddt import ddt, data, unpack
from src.base.browser import Browser
from test_definitions import BaseConfig
from src.base.instruments import Instruments
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages.signin_page import SignInPage
from tests.tests_web_platform.locators import main_screen_locators


@ddt
@test(groups=['home_page', ])
class AssetPanelUiTest(unittest.TestCase):
    def setUp(self):
        self.test_case = '6246'
        self.home_page = HomePage()
        self.signin_page = SignInPage()
        self.locators = main_screen_locators
        self.email = self.signin_page.email
        self.password = self.signin_page.password
        self.test_run = BaseConfig.TESTRAIL_RUN

    @test(groups=['sanity', 'positive', 'ui', ])
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_main_trading_screen(self, browser):
        self.driver = WebDriverFactory.get_browser(browser)
        delay = 5
        step1, step2, step3, step4 , step5= False, False, False, False, False
        try:
            step1 = self.home_page.open_signin_page(self.driver, delay)
            step2 = self.signin_page.sign_in(self.driver, self.email, self.password)
            try:
                assert Browser.wait_element_presented(self.driver, self.locators.BTC_CURRENCY_NOT_SELECTED, delay)
                assert Browser.wait_element_presented(self.driver, self.locators.ETH_CURRENCY_NOT_SELECTED, delay)
                assert Browser.wait_element_presented(self.driver, self.locators.DXEX_CURRENCY_SELECTED, delay)
                assert Browser.wait_element_presented(self.driver, self.locators.USD_DEFAULT_CURRENCY_DROPDOWN_NOT_SELECTED, delay)
                leading_currency_menu = Browser.find_element(self.driver, self.locators.LEADING_CURRENCY_MENU)
                search_box = Browser.find_element(self.driver, self.locators.SEARCH_BOX)
                if leading_currency_menu.location['x'] == search_box.location['x'] and\
                        leading_currency_menu.location['y'] < search_box.location['y']:
                    step3 = True
                assert Browser.wait_element_presented(self.driver, self.locators.STAR_ICON_FAV, delay)
                assert Browser.wait_element_presented(self.driver, self.locators.TWENTY_FOUR_H_CHANGE_NOT_SELECTED, delay)
                assert Browser.wait_element_presented(self.driver, self.locators.TWENTY_FOUR_H_VOLUME_SELECTED, delay)      # verify that that param meets to spec
                assert Browser.wait_element_presented(self.driver, self.locators.CURRENCIES_LIST_PANEL, delay)
                dxex_bitcoin_cash_bch_currency = Browser.find_element(self.driver, self.locators.DXEX_BITCOIN_CASH_BCH_CURRENCY)
                display_dxex_bitcoin_cash_bch_currency = Browser.get_attribute_from_element(dxex_bitcoin_cash_bch_currency, 'style')
                dxex_dash_dash_currency = Browser.find_element(self.driver, self.locators.DXEX_DASH_DASH_CURRENCY)
                display_dxex_dash_dash_currency = Browser.get_attribute_from_element(dxex_dash_dash_currency, 'style')
                dxex_litecoin_ltc_currency = Browser.find_element(self.driver, self.locators.DXEX_LITECOIN_LTC_CURRENCY)
                display_dxex_litecoin_ltc_currency = Browser.get_attribute_from_element(dxex_litecoin_ltc_currency, 'style')
                dxex_ripple_xrp_currency = Browser.find_element(self.driver, self.locators.DXEX_RIPPLE_XRP_CURRENCY)
                display_dxex_ripple_xrp_currency = Browser.get_attribute_from_element(dxex_ripple_xrp_currency, 'style')
                if Browser.wait_element_presented(self.driver, self.locators.DXEX_CURRENCY_SELECTED, delay):
                    if Browser.wait_element_presented(self.driver, self.locators.DXEX_BITCOIN_CASH_BCH_CURRENCY, delay) and display_dxex_bitcoin_cash_bch_currency is None \
                            or display_dxex_bitcoin_cash_bch_currency != 'display:none;':
                        assert Browser.wait_element_presented(self.driver, self.locators.DXEX_BITCOIN_CASH_BCH_CURRENCY_24_HOUR_CHANGE_PERCENTAGE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.DXEX_BITCOIN_CASH_BCH_CURRENCY_LAST_PRICE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.DXEX_BITCOIN_CASH_BCH_CURRENCY_USD_LAST_PRICE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.DXEX_BITCOIN_CASH_BCH_CURRENCY_24_HOUR_VOLUME, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.DXEX_BITCOIN_CASH_BCH_CURRENCY_24_HOUR_VOLUME_QUOTED_CURRENCY, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.DXEX_BITCOIN_CASH_BCH_CURRENCY_SYMBOL, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.DXEX_BITCOIN_CASH_BCH_CURRENCY_NAME, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.DXEX_BITCOIN_CASH_BCH_CURRENCY_CODE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.DXEX_BITCOIN_CASH_BCH_CURRENCY_FAV_CIRCLE, delay)
                    if Browser.wait_element_presented(self.driver, self.locators.DXEX_DASH_DASH_CURRENCY, delay) and display_dxex_dash_dash_currency is None \
                            or display_dxex_dash_dash_currency != 'display:none;':
                        assert Browser.wait_element_presented(self.driver, self.locators.DXEX_DASH_DASH_CURRENCY_24_HOUR_CHANGE_PERCENTAGE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.DXEX_DASH_DASH_CURRENCY_LAST_PRICE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.DXEX_DASH_DASH_CURRENCY_USD_LAST_PRICE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.DXEX_DASH_DASH_CURRENCY_24_HOUR_VOLUME, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.DXEX_DASH_DASH_CURRENCY_24_HOUR_VOLUME_QUOTED_CURRENCY, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.DXEX_DASH_DASH_CURRENCY_SYMBOL, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.DXEX_DASH_DASH_CURRENCY_NAME, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.DXEX_DASH_DASH_CURRENCY_CODE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.DXEX_DASH_DASH_CURRENCY_FAV_CIRCLE, delay)
                    if Browser.wait_element_presented(self.driver, self.locators.DXEX_LITECOIN_LTC_CURRENCY, delay) and display_dxex_litecoin_ltc_currency is None \
                            or display_dxex_litecoin_ltc_currency != 'display:none;':
                        assert Browser.wait_element_presented(self.driver, self.locators.DXEX_LITECOIN_LTC_CURRENCY_24_HOUR_CHANGE_PERCENTAGE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.DXEX_LITECOIN_LTC_CURRENCY_LAST_PRICE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.DXEX_LITECOIN_LTC_CURRENCY_USD_LAST_PRICE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.DXEX_LITECOIN_LTC_CURRENCY_24_HOUR_VOLUME, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.DXEX_LITECOIN_LTC_CURRENCY_24_HOUR_VOLUME_QUOTED_CURRENCY, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.DXEX_LITECOIN_LTC_CURRENCY_SYMBOL, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.DXEX_LITECOIN_LTC_CURRENCY_NAME, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.DXEX_LITECOIN_LTC_CURRENCY_CODE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.DXEX_LITECOIN_LTC_CURRENCY_FAV_CIRCLE, delay)
                    if Browser.wait_element_presented(self.driver, self.locators.DXEX_RIPPLE_XRP_CURRENCY, delay) and display_dxex_ripple_xrp_currency is None \
                            or display_dxex_ripple_xrp_currency != 'display:none;':
                        assert Browser.wait_element_presented(self.driver, self.locators.DXEX_RIPPLE_XPR_CURRENCY_24_HOUR_CHANGE_PERCENTAGE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.DXEX_RIPPLE_XPR_CURRENCY_LAST_PRICE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.DXEX_RIPPLE_XPR_CURRENCY_USD_LAST_PRICE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.DXEX_RIPPLE_XRP_CURRENCY_24_HOUR_VOLUME, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.DXEX_RIPPLE_XPR_CURRENCY_24_HOUR_VOLUME_QUOTED_CURRENCY, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.DXEX_RIPPLE_XRP_CURRENCY_SYMBOL, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.DXEX_RIPPLE_XRP_CURRENCY_NAME, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.DXEX_RIPPLE_XRP_CURRENCY_CODE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.DXEX_RIPPLE_XRP_CURRENCY_FAV_CIRCLE, delay)
                    step4 = True
                step5 = True
            except Exception as e:
                print("Exception is occurred.".format(e))

        finally:
            if step1 and step2 and step3 and step4 and step5 is True:
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    def tearDown(self):
        Browser.close_browser(self.driver)
