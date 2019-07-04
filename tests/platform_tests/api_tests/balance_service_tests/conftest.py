import pytest
from src.base import logger
from src.base.log_decorator import automation_logger


@pytest.fixture(scope="class")
@automation_logger(logger)
def add_balance(request, r_customer_sql):
    if hasattr(request, 'param'):
        response = r_customer_sql.postman.balance_service.add_balance(r_customer_sql.customer_id, request.param[0],
                                                                      request.param[1])
        assert response['result']['transactionGuid']
        assert "AAAAA" in response['result']['transactionGuid']
        logger.logger.info("GUID: {0}".format(response['result']['transactionGuid']))

        response = r_customer_sql.postman.balance_service.get_currency_balance(r_customer_sql.customer_id, request.param[0])
        assert float(response['result']['balance']['available']) >= 0

        #return float(response['result']['balance']['available']), float(response['result']['balance']['frozen'])

        return r_customer_sql
