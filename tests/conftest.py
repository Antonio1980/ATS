import time
import pytest
from src.base import logger
from src.base.browser import Browser
from src.base.services.crm import Crm
from config_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.customer.customer import Customer
from src.base.log_decorator import automation_logger
from src.drivers.webdriver_factory import WebDriverFactory
from src.base.customer.customer_app import CustomerApplication
from src.base.customer.registered_customer import RegisteredCustomer

instrument_id = 1008
c_currency_id = 4
currency_id = 1


collect_ignore = ["setup.py"]


@pytest.fixture(scope="class")
@automation_logger(logger)
def r_time_count(request):
    start_time = time.perf_counter()
    logger.logger.info("START TIME: {0}".format(start_time))

    def stop_counter():
        end_time = time.perf_counter()
        logger.logger.info(F"END TIME: {end_time}")
        average_time = time.strptime(time.ctime(end_time - start_time), "%a %b %d %H:%M:%S %Y")
        min_ = average_time.tm_min
        sec_ = average_time.tm_sec
        logger.logger.info("AVERAGE OF THE TEST CASE RUN TIME: {0} minutes {1} seconds".format(min_, sec_))

    request.addfinalizer(stop_counter)


@pytest.fixture(scope="class")
@automation_logger(logger)
def r_customer():
    r_customer = RegisteredCustomer()
    Instruments.customer_approval(r_customer.customer_id)
    return r_customer


@pytest.fixture(scope="class")
@automation_logger(logger)
def r_customer_sql():
    r_customer = Customer()
    r_customer.insert_customer_sql()
    return r_customer


@pytest.fixture(scope="class")
@automation_logger(logger)
def customer():
    customer = Customer()
    return customer


@pytest.fixture(scope="class")
@automation_logger(logger)
def customer_new():
    customer = Customer()
    customer.insert_customer_new()
    return customer


@pytest.fixture(scope="class")
@automation_logger(logger)
def customer_pending(customer):
    customer.customer_registration()
    return customer


@pytest.fixture(scope="class")
@automation_logger(logger)
def conf_customer():
    return RegisteredCustomer(None, BaseConfig.EMAIL, BaseConfig.PASSWORD, BaseConfig.CUSTOMER_ID)


@pytest.fixture(scope="class")
@automation_logger(logger)
def customer_app():
    return CustomerApplication()


@pytest.fixture(scope="class")
@automation_logger(logger)
def conf_customer_app():
    return CustomerApplication(None, BaseConfig.EMAIL, BaseConfig.PASSWORD, BaseConfig.CUSTOMER_ID)


@pytest.fixture(scope="class")
@automation_logger(logger)
def conf_prod_app():
    return CustomerApplication(None, BaseConfig.PROD_EMAIL, BaseConfig.PROD_PASSWORD, BaseConfig.PROD_CUSTOMER_ID)


@pytest.fixture(scope="class")
@automation_logger(logger)
def two_customers(request):
    if hasattr(request, 'param'):
        return Instruments.create_two_customers(request.param[0])
    else:
        return Instruments.create_two_customers()


@pytest.fixture(params=[[instrument_id, 1, "buy"]])
@automation_logger(logger)
def best_price_and_quantity(request):
    if hasattr(request, 'param'):
        (instrument_id_, direction, consistence) = request.param
        return Instruments.get_orders_best_price_and_quantity(instrument_id_, direction, consistence)


@pytest.fixture(params=[[instrument_id, ]])
@automation_logger(logger)
def get_last_trade_price_for_instrument(request):
    if hasattr(request, 'param'):
        return Instruments.get_price_last_trade(request.param[0])


@pytest.fixture(params=[[instrument_id, ]])
@automation_logger(logger)
def max_order_quantity_for_instrument(request):
    if hasattr(request, 'param'):
        instrument_id_ = str(request.param[0])
        try:
            return float(Instruments.run_mysql_query(
                f"SELECT maxOrderQuantity FROM instruments WHERE id= {instrument_id_};")[0][0])
        except Exception as e:
            logger.logger.error(f"{e}")
            pass


@pytest.fixture(params=[[instrument_id, ]])
@automation_logger(logger)
def min_order_quantity_for_instrument(request):
    if hasattr(request, 'param'):
        instrument_id_ = str(request.param[0])
        try:
            return float(Instruments.run_mysql_query(
                f"SELECT minOrderQuantity FROM instruments WHERE id= {instrument_id_};")[0][0])
        except Exception as e:
            logger.logger.error(f"{e}")
            pass


@pytest.fixture(params=[[currency_id, ]])
@automation_logger(logger)
def min_withdrawal_for_currency(request):
    if hasattr(request, 'param'):
        id_ = str(request.param[0])
        query = f"SELECT quantity FROM transaction_limitations WHERE transactionTypeId=2 AND limitationTypeId=1 AND " \
                f"currencyId= {id_}"
        try:
            return float(Instruments.run_mysql_query(query)[0][0])
        except Exception as e:
            logger.logger.error(f"{e}")
            pass


@pytest.fixture(params=[[currency_id, ]])
@automation_logger(logger)
def max_withdrawal_for_currency(request):
    if hasattr(request, 'param'):
        id_ = str(request.param[0])
        query = f"SELECT quantity FROM transaction_limitations WHERE transactionTypeId=2 AND limitationTypeId=2 AND " \
                f"currencyId= {id_}"
        try:
            return float(Instruments.run_mysql_query(query)[0][0])
        except Exception as e:
            logger.logger.error(f"{e}")
            pass


