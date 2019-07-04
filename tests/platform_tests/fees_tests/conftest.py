import time
import arrow
import pytest
from src.base import logger
from src.base.utils.k8s import Kubernetes
from src.base.equipment.order import Order
from src.base.instruments import Instruments
from src.base.utils.calculator import Calculator
from src.base.log_decorator import automation_logger


@pytest.fixture(scope="class")
@automation_logger(logger)
def preconditions(request, r_customer_sql):
    currency_id, c_currency_id = request.param[0], request.param[1] if request.param else None

    # Set membership fee to 1000 EUR for fee plan 2
    Instruments.run_mysql_query("UPDATE local_config SET VALUE = 1000 WHERE id = 10764 ;")

    # Turn-off DXCASH mode for customer
    update_customer_response = r_customer_sql.postman.customer_service.update_customer(False, True)
    assert update_customer_response['error'] is None

    # Adding credit card , calling PaymentServiceRequest.
    r_customer_sql.add_credit_card_and_deposit(250.0, currency_id)

    # customer_id, currency_id, deposit_amount, ref_number
    add_balance_response = r_customer_sql.postman.balance_service.add_balance(r_customer_sql.customer_id, c_currency_id,
                                                                              200.0)
    assert add_balance_response['result'] is not None

    convert_response = r_customer_sql.postman.obligation_service.convert_rate(c_currency_id, currency_id)
    rate_value = int(convert_response['result']['rates'][str(c_currency_id)]['value'])
    rate_precisions = int(convert_response['result']['rates'][str(c_currency_id)]['decimals'])
    return Instruments.calculate_from_decimals(rate_value, rate_precisions)


@pytest.fixture(scope="class")
@automation_logger(logger)
def fee_cleanup(request):
    def set_fee_back():
        Instruments.run_mysql_query("UPDATE local_config SET VALUE = 4 WHERE id = 10764 ;")

    request.addfinalizer(set_fee_back)


@pytest.fixture(scope="class")
@automation_logger(logger)
def preconditions_c6221(request, r_customer_sql):
    currency_id, fee_periodic_2 = request.param[0], request.param[1] if request.param else None

    # Adding the funds
    add_balance = r_customer_sql.postman.balance_service.add_balance(r_customer_sql.customer_id, currency_id, 500)

    total_before = float(add_balance['result']['balance']['total'])
    available_before = float(add_balance['result']['balance']['available'])
    frozen_before = float(add_balance['result']['balance']['frozen'])

    # Turn-off DXCASH mode for customer
    update_customer_response = r_customer_sql.postman.customer_service.update_customer(False, True)
    assert update_customer_response['error'] is None

    # Set membership fee to 200 EUR for fee plan 2
    Instruments.run_mysql_query("UPDATE local_config SET VALUE = " + fee_periodic_2 + " WHERE id = 10764 ;")

    # set the date the “nextProcessDate” to trigger fee deduction. Set the date to 24 h ago
    next_process_date = arrow.get().shift(days=-1).format('YYYY-MM-DD HH:mm:ss')
    assert next_process_date is not None
    last_process_date = arrow.get().shift(days=-30).format('YYYY-MM-DD HH:mm:ss')
    assert last_process_date is not None
    next_query = f"UPDATE fee_scheduler SET lastProcessDate = '{last_process_date}', " \
        f"nextProcessDate = '{next_process_date}', currentFeePlanId = 2, nextFeePlanId = 2 " \
        f" WHERE customerId = {r_customer_sql.customer_id}; "
    Instruments.run_mysql_query(next_query)

    # restart the PODS
    assert Kubernetes.restart_pod('membership-fee-service')
    time.sleep(30.0)
    assert Kubernetes.get_pods_by_name('membership-fee-service')
    data = {'balance': {'total_before': total_before,
                        'available_before': available_before,
                        'frozen_before': frozen_before,
                        }
            }
    return data


