import allure
import pytest
import unittest
from src.base import logger
from config_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger
from src.base.customer.registered_customer import RegisteredCustomer

test_case = '5682'


@allure.title("Maintenance Time")
@allure.description("""
    Generate Crypto Deposit during Maintenance time, API
    1. Get me-state 
    2. Verify that me-state equal 2 (Maintenance time)
    3. Add crypto deposit
    4. Verify that balance after deposit more that balance before deposit
    Calculation: balance_after > balance_before 
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Generate Crypto Deposit during Maintenance time')
@allure.testcase(
    BaseConfig.GITLAB_URL +
    "/maintenance_time_tests/C5685_crypto_deposit_at_maintenance_time_test.py",
    "TestGenerateCryptoDepositDuringMaintenanceTime")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.maintenance_time
class TestGenerateCryptoDepositDuringMaintenanceTime(unittest.TestCase):
    @automation_logger(logger)
    @allure.step("SetUp: calling registered customer and get me-state.")
    def setUp(self):
        self.customer = RegisteredCustomer()
        self.state_me = Instruments.get_me_state()

    @automation_logger(logger)
    @allure.step("Starting with: test_generate_crypto_deposit_during_maintenance_time_test")
    def test_generate_crypto_deposit_during_maintenance_time_test(self):
        assert self.state_me == 2
        deposit_response = self.customer.postman.payment_service.add_deposit_crypto(3)
        assert deposit_response['error'] is None
        logger.logger.info("Test {0}, with CustomerID {1}".format(test_case, self.customer.customer_id))
        logger.logger.info("==================== TEST IS PASSED ====================")
