import time
import pytest
from src.base import logger
from src.base.equipment.order import Order
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger

delay = 60.0
currency_id = 3
instrument_id = 1012


@pytest.mark.incremental
@pytest.mark.usefixtures('r_time_count', 'r_customer')
@pytest.mark.balance
@pytest.mark.functional
@pytest.mark.trading_sanity
class TestBalanceAfterOrderSellCancelled(object):
    frozen_quoted_before, available_quoted_before, total_quoted_before = None, None, None
    internal_id = None

    @automation_logger(logger)
    def test_clean_instrument(self, r_customer):
        r_customer.clean_instrument(instrument_id)
        r_customer.clean_up_customer()

    @automation_logger(logger)
    def test_add_customer_deposit(self, r_customer):
        balance_response = r_customer.postman.balance_service.add_balance(r_customer.customer_id, currency_id, 10.0)
        logger.logger.info("Balance GUID: {0}".format(balance_response['result']['transactionGuid']))
        assert balance_response['result']['transactionGuid']

    @automation_logger(logger)
    def test_get_customer_balance(self, r_customer):
        balance_before_order = r_customer.postman.p_balance_service.get_balance(currency_id)
        assert balance_before_order['error'] is None
        TestBalanceAfterOrderSellCancelled.frozen_quoted_before = float(balance_before_order['result']['balance'][str(
            currency_id)]['frozen'])
        TestBalanceAfterOrderSellCancelled.available_quoted_before = float(
            balance_before_order['result']['balance'][str(
                currency_id)]['available'])
        TestBalanceAfterOrderSellCancelled.total_quoted_before = float(balance_before_order['result']['balance'][str(
            currency_id)]['total'])

    @automation_logger(logger)
    def test_create_order_sell(self, r_customer):
        price = Instruments.get_price_last_trade(instrument_id)
        limit_sell = Order().set_order(2, instrument_id, 1, price)
        order_response = r_customer.postman.order_service.create_order_sync(limit_sell)
        assert order_response['error'] is None
        TestBalanceAfterOrderSellCancelled.internal_id = order_response['result']['orderId']

    @automation_logger(logger)
    def test_order_in_open_orders(self, r_customer):
        time.sleep(5.0)
        open_orders = r_customer.postman.order_service.get_open_orders()
        assert open_orders['error'] is None
        assert isinstance(open_orders['result']['orders'], list)
        TestBalanceAfterOrderSellCancelled.internal_id_open = open_orders['result']['orders'][-1]['id']
        assert self.internal_id == TestBalanceAfterOrderSellCancelled.internal_id_open

    @automation_logger(logger)
    def test_cancel_opened_order(self, r_customer):
        cancel_response = r_customer.postman.order_service.cancel_order(self.internal_id)
        assert cancel_response['error'] is None

    @automation_logger(logger)
    def test_check_order_not_in_open_orders(self, r_customer):
        time.sleep(5.0)
        open_orders = r_customer.postman.order_service.get_open_orders()
        assert open_orders['error'] is None
        orders = open_orders['result']['orders']
        if isinstance(orders, list):
            for order in orders:
                assert int(self.internal_id) != int(order['id'])

    @automation_logger(logger)
    def test_check_order_in_order_history(self, r_customer):
        time.sleep(5.0)
        order_history = r_customer.postman.order_service.get_order_history()
        assert order_history['error'] is None
        assert isinstance(order_history['result']['ordersForHistory'], list)
        assert self.internal_id == order_history['result']['ordersForHistory'][0]['order']['id']

    @automation_logger(logger)
    def test_check_balance_after_all(self, r_customer):
        balance_after = r_customer.postman.p_balance_service.get_balance(currency_id)
        assert balance_after['error'] is None
        frozen_delay = time.perf_counter() + delay
        frozen_quoted_after = float(balance_after['result']['balance'][str(currency_id)]['frozen'])
        while self.frozen_quoted_before != frozen_quoted_after and time.perf_counter() <= frozen_delay:
            frozen_quoted_after = r_customer.postman.p_balance_service.get_balance(currency_id)['result']['balance'][
                str(currency_id)]['frozen']
        assert self.frozen_quoted_before == frozen_quoted_after
        assert self.total_quoted_before == float(balance_after['result']['balance'][
                                                     str(currency_id)]['total'])
        assert self.available_quoted_before == float(balance_after['result']['balance'][
                                                         str(currency_id)]['available'])
        logger.logger.info("================== TEST CASE IS PASSED ===================")
