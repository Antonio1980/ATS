import allure
import pytest
from config_definitions import BaseConfig
from src.base import logger
from src.base.data_bases.redis_db import RedisDb
from src.base.data_bases.sql_db import SqlDb
from src.base.log_decorator import automation_logger

test_case = "8166"
instrument_id = 1007


@allure.title("TICKER")
@allure.description(""".
    Verification  "Last Trade Price"
    1. Get value "Last Trade Price" from Redis
    2. Get value "Last Trade Price" from DB
    5. Compare price from Redis with price from DB. They must be equal.
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Last Trade Price Verification')
@allure.testcase(BaseConfig.GITLAB_URL +
                 "/ticker_tests/C8166_last_trade_price_verification_test.py",
                 "TestLastPriceVerification")
@pytest.mark.incremental
@pytest.mark.usefixtures("r_time_count", )
@pytest.mark.ticker
@pytest.mark.functional
class TestLastPriceVerification(object):
    redis_last_price = None
    db_last_price = None

    @allure.step("Starting with: test_get_redis_last_trade_price")
    @automation_logger(logger)
    def test_get_redis_last_trade_price(self):
        TestLastPriceVerification.redis_last_price = RedisDb.get_ticker_last_price(instrument_id)

    @allure.step("Proceed with: test_get_db_last_trade_price")
    @automation_logger(logger)
    def test_get_db_last_trade_price(self):
        TestLastPriceVerification.db_last_price = float(
            SqlDb.run_mysql_query("SELECT price FROM trades_crypto WHERE instrumentId =" + str(
                instrument_id) + " ORDER BY executionDate  DESC limit 1;")[0][0])

    @allure.step("Proceed with: test_compare_last_trade_price")
    @automation_logger(logger)
    def test_compare_last_trade_price(self):
        assert self.redis_last_price == self.db_last_price
        logger.logger.info("redis_price {0} == db_price {1}".format(self.redis_last_price, self.db_last_price))
        logger.logger.info("Test {0}".format(test_case))
        logger.logger.info("==================== TEST IS PASSED ====================")
