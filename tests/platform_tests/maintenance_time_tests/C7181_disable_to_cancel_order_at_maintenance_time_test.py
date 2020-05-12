import allure
import pytest
import unittest
from src.base import logger
from config_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger
from src.base.customer.registered_customer import RegisteredCustomer

test_case = '7181'


@allure.title("Maintenance Time")
@allure.description("""
    Verification of some elements exist at the screen during maintenance time, UI test
    1. Get me-state 
    2. Verify that me-state equal 2 (Maintenance time)
    3. Get Open order from DB
    4. Define Customer of Open order
    5. Cancel Open Order 
    6. Verify that there is  no ability to cancel order.
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='End of Day Maintenance message at the Web Platform')
@allure.testcase(
    BaseConfig.GITLAB_URL + "/maintenance_time_tests/C5674_end_of_day_maintenance_message_presented_test.py",
    "TestNoAbilityToCancelOrderDuringMaintenanceTime")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.maintenance_time
class TestNoAbilityToCancelOrderDuringMaintenanceTime(unittest.TestCase):
    @automation_logger(logger)
    @allure.step("SetUp: get me-state.")
    def setUp(self):
        self.state_me = Instruments.get_me_state()

    @automation_logger(logger)
    @allure.step("Starting with: test_no_ability_to_cancel_order_during_maintenance_time")
    def test_no_ability_to_cancel_order_during_maintenance_time(self):
        assert self.state_me == 2
        data_query = Instruments.run_mysql_query(
            "SELECT orders.id, orders.customerId, customers.email FROM orders INNER JOIN order_types ON "
            "order_types.id = orders.typeId INNER JOIN customers ON orders.customerId = customers.id WHERE "
            "filledQuantity = 0 and orders.statusId = 1 and order_types.name = 'limit' and customers.email"
            " LIKE '%guerrilla%' OR customers.email LIKE '%gun%'")
        assert data_query
        customer_mail = data_query[0][2]
        customer_id = data_query[0][1]
        order_id = data_query[0][0]
        customer = RegisteredCustomer(None, customer_mail, '1Aa@<>12', customer_id)
        cancel_response = customer.postman.order_service.cancel_order(order_id)
        cancel_error = cancel_response['error']
        assert 'order_creation.matching_engine.trading_disabled' in cancel_error
        logger.logger.info("Test {0}, with CustomerID {1}".format(test_case, customer.customer_id))
        logger.logger.info("==================== TEST IS PASSED ====================")
