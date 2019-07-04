import allure
import pytest
from src.base import logger
from src.base.log_decorator import automation_logger

test_case = "6221"
currency_id = 1
fee_periodic_2 = '200'  # deducted after next deposit


@pytest.mark.membership_fee
@pytest.mark.usefixtures("r_time_count", "r_customer_sql", "fee_cleanup")
class TestMembershipFeeBalanceUpdate(object):

    @allure.step("test_membership_fee_balance_update")
    @automation_logger(logger)
    @pytest.mark.parametrize('preconditions_c6221', [[currency_id, fee_periodic_2]], indirect=True)
    def test_membership_fee_balance_sufficient(self, r_customer_sql, preconditions_c6221):
        # Verify that the next month fee deducted according selected fee plan
        balance_after = r_customer_sql.postman.balance_service.get_currency_balance(r_customer_sql.customer_id,
                                                                                    currency_id)
        total_after_fee = float(balance_after['result']['balance']['total'])
        available_after_fee = float(balance_after['result']['balance']['available'])
        frozen_after_fee = float(balance_after['result']['balance']['frozen'])

        total_before = preconditions_c6221['balance']['total_before']
        available_before = preconditions_c6221['balance']['available_before']
        frozen_before = preconditions_c6221['balance']['frozen_before']

        assert total_after_fee == float(total_before) - float(fee_periodic_2)
        assert available_after_fee == float(available_before) - float(fee_periodic_2)
        assert frozen_after_fee == frozen_before
        logger.logger.info(f"================== TEST CASE IS PASSED: {test_case}===================")
