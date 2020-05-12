import allure
import pytest
from src.base import logger
from src.base.log_decorator import automation_logger

test_case = "7497"


@pytest.mark.skip
@pytest.mark.usefixtures("r_time_count", "r_customer", )
@pytest.mark.fiat
class TestDepositSuccessfullyConfirmed(object):
    @allure.step("")
    @automation_logger(logger)
    def test_deposit_successfully_confirm(self, r_customer):
        logger.logger.info("TEST CASE N: {0}".format(test_case))
        logger.logger.info("method test_validate_redis_auth_token")
        _response = r_customer.postman.payment_service.add_credit_card(r_customer.credit_card)
        assert _response['error'] is None
        log_in_response = r_customer.postman.authorization_service.login_by_credentials(r_customer.email,
                                                                                           r_customer.password)
        assert log_in_response['error'] is None
        assert isinstance(log_in_response['result']['token'], str)
        r_customer.auth_token = log_in_response['result']['token']
        logger.logger.info("=============== TEST CASE - {0} IS PASSED !!! ===============".format(test_case))
