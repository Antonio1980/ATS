import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger

test_case = "Session Data"

@pytest.mark.incremental
@allure.title("SESSION DATA")
@allure.description("""
    Sanity tests.
    1. Verify that valid session data is received 
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/authorization_service_tests/session_data_test.py",
                 "TestGetSessionData")
@pytest.mark.usefixtures("r_time_count", "customer")
@pytest.mark.regression
@pytest.mark.authorization
@pytest.mark.authorization_service
class TestGetSessionData(object):

    @allure.step("Log in")
    @automation_logger(logger)
    def test_get_session_data(self, customer):
        response = customer.postman.authorization_service.get_session_data()
        assert response['error'] is None
        assert response['result']['meEnabled'] is True

        assert isinstance(response['result'], dict)
        assert isinstance(response['result']['geo'], dict)
        assert isinstance(response['result']['geo']['ip'], str)
        assert  len(response['result']['geo']['ip']) > 0
        assert isinstance(response['result']['geo']['phonePrefix'], int)
        assert isinstance(response['result']['geo']['id'], int)
        assert isinstance(response['result']['geo']['name'], str)

        assert isinstance(response['result']['time'], dict)
        assert isinstance(response['result']['time']['serverTime'], int)
        assert response['result']['time']['serverTime'] > 0
        assert isinstance(response['result']['time']['timeZone'], str)
        assert len(response['result']['time']['timeZone']) == 3
        assert isinstance(response['result']['time']['timeZoneOffset'], int)
        logger.logger.info(F"---------------TEST CASE {test_case} PASSED!--------------")
