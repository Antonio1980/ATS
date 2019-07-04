import pytest
from src.base import logger
from src.base.log_decorator import automation_logger

currency_id = 2
amount = 100000000.0


@pytest.mark.load
@pytest.mark.usefixtures("r_time_count", "r_customer_sql")
@pytest.mark.parametrize('add_custom_balance', [[currency_id, amount]], indirect=True)
@automation_logger(logger)
def test_load_balance_service_freeze(r_customer_sql, add_custom_balance):

    try:
        for i in range(50000000):
            response_ = r_customer_sql.postman.balance_service.subtract_transaction_initialize(
                r_customer_sql.customer_id, currency_id, 2.0)
            assert response_['result']['transactionGuid']

            _response = r_customer_sql.postman.balance_service.subtract_transaction_commit()
    except Exception as e:
        logger.logger.error(f"{e}")
        pass

    assert float(r_customer_sql.postman.balance_service.get_currency_balance(
        r_customer_sql.customer_id, currency_id)['result']['balance']['available']) != 0.0