@pytest.fixture(params=[[currency_id, ]])
@automation_logger(logger)
def max_deposit_for_currency(request):
    if hasattr(request, 'param'):
        id_ = str(request.param[0])
        query = f"SELECT quantity FROM transaction_limitations WHERE transactionTypeId=1 AND limitationTypeId=2 AND " \
                f"currencyId= {id_}"
        try:
            return float(Instruments.run_mysql_query(query)[0][0])
        except Exception as e:
            logger.logger.error(f"{e}")
            pass


@pytest.fixture(params=[[currency_id, ]])
@automation_logger(logger)
def min_deposit_for_currency(request):
    if hasattr(request, 'param'):
        id_ = str(request.param[0])
        query = f"SELECT quantity FROM transaction_limitations WHERE transactionTypeId=1 AND limitationTypeId=1 AND " \
                f"currencyId= {id_}"
        try:
            return float(Instruments.run_mysql_query(query)[0][0])
        except Exception as e:
            logger.logger.error(f"{e}")
            pass


@pytest.fixture(scope="class", params=[[currency_id, c_currency_id, ]])
@automation_logger(logger)
def add_balance(request, r_customer):
    if hasattr(request, 'param'):
        for i in request.param:
            response = r_customer.postman.balance_service.add_balance(r_customer.customer_id, int(i), 50000.0)
            assert response['result']['transactionGuid']
            assert "AAAAA" in response['result']['transactionGuid']
            logger.logger.info("GUID: {0}".format(response['result']['transactionGuid']))


@pytest.fixture(scope="class")
@automation_logger(logger)
def clean_up_customer_approval(request, r_customer):

    def clean_up():
        response_after = Crm().approve_customer([r_customer.customer_id, int(BaseConfig.CUSTOMER_ID)])
        logger.logger.info(response_after)

    request.addfinalizer(clean_up)


@pytest.fixture(params=[[instrument_id, ]])
@automation_logger(logger)
def prices_from_orderbook(request, r_customer):
    if hasattr(request, 'param'):
        instrument_id_ = request.param[0]
        result_dict = r_customer.postman.order_service.get_order_book(instrument_id_)['result']
        sell_dict = result_dict["sell"]
        buy_dict = result_dict["buy"]
        price_s = sorted(sell_dict, key=lambda k: k['price']['value'], reverse=True)
        price_b = sorted(buy_dict, key=lambda k: k['price']['value'], reverse=True)

        if len(price_s) >= 1 and len(price_b) >= 1:
            price_sell = Instruments.calculate_from_decimals(price_s[0]['price']['value'],
                                                             price_s[0]['price']['decimals'])
            price_buy = Instruments.calculate_from_decimals(price_b[0]['price']['value'],
                                                            price_b[0]['price']['decimals'])
            return {"sell": price_sell, "buy": price_buy}
        
        else:
            return Instruments.get_safe_price(instrument_id_)


@pytest.fixture(params=[[instrument_id, ]])
@automation_logger(logger)
def safe_price(request):
    if hasattr(request, 'param'):
        instrument_id_ = request.param[0]
        return Instruments.get_safe_price(instrument_id_)


@pytest.fixture(scope="class", params=[[instrument_id, ]])
@automation_logger(logger)
def update_reference_price(request):
    instrument_id_ = str(request.param[0])
    ref_before = float(Instruments.run_mysql_query("SELECT referencePriceRatio FROM instruments WHERE id =" +
                                                   instrument_id_)[0][0])
    logger.logger.info("Reference price for Instrument ID- {0} before test is: {1}".format(instrument_id_,
                                                                                           ref_before))
    Instruments.run_mysql_query("UPDATE instruments SET referencePriceRatio = 1.50000000 WHERE id =" + instrument_id_)

    def update_ref():
        Instruments.run_mysql_query("UPDATE instruments SET referencePriceRatio = " + str(ref_before) +
                                    " WHERE id = " + instrument_id_)
        logger.logger.info("Reference price updated back to {0}".format(ref_before))

    request.addfinalizer(update_ref())


@pytest.fixture(scope="class", params=[["chrome"]])
@automation_logger(logger)
def web_driver(request):

    def stop_driver():
        logger.logger.info("TEST STOP -> Closing browser... {0}".format(web_driver.name))
        Browser.close_browser(web_driver)

    logger.logger.info("Driver is: {0}".format(request.param[0]))
    web_driver = WebDriverFactory.get_driver(request.param[0])
    request.cls.driver = web_driver
    request.addfinalizer(stop_driver)
    return web_driver


def pytest_runtest_makereport(item, call):
    if "incremental" in item.keywords:
        if call.excinfo is not None:
            parent = item.parent
            parent._previousfailed = item


def pytest_runtest_setup(item):
    if "incremental" in item.keywords:
        previousfailed = getattr(item.parent, "_previousfailed", None)
        if previousfailed is not None:
            pytest.xfail("previous test failed (%s)" % previousfailed.name)


@pytest.fixture(scope="class")
@automation_logger(logger)
def me_state():
    return Instruments.get_me_state()


# @pytest.yield_fixture(scope="class")
# @automation_logger(logger)
# def r_time_count():
#     start_time = time.perf_counter()
#     logger.logger.info("START TIME: {0}".format(start_time))
#     yield
#
#     end_time = time.perf_counter()
#     logger.logger.info("END TIME: {0}".format(end_time))
#     logger.logger.info("AVERAGE OF THE TEST CASE RUN TIME: {0} seconds".format(end_time - start_time))
