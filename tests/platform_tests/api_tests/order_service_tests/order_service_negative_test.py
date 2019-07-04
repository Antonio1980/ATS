import json
import allure
import pytest
from src.base import logger
from src.base.customer.customer import Customer
from src.base.equipment.order import Order
from src.base.log_decorator import automation_logger
from config_definitions import BaseConfig

instrument_id = 1007
currency_id = 1
order_price = 100
order_quantity = 2
# An external ID of an existing order used for negative testing
externalOrderId = "0-AAAAAAAAAGE="

test_case = "order_service_negative"


@allure.feature("Order Management")
@allure.title("ORDER SERVICE API: NEGATIVE")
@allure.description("""
    Sanity API test.
    Coverage:
    order_service, public_api
    1 Verifies unregistered customer can't get information on open orders.
    2 Verifies unregistered customer can't get information on orders history.
    3 Verifies unregistered customer can't get information on trades history.
    4 Verifies unregistered customer can't place an order.
    5 Verifies unregistered customer can't cancel an existing order.
    6 Verifies registered customer can't place an order without enough assets on his available balance.
       """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/order_service_tests/order_service_negative_test.py",
                 "TestOrderNegative")
@pytest.mark.usefixtures("r_time_count", "r_customer")
@pytest.mark.regression
@pytest.mark.order_service
@pytest.mark.order_management
class TestOrderNegative(object):

    @pytest.fixture
    @automation_logger(logger)
    def another_customer(self):
        customer = Customer()
        return customer

    limit_buy_btc = Order().set_order(1, instrument_id, order_quantity, order_price)

    @allure.step("Verifying that newly created customer with empty balance can't place an order")
    @automation_logger(logger)
    def test_balance_required_for_trade(self, r_customer):
        initial_balance = r_customer.postman.p_balance_service.get_balance(currency_id)
        logger.logger.info(initial_balance)
        logger.logger.info(r_customer.customer_id)
        available_balance = initial_balance['result']['balance']['1']['available']

        # Removing available balance - if required.
        r_customer.postman.balance_service.subtract_balance(r_customer.customer_id, currency_id,
                                                            available_balance)

        order_response = r_customer.postman.order_service.create_order_sync(TestOrderNegative.limit_buy_btc)

        assert order_response['result'] is None
        error_report = json.loads(order_response['error'])

        assert int(error_report['type']) == 2
        assert error_report['term'] == "balance_freezing.freezing validation.balance_freeze"
        assert error_report['details'] == "error freezing balance"
        incident_id = str(error_report['incident_id'])
        assert len(incident_id) > 0

        logger.logger.info(F"Insufficient balance error message - verified .")

    @allure.step("Verifying  unregistred customer can't place or cancel an order")
    @automation_logger(logger)
    def test_authorization_required_create_order(self, another_customer):
        order_response = another_customer.postman.order_service.create_order_sync(TestOrderNegative.limit_buy_btc)
        assert order_response['error'] == "forbidden"

        # Verifying that unregistred customer can't cancel order
        order_response_cancel = another_customer.postman.order_service.cancel_order("0-AAAAAAAAAGE=")
        assert order_response_cancel['error'] == "forbidden"

        logger.logger.info(F"Unregistred customer can't place or cancel an order - verified")

    @allure.step("Comes to verify that unregistered customer can't get private information from Order Service")
    @automation_logger(logger)
    def test_registration_required_get_data(self, another_customer):
        # Verifying that unregistred customer can't get data on open orders
        open_orders = another_customer.postman.order_service.get_open_orders()

        assert open_orders['error'] == "forbidden"
        export_orders = another_customer.postman.order_service.export_open_orders()
        assert export_orders['error'] == "forbidden"

        # Verifying that unregistred customer can't get data on orders history
        orders_history = another_customer.postman.order_service.get_order_history(1)
        assert orders_history['error'] == "forbidden"
        orders_history = another_customer.postman.order_service.get_order_history(2)
        assert orders_history['error'] == "forbidden"

        # Verifying that unregistred customer can't get data on trade history
        trade_history = another_customer.postman.order_service.get_trades_history(1)
        assert trade_history['error'] == "forbidden"
        trade_history = another_customer.postman.order_service.get_trades_history(2)
        assert trade_history['error'] == "forbidden"

        export_trades = another_customer.postman.order_service.export_trades_history(1)
        assert export_trades['error'] == "forbidden"
        export_trades = another_customer.postman.order_service.export_trades_history(2)
        assert export_trades['error'] == "forbidden"

        logger.logger.info(F"Unregistered customer can't get private information from Order Service - verified")

        logger.logger.info(F"---------------TEST CASE {test_case} PASSED!--------------")
