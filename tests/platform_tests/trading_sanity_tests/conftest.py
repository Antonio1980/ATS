import pytest
from src.base import logger
from src.base.log_decorator import automation_logger


@pytest.fixture(scope="class")
@automation_logger(logger)
def cur_customer_balance(request, r_customer):
    quoted_currency_id = None
    if hasattr(request, 'param'):
        quoted_currency_id = request.param[0]
        for i in request.param:
            add_response = r_customer.postman.balance_service.add_balance(r_customer.customer_id, int(i), 50000.0)
            assert add_response['result']['transactionGuid']

    cur_balance = r_customer.postman.p_balance_service.get_balance(quoted_currency_id)
    logger.logger.info("Balance before: {0}".format(cur_balance))

    assert cur_balance['error'] is None
    frozen_quoted_before = \
        float(cur_balance['result']['balance'][str(quoted_currency_id)]['frozen'])
    logger.logger.info(f"Frozen quoted: {frozen_quoted_before}")
    return frozen_quoted_before
