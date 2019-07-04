import allure
import pytest
from src.base import logger
from src.base.log_decorator import automation_logger
from config_definitions import BaseConfig

test_case = "8193"
test_currency = 1
decimal_sum = 11.111111111111111

"""
In this test we are verifying that the amount of digits after the decimal point of frozen/unfrozen sum is equal
in the request that is sent to Balance Service and in Balance Service.
"""


@allure.feature("Balance")
@allure.story("Balance Service - tail digits verified.")
@allure.title("Unfreeze Balance - Negative")
@allure.description("""
    Functional api test.
    Coverage:
    balance_service, balance, api
    1. Add 100 to available balance.
    2. Perfrom freeze operation on the decimal sum.
    3. Perfrom unfreeze operation on the decimal sum.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='API BASE URL')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/balance_service_tests/C8193_tail_digits_test.py",
                 "Unfreeze Balance - Negative")
@pytest.mark.usefixtures("r_customer")
class TestUnfreezeAmountNegative(object):

    freeze_transaction_id = ""
    test_customer_balance_available = ""
    test_customer_balance_frozen = ""

    @allure.step("Add 100 to available balance.")
    @automation_logger(logger)
    def test_add_balance(self, r_customer):
        r_customer.postman.balance_service.add_balance(r_customer.customer_id, test_currency, 100)

        response = r_customer.postman.balance_service.get_currency_balance(r_customer.customer_id, test_currency)
        assert float(response['result']['balance']['available']) >= 0

        TestUnfreezeAmountNegative.test_customer_balance_available = \
            float(response['result']['balance']['available'])
        TestUnfreezeAmountNegative.test_customer_balance_frozen = \
            float(response['result']['balance']['frozen'])

        logger.logger.info(
            F"Customer's balance available in test currency - response: "
            F"{TestUnfreezeAmountNegative.test_customer_balance_available}")
        print(
            F"Customer's  available balance in test currency - response: "
            F"{TestUnfreezeAmountNegative.test_customer_balance_available}")

    @allure.step("Perfrom freeze operation on the decimal sum.")
    @automation_logger(logger)
    def test_freeze_sum(self, r_customer):
        response = r_customer.postman.balance_service. \
            subtract_transaction_initialize(r_customer.customer_id, test_currency, decimal_sum)

        print(f"Freeze response {response}")
        logger.logger.info(f"Freeze response {response}")

        TestUnfreezeAmountNegative.freeze_transaction_id = response['result']['transactionGuid']
        assert len(TestUnfreezeAmountNegative.freeze_transaction_id) > 0

        response = r_customer.postman.balance_service.get_currency_balance(r_customer.customer_id, test_currency)

        assert float(response['result']['balance']['frozen']) == TestUnfreezeAmountNegative.\
            test_customer_balance_frozen + decimal_sum

        logger.logger.info(f"Decimal sum frozen - service response: {response}")
        print(f"Decimal sum frozen - service response: {response}")

    @allure.step("Perfrom unfreeze operation on the decimal sum.")
    @automation_logger(logger)
    def test_unfreeze_sum(self, r_customer):
        response = r_customer.postman.balance_service.subtract_transaction_partial_commit(
            TestUnfreezeAmountNegative.freeze_transaction_id, r_customer.customer_id, test_currency,
            decimal_sum)

        logger.logger.info(f"Decimal sum - unfrozen and removed: {response}")
        print(f"Decimal sum - unfrozen and removed: {response}")

        response = r_customer.postman.balance_service.get_currency_balance(r_customer.customer_id, test_currency)

        assert float(response['result']['balance']['frozen']) == TestUnfreezeAmountNegative.test_customer_balance_frozen
        assert float(response['result']['balance']['total']) == TestUnfreezeAmountNegative.test_customer_balance_frozen + TestUnfreezeAmountNegative.test_customer_balance_available - decimal_sum
        assert float(response['result']['balance']['available']) == TestUnfreezeAmountNegative.test_customer_balance_available - decimal_sum
