from src.base import logger
from tests.platform_tests_base.base_page import BasePage
from src.base.log_decorator import automation_logger
from tests.platform_tests_base.locators import market_order_panel_locators


class MarketOrderPanelPage(BasePage):
    
    def __init__(self):
        super(MarketOrderPanelPage, self).__init__()
        self.locators = market_order_panel_locators

    @automation_logger(logger)
    def select_tradable_instrument(self, driver):
        try:
            instrument = self.find_element(driver, self.locators.USD)
            self.click_on_element(instrument)
            image_usd = self.find_element(driver, self.locators.IMAGE_USD)
            self.click_on_element(image_usd)
            asset_bch = self.find_element(driver, self.locators.ASSET_BCH)
            self.click_on_element(asset_bch)
            return True
        except Exception as e:
            logger.logger.error("{0} select_tradable_instrument failed with error: {1}".format(e.__class__.__name__,
                                                                                               e.__cause__), e)
            return False

    @automation_logger(logger)
    def availability_for_trading(self, driver):
        try:
            assets_usd = self.find_elements(driver, self.locators.USD_ASSETS)
            assert assets_usd[1]
            assets_bch = self.find_elements(driver, self.locators.BCH_ASSETS)
            assert assets_bch[0]
            return True
        except Exception as e:
            logger.logger.error("{0} availability_for_trading failed with error: {1}".format(e.__class__.__name__,
                                                                                             e.__cause__), e)
            return False
