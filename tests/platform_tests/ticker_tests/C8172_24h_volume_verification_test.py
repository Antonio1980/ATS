import allure
import pytest
from datetime import datetime, timedelta
from config_definitions import BaseConfig
from src.base import logger
from src.base.data_bases.redis_db import RedisDb
from src.base.data_bases.sql_db import SqlDb
from src.base.log_decorator import automation_logger

test_case = "8172"


@allure.title("TICKER")
@allure.description(""".
    Verification  "Last Trade Price"
    1. Get value "Volume24" from Redis
    2. Get value "Volume24" from DB
    5. Compare volume from Redis with volume from DB. They must be equal.
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Volume 24 Verification')
@allure.testcase(BaseConfig.GITLAB_URL +
                 "/ticker_tests/C8172_24h_volume_verification_test.py",
                 "TestVolume24Verification")
@pytest.mark.incremental
@pytest.mark.usefixtures("r_time_count", )
@pytest.mark.ticker
@pytest.mark.functional
class TestVolume24Verification(object):
    redis_volume = None
    db_volume = None
    date_24_hours_ago = None
    instrument_id = None

    @allure.step("Proceed with: test_get_date_24_hours_ago")
    @automation_logger(logger)
    def test_get_date_24_hours_ago(self):
        TestVolume24Verification.date_24_hours_ago = datetime.utcnow() + timedelta(days=-1)
        assert self.date_24_hours_ago is not None

    def test_get_instrument_id_last_trade_24h(self):
        instrument_id_query = (
                "SELECT instrumentId FROM trades_crypto WHERE executionDate > '" + str(self.date_24_hours_ago)
                + "' AND direction='buy'")
        TestVolume24Verification.instrument_id = ((SqlDb.run_mysql_query(instrument_id_query))[0][0])
        # TestVolume24Verification.instrument_id = 1012
        if self.instrument_id is None:
            TestVolume24Verification.instrument_id = 1007
        assert self.instrument_id is not None

    @allure.step("Starting with: test_get_volume_redis")
    @automation_logger(logger)
    def test_get_volume_redis(self):
        TestVolume24Verification.redis_volume = RedisDb.get_ticker_volume_24(self.instrument_id)
        assert self.redis_volume is not None

    @allure.step("Proceed with: test_get_volume_db")
    @automation_logger(logger)
    def test_get_volume_db(self):
        total_quantity_query = ("SELECT sum(quantity*price) FROM trades_crypto WHERE instrumentId= '"
                                + str(self.instrument_id) + "'AND executionDate > '" +
                                str(self.date_24_hours_ago) + "'AND direction='buy'")
        TestVolume24Verification.db_volume = SqlDb.run_mysql_query(total_quantity_query)[0][0]
        if self.db_volume is None:
            TestVolume24Verification.db_volume = 0.0
        assert self.db_volume is not None

    @allure.step("Proceed with: test_compare_volume_24")
    @automation_logger(logger)
    def test_compare_volume_24(self):
        assert self.redis_volume == float(self.db_volume)
        logger.logger.info("Instrument Id {0}".format(self.instrument_id))
        logger.logger.info("redis_price {0} == db_price {1}".format(self.redis_volume, self.db_volume))
        logger.logger.info("Test {0}".format(test_case))
        logger.logger.info("==================== TEST IS PASSED ====================")
