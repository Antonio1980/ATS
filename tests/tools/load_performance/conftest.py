import pytest
from src.base import logger
from src.base.log_decorator import automation_logger
from src.base.customer.registered_customer import RegisteredCustomer


@pytest.fixture
@automation_logger(logger)
def load_customer():
    r_customer = RegisteredCustomer(None, "James_King@sandbox7e64c317900647609c225574db67437b.mailgun.org", "1Aa@<>12",
                                    "100001100000023976")
    return r_customer


@pytest.fixture
@automation_logger(logger)
def add_customer_balance(request, load_customer):
    logger.logger.info(request.param)
    for i in request.param:
        cur_balance = float(load_customer.postman.balance_service.get_currency_balance(
            load_customer.customer_id, int(i))['result']['balance']['available'])
        if cur_balance < 5000000.0:
            load_customer.postman.balance_service.add_balance(load_customer.customer_id, int(i), 5000000.0)


@pytest.fixture
@automation_logger(logger)
def add_custom_balance(request, load_customer):
    currency_, amount_ = request.param[0], request.param[1]
    response_ = load_customer.postman.balance_service.add_balance(load_customer.customer_id, currency_, amount_)
    assert response_['result']['transactionGuid']
