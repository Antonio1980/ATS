import time
import pytest
from src.base import logger
from src.base.utils.k8s import Kubernetes
from src.base.equipment.order import Order
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger


@pytest.fixture(scope="class")
@automation_logger(logger)
def set_cumulative_fee_first_step(customer):
    assert Instruments.set_cumulative_fee_dxchash_disabled(7, 10000.0, 0.05)
    assert Instruments.set_cumulative_fee_dxchash_disabled(8, 100000.0, 0.10)
    assert Kubernetes.restart_pod('cumulative')
    time.sleep(5.0)


@pytest.fixture(scope="class")
@automation_logger(logger)
def set_cumulative_fee_second_step(customer):
    assert Instruments.set_cumulative_fee_dxchash_disabled(7, 0.0, 0.00)
    assert Instruments.set_cumulative_fee_dxchash_disabled(8, 100000.0, 0.10)
    assert Kubernetes.restart_pod('cumulative')
    time.sleep(5.0)


@pytest.fixture(scope="class")
@automation_logger(logger)
def precondition_cumulative(request, r_customer_sql):
    a = r_customer_sql.customer_id
    if hasattr(request, 'param'):
        quoted_currency_id = request.param[0]
        base_currency_id = request.param[1]
        instrument_id = request.param[2]
        response_credit_card = r_customer_sql.add_credit_card_and_deposit(1500.0, quoted_currency_id)
        assert response_credit_card is not None

        time.sleep(2.0)

        r_customer_sql.clean_instrument(instrument_id)
        r_customer_sql.clean_up_customer()

        price = Instruments.get_price_last_trade(instrument_id)
        amount = 2

        r_customer_sql.postman.balance_service.add_balance(int(r_customer_sql.customer_id), quoted_currency_id, 50000)
        r_customer_sql.postman.balance_service.add_balance(int(r_customer_sql.customer_id), base_currency_id, amount)

        get_balance_quoted_currency_id = r_customer_sql.postman.balance_service.get_currency_balance(
            r_customer_sql.customer_id, quoted_currency_id)
        total_quoted_before = float(get_balance_quoted_currency_id['result']['balance']['total'])
        available_quoted_before = float(get_balance_quoted_currency_id['result']['balance']['available'])
        frozen_quoted_before = float(get_balance_quoted_currency_id['result']['balance']['frozen'])

        get_balance_base_currency_id = r_customer_sql.postman.balance_service.get_currency_balance(
            r_customer_sql.customer_id, base_currency_id)
        total_base_before = float(get_balance_base_currency_id['result']['balance']['total'])
        available_base_before = float(get_balance_base_currency_id['result']['balance']['available'])
        frozen_base_before = float(get_balance_base_currency_id['result']['balance']['frozen'])

        order_limit_sell = Order().set_order(2, instrument_id, amount, price)
        order_response_sell = r_customer_sql.postman.order_service.create_order_sync(order_limit_sell)
        assert order_response_sell['error'] is None
        order_id_sell = order_response_sell['result']['orderId']
        time.sleep(5.0)

        order_limit_buy = Order().set_order(1, instrument_id, amount, price)
        order_response_buy = r_customer_sql.postman.order_service.create_order_sync(order_limit_buy)
        assert order_response_buy['error'] is None
        order_id_buy = order_response_buy['result']['orderId']
        time.sleep(5.0)

        data = {
            'price': price,
            'amount': amount,
            'balance': {'total_quoted_before': total_quoted_before,
                        'available_quoted_before': available_quoted_before,
                        'frozen_quoted_before': frozen_quoted_before,
                        'total_base_before': total_base_before,
                        'available_base_before': available_base_before,
                        'frozen_base_before': frozen_base_before
                        },
            'order_id': {'order_id_sell': order_id_sell,
                         'order_id_buy': order_id_buy
                         }
        }
        return data
