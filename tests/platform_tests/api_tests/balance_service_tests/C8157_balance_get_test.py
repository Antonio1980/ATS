import allure
import pytest
from src.base import logger
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger
from config_definitions import BaseConfig

test_case = "8157"

"""
To verify "get balance for all currencies" method we are registering a new customer.
We exepect that total, available and frozen balance for each currency will be zero,
and we can use it to verify the "get balance" and "get all balance" methods.
"""


@allure.feature("Balance")
@allure.story("Ability to frozen balance for the given account per customer_id, currency and amount.")
@allure.title("Get BALANCE")
@allure.description("""
    Functional api test.
    Coverage:
    balance_service, balance, api
    1. Get All Currencies balance.
    2. Get balance for given currency .
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='API BASE URL')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/balance_service_tests/C8157_balance_get_test.py",
                 "Get Balance")
@pytest.mark.usefixtures("r_customer")
class TestBalanceGet(object):
    joe = None

    joe_token = ""

    currencies = []

    @allure.step("Get All Currencies balance.")
    @automation_logger(logger)
    def test_create_customers(self, r_customer):
        # Creating a new customer
        test_customers = Instruments.create_two_customers(1)

        # Saving the customer and his authorization tokens to class variables.
        TestBalanceGet.joe = test_customers[0][0]
        TestBalanceGet.joe_token = test_customers[0][1]

    def test_verifying_get_all_currencies(self):
        balance_response = TestBalanceGet.joe.postman.get_static_postman(TestBalanceGet.joe_token) \
            .balance_service.get_all_currencies_balance(TestBalanceGet.joe.customer_id)

        for currency in balance_response['result']:
            assert float(currency['balance']['total']) == 0
            assert float(currency['balance']['frozen']) == 0
            assert float(currency['balance']['available']) == 0
            assert str(currency['customerId']) == TestBalanceGet.joe.customer_id
            TestBalanceGet.currencies.append(currency['currencyId'])

    @allure.step("Get balance for given currency.")
    @automation_logger(logger)
    def test_verifying_balance_get(self):

        for currency in TestBalanceGet.currencies:
            balance_response = TestBalanceGet.joe.postman.get_static_postman(TestBalanceGet.joe_token) \
                .balance_service.get_currency_balance(TestBalanceGet.joe.customer_id, currency)

            assert float(balance_response['result']['balance']['total']) == 0
            assert float(balance_response['result']['balance']['frozen']) == 0
            assert float(balance_response['result']['balance']['available']) == 0
            assert str(balance_response['result']['customerId']) == TestBalanceGet.joe.customer_id

        logger.logger.info(f"================== TEST CASE PASSED: {test_case}===================")
        print(f"================== TEST CASE PASSED: {test_case}===================")
