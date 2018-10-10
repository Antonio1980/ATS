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
        self.test_case = '6261'
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
        step1, step2, step3, step4 = False, False, False, False
        try:
            step1 = self.home_page.open_signin_page(self.driver, delay)
            step2 = self.signin_page.sign_in(self.driver, self.email, self.password)
            try:
                eth_currency_button = Browser.find_element(self.driver, self.locators.ETH_CURRENCY_NOT_SELECTED)
                Browser.try_click(self.driver, eth_currency_button, 2)
                eth_bitcoin_cash_bch_currency = Browser.find_element(self.driver, self.locators.ETH_BITCOIN_CASH_BCH_CURRENCY)
                display_eth_bitcoin_cash_bch_currency = Browser.get_attribute_from_element(eth_bitcoin_cash_bch_currency, 'style')
                eth_dash_dash_currency = Browser.find_element(self.driver, self.locators.ETH_DASH_DASH_CURRENCY)
                display_eth_dash_dash_currency = Browser.get_attribute_from_element(eth_dash_dash_currency, 'style')
                eth_dx_coin_dxex_currency = Browser.find_element(self.driver, self.locators.ETH_DX_COIN_DXEX_CURRENCY)
                display_eth_dx_coin_dxex_currency = Browser.get_attribute_from_element(eth_dx_coin_dxex_currency, 'style')
                eth_litecoin_ltc_currency = Browser.find_element(self.driver, self.locators.ETH_LITECOIN_LTC_CURRENCY)
                display_eth_litecoin_ltc_currency = Browser.get_attribute_from_element(eth_litecoin_ltc_currency,'style')
                eth_ripple_xrp_currency = Browser.find_element(self.driver, self.locators.ETH_RIPPLE_XRP_CURRENCY)
                display_eth_ripple_xrp_currency = Browser.get_attribute_from_element(eth_ripple_xrp_currency, 'style')
                if Browser.wait_element_presented(self.driver, self.locators.ETH_CURRENCY_SELECTED, delay):
                    if Browser.wait_element_presented(self.driver, self.locators.ETH_BITCOIN_CASH_BCH_CURRENCY, delay) and display_eth_bitcoin_cash_bch_currency is None \
                            or display_eth_bitcoin_cash_bch_currency != 'display:none;':
                        assert Browser.wait_element_presented(self.driver, self.locators.ETH_BITCOIN_CASH_BCH_CURRENCY_24_HOUR_CHANGE_PERCENTAGE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.ETH_BITCOIN_CASH_BCH_CURRENCY_LAST_PRICE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.ETH_BITCOIN_CASH_BCH_CURRENCY_USD_LAST_PRICE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.ETH_BITCOIN_CASH_BCH_CURRENCY_24_HOUR_VOLUME, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.ETH_BITCOIN_CASH_BCH_CURRENCY_24_HOUR_VOLUME_QUOTED_CURRENCY, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.ETH_BITCOIN_CASH_BCH_CURRENCY_SYMBOL, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.ETH_BITCOIN_CASH_BCH_CURRENCY_NAME, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.ETH_BITCOIN_CASH_BCH_CURRENCY_CODE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.ETH_BITCOIN_CASH_BCH_CURRENCY_FAV_CIRCLE, delay)
                    if Browser.wait_element_presented(self.driver, self.locators.ETH_DASH_DASH_CURRENCY, delay) and display_eth_dash_dash_currency is None \
                            or display_eth_dash_dash_currency != 'display:none;':
                        assert Browser.wait_element_presented(self.driver, self.locators.ETH_DASH_DASH_CURRENCY_24_HOUR_CHANGE_PERCENTAGE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.ETH_DASH_DASH_CURRENCY_LAST_PRICE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.ETH_DASH_DASH_CURRENCY_USD_LAST_PRICE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.ETH_DASH_DASH_CURRENCY_24_HOUR_VOLUME, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.ETH_DASH_DASH_CURRENCY_24_HOUR_VOLUME_QUOTED_CURRENCY, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.ETH_DASH_DASH_CURRENCY_SYMBOL, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.ETH_DASH_DASH_CURRENCY_NAME, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.ETH_DASH_DASH_CURRENCY_CODE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.ETH_DASH_DASH_CURRENCY_FAV_CIRCLE, delay)
                    if Browser.wait_element_presented(self.driver, self.locators.ETH_LITECOIN_LTC_CURRENCY, delay) and display_eth_litecoin_ltc_currency is None \
                            or display_eth_litecoin_ltc_currency != 'display:none;':
                        assert Browser.wait_element_presented(self.driver, self.locators.ETH_LITECOIN_LTC_CURRENCY_24_HOUR_CHANGE_PERCENTAGE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.ETH_LITECOIN_LTC_CURRENCY_LAST_PRICE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.ETH_LITECOIN_LTC_CURRENCY_USD_LAST_PRICE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.ETH_LITECOIN_LTC_CURRENCY_24_HOUR_VOLUME, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.ETH_LITECOIN_LTC_CURRENCY_24_HOUR_VOLUME_QUOTED_CURRENCY, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.ETH_LITECOIN_LTC_CURRENCY_SYMBOL, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.ETH_LITECOIN_LTC_CURRENCY_NAME, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.ETH_LITECOIN_LTC_CURRENCY_CODE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.ETH_LITECOIN_LTC_CURRENCY_FAV_CIRCLE, delay)
                    if Browser.wait_element_presented(self.driver, self.locators.ETH_RIPPLE_XRP_CURRENCY, delay) and display_eth_ripple_xrp_currency is None \
                            or display_eth_ripple_xrp_currency != 'display:none;':
                        assert Browser.wait_element_presented(self.driver, self.locators.ETH_RIPPLE_XPR_CURRENCY_24_HOUR_CHANGE_PERCENTAGE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.ETH_RIPPLE_XPR_CURRENCY_LAST_PRICE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.ETH_RIPPLE_XPR_CURRENCY_USD_LAST_PRICE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.ETH_RIPPLE_XRP_CURRENCY_24_HOUR_VOLUME, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.ETH_RIPPLE_XPR_CURRENCY_24_HOUR_VOLUME_QUOTED_CURRENCY, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.ETH_RIPPLE_XRP_CURRENCY_SYMBOL, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.ETH_RIPPLE_XRP_CURRENCY_NAME, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.ETH_RIPPLE_XRP_CURRENCY_CODE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.ETH_RIPPLE_XRP_CURRENCY_FAV_CIRCLE, delay)
                    if Browser.wait_element_presented(self.driver, self.locators.ETH_DX_COIN_DXEX_CURRENCY, delay) and display_eth_dx_coin_dxex_currency is None \
                            or display_eth_dx_coin_dxex_currency != 'display:none;':
                        assert Browser.wait_element_presented(self.driver, self.locators.ETH_DX_COIN_DXEX_CURRENCY_24_HOUR_CHANGE_PERCENTAGE,delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.ETH_DX_COIN_DXEX_CURRENCY_LAST_PRICE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.ETH_DX_COIN_DXEX_CURRENCY_USD_LAST_PRICE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.ETH_DX_COIN_DXEX_CURRENCY_24_HOUR_VOLUME, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.ETH_DX_COIN_DXEX_CURRENCY_24_HOUR_VOLUME_QUOTED_CURRENCY, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.ETH_DX_COIN_DXEX_CURRENCY_SYMBOL, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.ETH_DX_COIN_DXEX_CURRENCY_NAME, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.ETH_DX_COIN_DXEX_CURRENCY_CODE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.ETH_DX_COIN_DXEX_CURRENCY_FAV_CIRCLE, delay)
                    step3 = True
                btc_currency_button = Browser.find_element(self.driver, self.locators.BTC_CURRENCY_NOT_SELECTED)
                Browser.try_click(self.driver, btc_currency_button, 2)
                btc_etherium_eth_currency = Browser.find_element(self.driver, self.locators.BTC_ETHEREUM_ETH_CURRENCY)
                display_btc_etherium_eth_currency = Browser.get_attribute_from_element(btc_etherium_eth_currency, 'style')
                btc_bitcoin_cash_bch_currency = Browser.find_element(self.driver, self.locators.BTC_BITCOIN_CASH_BCH_CURRENCY)
                display_btc_bitcoin_cash_bch_currency = Browser.get_attribute_from_element(btc_bitcoin_cash_bch_currency, 'style')
                btc_dash_dash_currency = Browser.find_element(self.driver, self.locators.BTC_DASH_DASH_CURRENCY)
                display_btc_dash_dash_currency = Browser.get_attribute_from_element(btc_dash_dash_currency, 'style')
                btc_dx_coin_dxex_currency = Browser.find_element(self.driver, self.locators.BTC_DX_COIN_DXEX_CURRENCY)
                display_btc_dx_coin_dxex_currency = Browser.get_attribute_from_element(btc_dx_coin_dxex_currency,'style')
                btc_litecoin_ltc_currency = Browser.find_element(self.driver, self.locators.BTC_LITECOIN_LTC_CURRENCY)
                display_btc_litecoin_ltc_currency = Browser.get_attribute_from_element(btc_litecoin_ltc_currency,'style')
                btc_ripple_xrp_currency = Browser.find_element(self.driver, self.locators.BTC_RIPPLE_XRP_CURRENCY)
                display_btc_ripple_xrp_currency = Browser.get_attribute_from_element(btc_ripple_xrp_currency, 'style')
                if Browser.wait_element_presented(self.driver, self.locators.BTC_CURRENCY_SELECTED, delay):
                    if Browser.wait_element_presented(self.driver, self.locators.BTC_ETHEREUM_ETH_CURRENCY, delay) and display_btc_etherium_eth_currency is None \
                            or display_btc_etherium_eth_currency != 'display:none;':
                        assert Browser.wait_element_presented(self.driver, self.locators.BTC_ETHEREUM_ETH_CURRENCY_24_HOUR_CHANGE_PERCENTAGE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.BTC_ETHEREUM_ETH_CURRENCY_LAST_PRICE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.BTC_ETHEREUM_ETH_CURRENCY_USD_LAST_PRICE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.BTC_ETHEREUM_ETH_CURRENCY_24_HOUR_VOLUME, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.BTC_ETHEREUM_ETH_CURRENCY_24_HOUR_VOLUME_QUOTED_CURRENCY, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.BTC_ETHEREUM_ETH_CURRENCY_SYMBOL, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.BTC_ETHEREUM_ETH_CURRENCY_NAME, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.BTC_ETHEREUM_ETH_CURRENCY_CODE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.BTC_ETHEREUM_ETH_CURRENCY_FAV_CIRCLE, delay)
                    if Browser.wait_element_presented(self.driver, self.locators.BTC_BITCOIN_CASH_BCH_CURRENCY, delay) and display_btc_bitcoin_cash_bch_currency is None \
                            or display_btc_bitcoin_cash_bch_currency != 'display:none;':
                        assert Browser.wait_element_presented(self.driver, self.locators.BTC_BITCOIN_CASH_BCH_CURRENCY_24_HOUR_CHANGE_PERCENTAGE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.BTC_BITCOIN_CASH_BCH_CURRENCY_LAST_PRICE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.BTC_BITCOIN_CASH_BCH_CURRENCY_USD_LAST_PRICE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.BTC_BITCOIN_CASH_BCH_CURRENCY_24_HOUR_VOLUME, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.BTC_BITCOIN_CASH_BCH_CURRENCY_24_HOUR_VOLUME_QUOTED_CURRENCY, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.BTC_BITCOIN_CASH_BCH_CURRENCY_SYMBOL, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.BTC_BITCOIN_CASH_BCH_CURRENCY_NAME, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.BTC_BITCOIN_CASH_BCH_CURRENCY_CODE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.BTC_BITCOIN_CASH_BCH_CURRENCY_FAV_CIRCLE, delay)
                    if Browser.wait_element_presented(self.driver, self.locators.BTC_DASH_DASH_CURRENCY, delay) and display_btc_dash_dash_currency is None \
                            or display_btc_dash_dash_currency != 'display:none;':
                        assert Browser.wait_element_presented(self.driver, self.locators.BTC_DASH_DASH_CURRENCY_24_HOUR_CHANGE_PERCENTAGE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.BTC_DASH_DASH_CURRENCY_LAST_PRICE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.BTC_DASH_DASH_CURRENCY_USD_LAST_PRICE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.BTC_DASH_DASH_CURRENCY_24_HOUR_VOLUME, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.BTC_DASH_DASH_CURRENCY_24_HOUR_VOLUME_QUOTED_CURRENCY, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.BTC_DASH_DASH_CURRENCY_SYMBOL, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.BTC_DASH_DASH_CURRENCY_NAME, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.BTC_DASH_DASH_CURRENCY_CODE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.BTC_DASH_DASH_CURRENCY_FAV_CIRCLE, delay)
                    if Browser.wait_element_presented(self.driver, self.locators.BTC_LITECOIN_LTC_CURRENCY, delay) and display_btc_litecoin_ltc_currency is None \
                            or display_btc_litecoin_ltc_currency != 'display:none;':
                        assert Browser.wait_element_presented(self.driver, self.locators.BTC_LITECOIN_LTC_CURRENCY_24_HOUR_CHANGE_PERCENTAGE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.BTC_LITECOIN_LTC_CURRENCY_LAST_PRICE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.BTC_LITECOIN_LTC_CURRENCY_USD_LAST_PRICE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.BTC_LITECOIN_LTC_CURRENCY_24_HOUR_VOLUME, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.BTC_LITECOIN_LTC_CURRENCY_24_HOUR_VOLUME_QUOTED_CURRENCY, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.BTC_LITECOIN_LTC_CURRENCY_SYMBOL, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.BTC_LITECOIN_LTC_CURRENCY_NAME, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.BTC_LITECOIN_LTC_CURRENCY_CODE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.BTC_LITECOIN_LTC_CURRENCY_FAV_CIRCLE, delay)
                    if Browser.wait_element_presented(self.driver, self.locators.BTC_RIPPLE_XRP_CURRENCY, delay)and display_btc_ripple_xrp_currency is None \
                            or display_btc_ripple_xrp_currency != 'display:none;':
                        assert Browser.wait_element_presented(self.driver, self.locators.BTC_RIPPLE_XPR_CURRENCY_24_HOUR_CHANGE_PERCENTAGE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.BTC_RIPPLE_XPR_CURRENCY_LAST_PRICE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.BTC_RIPPLE_XPR_CURRENCY_USD_LAST_PRICE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.BTC_RIPPLE_XRP_CURRENCY_24_HOUR_VOLUME, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.BTC_RIPPLE_XPR_CURRENCY_24_HOUR_VOLUME_QUOTED_CURRENCY, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.BTC_RIPPLE_XRP_CURRENCY_SYMBOL, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.BTC_RIPPLE_XRP_CURRENCY_NAME, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.BTC_RIPPLE_XRP_CURRENCY_CODE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.BTC_RIPPLE_XRP_CURRENCY_FAV_CIRCLE, delay)
                    if Browser.wait_element_presented(self.driver, self.locators.BTC_DX_COIN_DXEX_CURRENCY, delay) and display_btc_dx_coin_dxex_currency is None \
                            or display_btc_dx_coin_dxex_currency != 'display:none;':
                        assert Browser.wait_element_presented(self.driver, self.locators.BTC_DX_COIN_DXEX_CURRENCY_24_HOUR_CHANGE_PERCENTAGE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.BTC_DX_COIN_DXEX_CURRENCY_LAST_PRICE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.BTC_DX_COIN_DXEX_CURRENCY_USD_LAST_PRICE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.BTC_DX_COIN_DXEX_CURRENCY_24_HOUR_VOLUME, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.BTC_DX_COIN_DXEX_CURRENCY_24_HOUR_VOLUME_QUOTED_CURRENCY, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.BTC_DX_COIN_DXEX_CURRENCY_SYMBOL, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.BTC_DX_COIN_DXEX_CURRENCY_NAME, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.BTC_DX_COIN_DXEX_CURRENCY_CODE, delay)
                        assert Browser.wait_element_presented(self.driver, self.locators.BTC_DX_COIN_DXEX_CURRENCY_FAV_CIRCLE, delay)
                    step4 = True
            except Exception as e:
                print("Exception is occurred.".format(e))

        finally:
            if step1 and step2 and step3 and step4 is True:
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    def tearDown(self):
        Browser.close_browser(self.driver)
