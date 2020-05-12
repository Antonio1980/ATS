import time
from src.base import logger
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger
from tests.platform_tests_base.base_page import BasePage
from tests.platform_tests_base.locators import main_screen_locators


class MainScreenPage(BasePage):

    def __init__(self):
        super(MainScreenPage, self).__init__()
        self.locators = main_screen_locators
        self.script_signin_button = "return $('#dx_header .loginButtons').is(':visible');"
        self.script_signup_button = "return $('#dx_header .signUpLink').is(':visible');"
        self.script_usd = "$('.assetsGroupTypeFilter_exchange_usd .usd').click(); $('.assetsGroupTypeFilter_exchange_usd .usd').click();"
        self.script_eur = "$('.assetsGroupTypeFilter_exchange_eur .eur').click(); $('.assetsGroupTypeFilter_exchange_eur .eur').click();"
        self.script_gbp = "$('.assetsTypeFilter_exchange_gbp .gbp').click(); $('.assetsTypeFilter_exchange_gbp .gbp').click();"
        self.script_jpy = "$('.assetsTypeFilter_exchange_jpy .jpy').click(); $('.assetsTypeFilter_exchange_jpy .jpy').click();"
        self.script_stocks_usd = "$('.assetsGroupTypeFilter_exchange_group_stocks_usd .usd').click(); $('.assetsGroupTypeFilter_exchange_group_stocks_usd .usd').click();"
        self.script_stocks_btc = "$('.assetsGroupTypeFilter_exchange_group_stocks_btc .btc').click(); $('.assetsGroupTypeFilter_exchange_group_stocks_btc .btc').click();"
        self.script_etf_usd = "$('.assetsGroupTypeFilter_exchanggroup_etfe_usd .usd').click(); $('.assetsGroupTypeFilter_exchanggroup_etfe_usd .usd').click();"
        self.script_etf_btc = "$('.assetsGroupTypeFilter_exchangegroup_etf_btc .btc').click(); $('.assetsGroupTypeFilter_exchangegroup_etf_btc').click();"

    @automation_logger(logger)
    def check_asset_panel_by_tab(self, currencies_items):
        time.sleep(3.0)
        for i in currencies_items:
            assert i.find_element_by_xpath("./div/div[@class='dot']")
            icon_val = i.find_element_by_xpath("./div[@class='graphData']/img[@class='assetIcon']").get_attribute('src')
            full_title = i.find_element_by_xpath(
                "div[@class = 'graphData']/div[@class='assetFullTitle']").get_attribute('innerText')
            title = i.find_element_by_xpath("div[@class = 'graphData']/div[@class='assetTitle']").get_attribute(
                'innerText')
            twenty_four_hour_change = i.find_element_by_xpath(
                "div[@class = 'countedData']/div[@class='assetChange24h']").get_attribute('innerText')
            common_price = i.find_element_by_xpath(
                "./div[@class = 'countedData']/div[@class='assetPrice']/div[@class='commonPrice']").get_attribute(
                'innerText')
            usd_price = i.find_element_by_xpath(
                "./div[@class = 'countedData']/div[@class='assetPrice']/div[@class='usdPrice']").get_attribute(
                'innerText')
            volume_text = i.find_element_by_xpath(
                "./div[@class = 'countedData']/div[@class='assetVolume24h']/div[@class='volumeText']").get_attribute(
                'innerText')
            volume_value = i.find_element_by_xpath(
                "./div[@class = 'countedData']/div[@class='assetVolume24h']/div[@class='volumeValue']").get_attribute(
                'innerText')
            underlying_currency = i.find_element_by_xpath(
                "./div[@class = 'countedData']/div[@class='assetVolume24h']/div[@class='underlyingCurrency']").get_attribute(
                'innerText')
            assert '_missing.svg' not in icon_val
            assert full_title != ""
            assert title != ""
            assert twenty_four_hour_change != ""
            assert common_price != ""
            assert usd_price != ""
            assert volume_text != ""
            assert volume_value != ""
            assert underlying_currency != ""

    @automation_logger(logger)
    def generate_x_path_for_volume(self, instrument_id):
        return "//*[@id='dx_platform']//li[@data-instrumentid='" + str(instrument_id) + "']//div[@class='volumeValue']"

    @automation_logger(logger)
    def generate_x_path_for_change(self, instrument_id):
        return "//*[@id='dx_platform']//li[@data-instrumentid='" + str(
            instrument_id) + "']//div[@class='assetChange24h']"

    @automation_logger(logger)
    def get_all_base_names(self, currencies_items):
        list_of_names = []
        for i in currencies_items:
            title = i.find_element_by_xpath("div[@class = 'graphData']/div[@class='assetTitle']").get_attribute(
                'innerText')
            list_of_names.append(title)
        return list_of_names

    @automation_logger(logger)
    def get_all_volume(self, currencies_items):
        list_of_volume = []
        for i in currencies_items:
            volume_value = i.find_element_by_xpath(
                "./div[@class = 'countedData']/div[@class='assetVolume24h']/div[@class='volumeValue']").get_attribute(
                'innerText')
            list_of_volume.append(float(volume_value.replace(",", "")))
        return list_of_volume

    @automation_logger(logger)
    def get_all_24_h_change(self, currencies_items):
        list_of_24_h_change = []
        for i in currencies_items:
            twenty_four_hour_change = i.find_element_by_xpath(
                "div[@class = 'countedData']/div[@class='assetChange24h']").get_attribute('innerText')
            list_of_24_h_change.append(float(twenty_four_hour_change))
        return list_of_24_h_change

    # There is assetTypeId  != 4 in the select. Cause: STO is not available on the Web Platform at the moment.
    @automation_logger(logger)
    def get_all_base_names_db(self, instrument_name):
        name_db = list(Instruments.run_mysql_query((
                "SELECT instruments.name FROM instruments JOIN assets ON instruments.name = assets.name WHERE assets.fullName LIKE '%" + str(
            instrument_name) + "' and assets.assetTypeId != 4 and instruments.statusId = 1")))
        list_of_names_db = list(sum(name_db, ()))
        list_names_db = []
        for i in list_of_names_db:
            list_names_db.append(i.replace('/' + str(instrument_name) + '', ''))
        return list_names_db

    @automation_logger(logger)
    def generate_x_path_last_trade_price(self, instrument_name):
        instrument_id = \
            Instruments.run_mysql_query("SELECT id FROM instruments WHERE name = '" + str(instrument_name) + "'")[0][0]
        x = "//li[@data-instrumentid = '" + str(instrument_id) + "']//div[@class='usdPrice']"
        return x

    @automation_logger(logger)
    def set_favorites(self, currencies_items, browser):
        list_of_names = []

        for i in currencies_items:
            fav = i.get_attribute("class")
            if 'favorite' in fav:
                title_1 = i.find_element_by_xpath("./div[@class = 'graphData']/div[@class='assetTitle']").get_attribute(
                    'innerText')
                list_of_names.append(title_1)
            else:
                dot = i.find_element_by_xpath("./div/div[@class='dot']")
                browser.click_on_element(dot)
                time.sleep(2.0)
                title = i.find_element_by_xpath("div[@class = 'graphData']/div[@class='assetTitle']").get_attribute(
                    'innerText')
                list_of_names.append(title)
        return list_of_names

    # Getting list of filtered currencies at the Funds panel
    @automation_logger(logger)
    def get_filtered_currencies(self, currencies_names):
        list_of_names = []
        for i in currencies_names:
            name = i.get_attribute('innerText')
            list_of_names.append(name)
        return list_of_names

    # Getting available currencies by specific type from DB
    @automation_logger(logger)
    def get_list_of_specific_type_currencies_db(self, currency_type):
        if currency_type != "All":
            query = (
                    "SELECT DISTINCT currencies.code FROM currencies JOIN currency_types "
                    " ON currencies.typeId=currency_types.id JOIN assets ON currencies.id=assets.baseCurrencyId"
                    " OR currencies.id=assets.quotedCurrencyId JOIN instruments ON assets.id=instruments.assetId"
                    " where currency_types.name='" + str(currency_type) + "' AND instruments.statusId=1")
        else:
            assert currency_type == "All"
            query = ("SELECT DISTINCT currencies.code FROM currencies JOIN currency_types "
                     "ON currencies.typeId=currency_types.id JOIN assets ON currencies.id=assets.baseCurrencyId "
                     "OR currencies.id=assets.quotedCurrencyId JOIN instruments ON assets.id=instruments.assetId "
                     "WHERE instruments.statusId=1")
        currencies_db = Instruments.run_mysql_query(query)
        if currencies_db is not None:
            list_of_names_db = list(sum(currencies_db, ()))
            return list_of_names_db
        else:
            return currencies_db
