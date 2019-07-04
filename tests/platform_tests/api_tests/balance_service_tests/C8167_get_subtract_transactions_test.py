import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger

test_case = "8167"
currency_id = 3
amount = 0.1


@allure.feature("Balance")
@allure.story("Ability to ")
@allure.title("GET SUBTRACT TRANSACTIONS")
@allure.description("""
    Functional api test.
    Coverage:

    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='Get Substract Transactions')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/balance_service_tests/C8167_get_subtract_transactions_test.py",
                 "TestGetSubtractTransactions")
@pytest.mark.usefixtures("r_time_count", "r_customer")
@pytest.mark.balance
@pytest.mark.regression
@pytest.mark.balance_service
class TestGetSubtractTransactions(object):

    @allure.step("Starting with: ")
    @automation_logger(logger)
    def test_get_subtract_transactions_method_works(self, r_customer):
        subtract_transactions = r_customer.postman.balance_service.get_subtract_transactions(r_customer.customer_id,
                                                                                             currency_id)
        assert isinstance(subtract_transactions['result'], dict)
        assert subtract_transactions['result']['customerId'] == r_customer.customer_id
        assert subtract_transactions['result']['currencyId'] == currency_id
        assert isinstance(subtract_transactions['result']['subtractTransactions'], list)
        
        logger.logger.info("================== TEST CASE PASSED ===================".format(test_case))

    @allure.step("")
    @automation_logger(logger)
    @pytest.mark.parametrize('add_balance', [[currency_id, amount]], indirect=True)
    def test_get_subtract_transactions_functional(self, add_balance):
        sub_transaction = add_balance.postman.balance_service.subtract_transaction_initialize(add_balance.customer_id,
                                                                                             currency_id, 0.0015)
        assert sub_transaction['result']['customerId'] == add_balance.customer_id
        assert sub_transaction['result']['currencyId'] == currency_id

        subtract_transactions = add_balance.postman.balance_service.get_subtract_transactions(add_balance.customer_id,
                                                                                             currency_id)
        assert len(subtract_transactions['result']['subtractTransactions']) > 0
