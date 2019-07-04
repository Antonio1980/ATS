import allure
import pytest
from datetime import datetime, timedelta
from config_definitions import BaseConfig
from src.base import logger
from src.base.data_bases.redis_db import RedisDb
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger

test_case = "8185"
instrument_id = 1007


@allure.title("TICKER")
@allure.description(""".
    Verification  "24h Change"
    1. Get value "Change" from Redis as 'redis_change'
    2. Get value "Last Trade Price" from DB as 'last_trade_price'
    3. Get data 24H ago 
    4. Get last trade price 24H ago from DB as 'price_24_h_ago'
    5. Calculation of '24h Change': round((((last_trade_price - price_24_h_ago)/price_24_h_ago) * 100), 2)
    5. Compare Change from Redis with  '24h Change' . They must be equal.
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='24H Change Verification')
@allure.testcase(BaseConfig.GITLAB_URL +
                 "/ticker_tests/C8185_24h_change_verification.py",
                 "Test24hChangeVerification")
@pytest.mark.incremental
@pytest.mark.usefixtures("r_time_count", )
@pytest.mark.ticker
@pytest.mark.functional
class Test24hChangeVerification(object):
    redis_change = None
    date_24_hours_ago = None
    last_trade_price = None

    @allure.step("Starting with: test_get_redis_change_price")
    @automation_logger(logger)
    def test_get_redis_change_price(self):
        Test24hChangeVerification.redis_change = RedisDb.get_ticker_change_24(instrument_id)
        assert self.redis_change is not None

    @allure.step("Proceed with: test_get_last_trade_price_in_db")
    @automation_logger(logger)
    def test_get_last_trade_price_in_db(self):
        price_query = ("SELECT price FROM trades_crypto WHERE direction='buy' AND instrumentId = '"
                       + str(instrument_id) + "'ORDER BY executionDate DESC limit 1")
        Test24hChangeVerification.last_trade_price = float(Instruments.run_mysql_query(price_query)[0][0])
        assert self.last_trade_price is not None

    @allure.step("Proceed with: test_get_date_24_hours_ago")
    @automation_logger(logger)
    def test_get_date_24_hours_ago(self):
        Test24hChangeVerification.date_24_hours_ago = datetime.utcnow() + timedelta(days=-1)
        assert self.date_24_hours_ago is not None

    @allure.step("Proceed with: test_get_last_trade_price_24_h_ago_in_db")
    @automation_logger(logger)
    def test_get_last_trade_price_24_h_ago_in_db(self):
        price_24_h_ago_query = ("SELECT price FROM trades_crypto WHERE instrumentId='" + str(instrument_id) +
                                "'AND direction='buy' AND executionDate < '" + str(self.date_24_hours_ago) +
                                "' ORDER BY executionDate DESC LIMIT 1")
        Test24hChangeVerification.price_24_h_ago = float(
            Instruments.run_mysql_query(price_24_h_ago_query)[0][0])
        assert self.price_24_h_ago is not None

    @allure.step("Proceed with: test_calculation_of_24_h_change")
    @automation_logger(logger)
    def test_calculation_of_24_h_change(self):
        Test24hChangeVerification.value_24_change = round((((self.last_trade_price - self.price_24_h_ago)
                                                            / self.price_24_h_ago) * 100), 2)
        assert self.value_24_change is not None

    @allure.step("Proceed with: test_compare_change_price")
    @automation_logger(logger)
    def test_compare_change_price(self):
        assert self.redis_change == self.value_24_change
        logger.logger.info("redis_change {0} == value_24_change {1}".format(self.redis_change, self.value_24_change))
        logger.logger.info("Test {0}".format(test_case))
        logger.logger.info("==================== TEST IS PASSED ====================")
