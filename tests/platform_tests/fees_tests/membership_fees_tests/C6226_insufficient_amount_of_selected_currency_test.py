import allure
import pytest
from src.base import logger
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger

test_case = "6221"
currency_id_default = 1  # currency that set as 1 priority for fee deducting
currency_id_2 = 6  # XRP for deduction fee
fee_periodic_2 = '200'  # deducted after next deposit
add_amount_currency_default = 10
add_amount_currency_2 = 250
instrument_id = 1007
placed_order_id = ""
rate_value = ""


@pytest.mark.membership_fee
@pytest.mark.usefixtures("r_time_count", "r_customer_sql", "fee_cleanup")
class TestMembershipFeeBalanceUpdate(object):

    @allure.step("test_membership_fee_balance_update")
    @automation_logger(logger)
    @pytest.mark.parametrize('preconditions_c6226', [[currency_id_default, currency_id_2, fee_periodic_2,
                                                      add_amount_currency_default, add_amount_currency_2,
                                                      instrument_id, placed_order_id, rate_value]], indirect=True)
    def test_membership_fee_balance_sufficient(self, r_customer_sql, preconditions_c6226):
        # Verify that the next month fee deducted according selected fee plan
        default_currency_balance_after = r_customer_sql.postman.balance_service.get_currency_balance(r_customer_sql.customer_id,
                                                                                    currency_id_default)
        default_total_after_fee = float(default_currency_balance_after['result']['balance']['total'])
        default_available_after_fee = float(default_currency_balance_after['result']['balance']['available'])
        default_frozen_after_fee = float(default_currency_balance_after['result']['balance']['frozen'])

        default_total_before = preconditions_c6226['balance']['total_currency_default_before']
        default_available_before = preconditions_c6226['balance']['available_currency_default_before']
        default_frozen_before = preconditions_c6226['balance']['frozen_currency_default_before']

        assert default_total_after_fee == default_total_before
        assert default_available_after_fee == default_available_before
        assert default_frozen_after_fee == default_frozen_before

        currency_2_balance_after = r_customer_sql.postman.balance_service.get_currency_balance(
            r_customer_sql.customer_id, currency_id_2)
        currency_2_total_after_fee = float(currency_2_balance_after['result']['balance']['total'])
        currency_2_available_after_fee = float(currency_2_balance_after['result']['balance']['available'])
        currency_2_frozen_after_fee = float(currency_2_balance_after['result']['balance']['frozen'])

        currency_2_total_before = preconditions_c6226['balance']['total_currency_2_before']
        currency_2_available_before = preconditions_c6226['balance']['available_currency_2_before']
        currency_2_frozen_before = preconditions_c6226['balance']['frozen_currency_2_before']

        converted_rate = preconditions_c6226['convert_response']['rate_value']

        assert currency_2_total_after_fee == currency_2_total_before - float(fee_periodic_2 * converted_rate)
        assert currency_2_available_after_fee == currency_2_available_before - float(fee_periodic_2 * converted_rate)
        assert currency_2_frozen_after_fee == currency_2_frozen_before

        open_orders = Instruments.get_orders_by_customer_mysql(r_customer_sql.customer_id, 1)
        assert open_orders is not None
        assert open_orders

        logger.logger.info(f"================== TEST CASE IS PASSED: {test_case}===================")