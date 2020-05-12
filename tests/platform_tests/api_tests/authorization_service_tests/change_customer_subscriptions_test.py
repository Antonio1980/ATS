import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.customer.customer import Customer
from src.base.log_decorator import automation_logger

test_case = "Change Customer Subscriptions"


@allure.title("CHANGE SUBSCRIPTIONS")
@allure.description("""
    Sanity tests.
    1. Verify that registered customer can update customer subscriptions
    2. Verify that unregistered customer can't update customer subscriptions
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/authorization_service_tests/change_customer_subscriptions_test.py",
                 "TestChangeSubscriptions")
@pytest.mark.usefixtures("r_customer", "r_time_count", )
@pytest.mark.regression
@pytest.mark.authorization
@pytest.mark.authorization_service
class TestChangeCustomerSubscription(object):

    @pytest.fixture
    @automation_logger(logger)
    def another_customer(self):
        customer = Customer()
        return customer

    @allure.step("Veifying that registred customer can change customer subscriptions")
    @automation_logger(logger)
    def test_registred_customer_subscriptions(self, r_customer):
        response = r_customer.postman.authorization_service.change_subscriptions(True, True, False)
        assert response['error'] is None

        logger.logger.info("Addressing the Trade Service to get the selected customer data")
        customer_data_response = r_customer.postman.trade_service.customer_data()

        logger.logger.info("Verifying the selected subscriptions")
        assert customer_data_response['result']['customer']['receivePromoSMS'] is True
        assert customer_data_response['result']['customer']['receivePromoPushToMobile'] is False
        assert customer_data_response['result']['customer']['receivePromoEmail'] is True

        print(F"Test print {response['error']}")
        logger.logger.info("Registred customer can change customer subscriptions - Verified")

    @allure.step("Verify that unregistered customer can't update customer subscriptions")
    @automation_logger(logger)
    def test_unregistered_customer_negative(self, another_customer):
        response = another_customer.postman.authorization_service.change_subscriptions(True, True, False)
        assert response['error'] == "forbidden"
        logger.logger.info("Unregistered customer can't update customer subscriptions - Verified")
        logger.logger.info(F"---------------TEST CASE {test_case} PASSED!--------------")
