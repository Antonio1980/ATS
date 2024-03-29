import allure
import pytest
from datetime import datetime, timedelta
from config_definitions import BaseConfig
from src.base import logger
from src.base.data_bases.redis_db import RedisDb
from src.base.data_bases.sql_db import SqlDb
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger

test_case = "8194"
instrument_id = 1007


@allure.title("TICKER")
@allure.description(""".
    Verification  "24H High Value"
    1. Get value "24H High Value" from Redis
    2. Get value "24H High Value" from DB. If value is None , "24H High Value" = Last Price 24
    5. Compare value from Redis with value from DB. They must be equal.
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='24H High Value Verification')
@allure.testcase(BaseConfig.GITLAB_URL +
                 "/ticker_tests/C8194_24h_high_value_verification_test.py",
                 "Test24HHighVerification")
@pytest.mark.incremental
@pytest.mark.usefixtures("r_time_count", )
@pytest.mark.ticker
@pytest.mark.functional
class Test24HHighVerification(object):
    redis_24_h_high = None
    max_price = None
    date_24_hours_ago = None

    @allure.step("Starting with: test_get_redis_24_h_high")
    @automation_logger(logger)
    def test_get_redis_24_h_high(self):
        Test24HHighVerification.redis_24_h_high = RedisDb.get_ticker_high_24(instrument_id)
        assert self.redis_24_h_high is not None

    @allure.step("Proceed with: test_get_date_24_hours_ago")
    @automation_logger(logger)
    def test_get_date_24_hours_ago(self):
        Test24HHighVerification.date_24_hours_ago = datetime.utcnow() + timedelta(days=-1)
        assert self.date_24_hours_ago is not None

    @allure.step("Proceed with: test_get_max_price_last_24_hours")
    @automation_logger(logger)
    def test_get_max_price_last_24_hours(self):
        data_now = datetime.utcnow()
        total_quantity_query = ("SELECT max(price) FROM trades_crypto WHERE instrumentId= '"
                                + str(instrument_id) + "'AND executionDate between '" +
                                str(self.date_24_hours_ago) + "' and '" + str(data_now) + "'")
        Test24HHighVerification.max_price = (Instruments.run_mysql_query(total_quantity_query)[0][0])
        if self.max_price is None:
            Test24HHighVerification.max_price = float(
                SqlDb.run_mysql_query("SELECT price FROM trades_crypto WHERE instrumentId =" + str(
                    instrument_id) + " ORDER BY executionDate  DESC limit 1;")[0][0])
        assert self.max_price is not None

    @allure.step("Proceed with: test_compare_24_h_high")
    @automation_logger(logger)
    def test_compare_24_h_high(self):
        assert self.redis_24_h_high == round(self.max_price, 2)
        logger.logger.info("redis_24h_high {0} == max_price {1}".format(self.redis_24_h_high, round(self.max_price, 2)))
        logger.logger.info("Test {0}".format(test_case))
        logger.logger.info("==================== TEST IS PASSED ====================")
