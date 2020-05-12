import pytest
import allure
from src.base import logger
from config_definitions import BaseConfig
from src.base.data_bases.redis_db import RedisDb
from src.base.log_decorator import automation_logger

test_case = ""
currency_id = 2
amount = 10000

@allure.feature("Balance")
@allure.story("Ability to ")
@allure.title("ENSURE IN REDIS")
@allure.description("""
    Functional api test.
    Coverage:

    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='Ensure In Redis')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/balance_service_tests/ensure_in_redis_test.py", "TestEnsureInRedis")
@pytest.mark.usefixtures("r_time_count", "r_customer")
@pytest.mark.balance
@pytest.mark.regression
@pytest.mark.balance_service
class TestEnsureInRedis(object):

    @allure.step("Starting with: ")
    @automation_logger(logger)
    def test_ensure_in_redis_method_works(self, r_customer):
        ensure_response = r_customer.postman.balance_service.ensure_in_redis(r_customer.customer_id)
        assert ensure_response['result'] is True
        logger.logger.info("================== TEST CASE PASSED ===================".format(test_case))

    @allure.step("Starting with: ")
    @automation_logger(logger)
    @pytest.mark.parametrize('add_balance', [[currency_id, amount]], indirect=True)
    def test_ensure_in_redis_functional(self, r_customer, add_balance):
        total_key = "balance_{" + str(r_customer.customer_id) + "}"
        frozen_key =  "frozen_balance_{" + str(r_customer.customer_id) + "}"

        total_balance_before = RedisDb.get_hash_key_value(total_key, currency_id)
        frozen_balance_before = RedisDb.get_hash_key_value(frozen_key, currency_id)

        RedisDb.delete_redis_key(total_key)
        RedisDb.delete_redis_key(frozen_key)

        cur_total_balance = RedisDb.get_hash_key_value(total_key, currency_id)
        cur_frozen_balance = RedisDb.get_hash_key_value(frozen_key, currency_id)

        assert cur_total_balance is None
        assert cur_frozen_balance is None

        ensure_response = r_customer.postman.balance_service.ensure_in_redis(r_customer.customer_id)
        assert ensure_response['result'] is True

        total_balance_after = RedisDb.get_hash_key_value(total_key, currency_id)
        frozen_balance_after = RedisDb.get_hash_key_value(frozen_key, currency_id)

        assert total_balance_before == total_balance_after
        assert frozen_balance_before == frozen_balance_after

        logger.logger.info("================== TEST CASE PASSED ===================".format(test_case))
