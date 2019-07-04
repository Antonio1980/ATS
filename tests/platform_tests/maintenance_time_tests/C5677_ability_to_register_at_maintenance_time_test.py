import allure
import pytest
import unittest
from src.base import logger
from config_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.customer.customer import Customer
from src.base.log_decorator import automation_logger

test_case = '5677'


@allure.title("Maintenance Time")
@allure.description("""
    Ability to Registration during Maintenance time, API
    1. Get me-state 
    2. Verify that me-state equal 2 (Maintenance time)
    3. Register new customer
    4. Verify that registered customer has "registrationStep" equal 8 in DB
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Ability to Registration during Maintenance time')
@allure.testcase(
    BaseConfig.GITLAB_URL +
    "/maintenance_time_tests/C5677_ability_to_register_at_maintenance_time_test.py",
    "TestAbilityToRegisterDuringMaintenanceTime")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.maintenance_time
class TestAbilityToRegisterDuringMaintenanceTime(unittest.TestCase):
    @automation_logger(logger)
    @allure.step("SetUp: set new customer and get me-state.")
    def setUp(self):
        self.customer = Customer()
        self.state_me = Instruments.get_me_state()

    @automation_logger(logger)
    @allure.step("Starting with: test_ability_to_register_during_maintenance_time")
    def test_ability_to_register_during_maintenance_time(self):
        assert self.state_me == 2
        self.customer.customer_registration()
        verification_of_customer = Instruments.run_mysql_query(
            "SELECT registrationStep FROM customers WHERE id = " + str(self.customer.customer_id) + ";")[0][0]
        assert verification_of_customer == 8
        logger.logger.info("Test {0}, with CustomerID {1}".format(test_case, self.customer.customer_id))
        logger.logger.info("==================== TEST IS PASSED ====================")
