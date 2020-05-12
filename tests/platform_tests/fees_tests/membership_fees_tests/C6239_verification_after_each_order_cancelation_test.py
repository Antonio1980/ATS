import time
import allure
import arrow
import pytest
from src.base import logger
from src.base.equipment.order import Order
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger

test_case = "6239"
currency_id = 1
c_currency_id = 4
instrument_id = 1008


@pytest.mark.fee
@pytest.mark.membership_fee
@pytest.mark.usefixtures("r_time_count", "r_customer_sql", "fee_cleanup")
class TestVerifyFeeAfterEachOrder(object):

    @allure.step("test_verify_fee_after_each_order")
    @automation_logger(logger)
    @pytest.mark.parametrize('safe_price', [[instrument_id]], indirect=True)
    @pytest.mark.parametrize('preconditions', [[currency_id, c_currency_id]], indirect=True)
    def test_verify_fee_after_each_order(self, r_customer_sql, preconditions, safe_price):

        quantity1 = round((100 / preconditions), 4)
        order1 = r_customer_sql.postman.order_service.create_order_sync(
            Order().set_order(2, instrument_id, quantity1, safe_price))

        quantity2 = round((300 / preconditions), 4)
        order2 = r_customer_sql.postman.order_service.create_order_sync(
            Order().set_order(2, instrument_id, quantity2, safe_price))

        quantity3 = round((400 / preconditions), 4)
        order3 = r_customer_sql.postman.order_service.create_order_sync(
            Order().set_order(2, instrument_id, quantity3, safe_price))

        quantity4 = round((600 / preconditions), 4)
        order4 = r_customer_sql.postman.order_service.create_order_sync(
            Order().set_order(2, instrument_id, quantity4, safe_price))

        assert order1['error'] is None
        assert order2['error'] is None
        assert order3['error'] is None
        assert order4['error'] is None

        balance_response = r_customer_sql.postman.balance_service.get_currency_balance(r_customer_sql.customer_id,
                                                                                   c_currency_id)
        available_balance = float(balance_response['result']['balance']['available'])
        subtract_response = r_customer_sql.postman.balance_service.subtract_balance(
            r_customer_sql.customer_id, c_currency_id, available_balance)
        assert float(subtract_response['result']['balance']['available']) == 0.0

        next_process_date = arrow.get().shift(days=-1).format('YYYY-MM-DD HH:mm:ss')
        next_query = f"UPDATE fee_scheduler SET nextProcessDate = '{next_process_date}' WHERE customerId = {r_customer_sql.customer_id};"
        Instruments.run_mysql_query(next_query)

        assert Instruments.restart_pod("membership-fee-service")
        time.sleep(5.0)
        
        check_fee_query = f"SELECT isActive, remainingFee FROM fee_scheduler WHERE customerId={r_customer_sql.customer_id};"
        fee_result = Instruments.run_mysql_query(check_fee_query)[0]
        customer_status = fee_result[0]
        customer_fee = float(fee_result[1])
        assert customer_fee == 0.0, f"Customers fee != 0.0 - current is {customer_fee}"

        check_orders_query = f"SELECT statusId FROM orders WHERE customerId = {r_customer_sql.customer_id} ;"
        time.sleep(5.0)
        orders_result = Instruments.run_mysql_query(check_orders_query)
        results = [row[0] for row in orders_result]

        assert customer_status == 1, f"Customer status is changed - {customer_status}"
        assert results[0] == 2 and results[1] == 2 and results[2] == 2 and results[3] == 1, "Order status isn't changed"