@pytest.fixture(scope="class")
@automation_logger(logger)
def preconditions_c6226(request, r_customer_sql):
    currency_id_default = request.param[0]
    currency_id_2 = request.param[1]
    fee_periodic_2 = request.param[2]
    add_amount_currency_default = request.param[3]
    add_amount_currency_2 = request.param[4]
    instrument_id = request.param[5]
    placed_order_id = request.param[6]
    rate_value = request.param[7]

    r_customer_sql.clean_instrument(instrument_id)
    r_customer_sql.clean_up_customer()

    add_balance_btc = r_customer_sql.postman.balance_service.add_balance(r_customer_sql.customer_id,
                                                                         3, 0.5)
    available_balance = float(add_balance_btc['result']['balance']['available'])
    assert available_balance == 0.5

    price = Instruments.get_ticker_last_price(instrument_id) * 1.5

    order_sell_btc = r_customer_sql.postman.order_service.create_order_sync(
        Order().set_order(2, instrument_id, available_balance, price))
    assert order_sell_btc['error'] is None
    placed_order_id = order_sell_btc['result']['orderId']

    # Adding the funds
    add_balance_currency_default = r_customer_sql.postman.balance_service.add_balance(r_customer_sql.customer_id,
                                                                                      currency_id_default,
                                                                                      add_amount_currency_default)

    total_currency_default_before = float(add_balance_currency_default['result']['balance']['total'])
    available_currency_default_before = float(add_balance_currency_default['result']['balance']['available'])
    frozen_currency_default_before = float(add_balance_currency_default['result']['balance']['frozen'])

    add_balance_currency_2 = r_customer_sql.postman.balance_service.add_balance(r_customer_sql.customer_id,
                                                                                currency_id_2,
                                                                                add_amount_currency_2)

    total_currency_2_before = float(add_balance_currency_2['result']['balance']['total'])
    available_currency_2_before = float(add_balance_currency_2['result']['balance']['available'])
    frozen_currency_2_before = float(add_balance_currency_2['result']['balance']['frozen'])

    # Turn-off DXCASH mode for customer
    update_customer_response = r_customer_sql.postman.customer_service.update_customer(False, True)
    assert update_customer_response['error'] is None

    # Set membership fee to 200 EUR for fee plan 2
    Instruments.run_mysql_query("UPDATE local_config SET VALUE = " + fee_periodic_2 + " WHERE id = 10764 ;")

    # set the date the “nextProcessDate” to trigger fee deduction. Set the date to 24 h ago
    next_process_date = arrow.get().shift(days=-1).format('YYYY-MM-DD HH:mm:ss')
    assert next_process_date is not None
    last_process_date = arrow.get().shift(days=-30).format('YYYY-MM-DD HH:mm:ss')
    assert last_process_date is not None
    next_query = f"UPDATE fee_scheduler SET lastProcessDate = '{last_process_date}', " \
        f"nextProcessDate = '{next_process_date}', currentFeePlanId = 2, nextFeePlanId = 2 " \
        f" WHERE customerId = {r_customer_sql.customer_id}; "
    Instruments.run_mysql_query(next_query)

    # restart the PODS
    assert Kubernetes.restart_pod('membership-fee-service')
    time.sleep(30.0)
    assert Kubernetes.get_pods_by_name('membership-fee-service')

    convert_response = r_customer_sql.postman.obligation_service.convert_rate(currency_id_2, currency_id_default)
    assert convert_response.rate_value == Calculator.value_decimal(
        convert_response['result']['rates'][str(currency_id_2)])

    data = {'order_id': placed_order_id,
            'convert_response': rate_value,
            'balance': {'total_currency_default_before': total_currency_default_before,
                        'available_currency_default_before': available_currency_default_before,
                        'frozen_currency_default_before': frozen_currency_default_before,
                        'total_currency_1_before': total_currency_2_before,
                        'available_currency_1_before': available_currency_2_before,
                        'frozen_currency_1_before': frozen_currency_2_before
                        },
            }
    return data
