import time
import pytest
from src.base import logger
from src.base.equipment.order import Order
from src.base.log_decorator import automation_logger

quoted_currency_id = 2
base_currency_id = 6
delay = 60.0


@pytest.mark.incremental
@pytest.mark.usefixtures('r_time_count', 'r_customer')
@pytest.mark.balance
@pytest.mark.functional
@pytest.mark.trading_sanity
class TestBalanceUnfrozenAfterTradeLessOrderPrice(object):
    test_case = ""
    # XRP/JPY
    instrument_id = 1014

    @pytest.mark.parametrize("cur_customer_balance", [[quoted_currency_id, base_currency_id]], indirect=True)
    @automation_logger(logger)
    def test_place_first_order(self, r_customer, cur_customer_balance):
        first_order = Order().set_order(2, self.instrument_id, 100, 60)
        order_response = r_customer.postman.order_service.create_order(first_order)
        logger.logger.info("1 Order: {0}".format(order_response))
        assert order_response['error'] is None
        assert order_response['result']['status'] is True

    @automation_logger(logger)
    def test_place_second_order(self, r_customer):
        second_order = Order().set_order(2, self.instrument_id, 80, 56)
        order_response = r_customer.postman.order_service.create_order(second_order)
        logger.logger.info("2 Order: {0}".format(order_response))
        assert order_response['error'] is None
        assert order_response['result']['status'] is True

    @automation_logger(logger)
    def test_place_third_order(self, r_customer):
        third_order = Order().set_order(1, self.instrument_id, 180, 60)
        order_response = r_customer.postman.order_service.create_order(third_order)
        logger.logger.info("3 Order: {0}".format(order_response))
        assert order_response['error'] is None
        assert order_response['result']['status'] is True

    @automation_logger(logger)
    def test_check_cur_customer_balance(self, r_customer, cur_customer_balance):
        cur_balance = r_customer.postman.p_balance_service.get_balance(quoted_currency_id)
        logger.logger.info(f"cur_customer_balance: {cur_customer_balance}")
        frozen_delay = time.perf_counter() + delay
        assert cur_balance['error'] is None
        frozen_quoted_after = float(cur_balance['result']['balance'][str(quoted_currency_id)]['frozen'])
        while cur_customer_balance != frozen_quoted_after or time.perf_counter() >= frozen_delay:
            frozen_quoted_after = float(r_customer.postman.p_balance_service.get_balance(
                quoted_currency_id)['result']['balance'][str(quoted_currency_id)]['frozen'])
        assert float(cur_customer_balance) == float(frozen_quoted_after)

        logger.logger.info("================== TEST CASE IS PASSED ===================")
