import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger
from src.base.customer.registered_customer import RegisteredCustomer

test_case = ""


@allure.feature("Payment")
@allure.title("Portfolio Chat")
@allure.description("""
    Functional api test.
    Validation of responses portfolio chart 
    1)Check, that response returns 'Portfolio Time Span' (axis  X) as not empty value and 'customer
     portfolio value' (axis Y) as not empty value
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='Portfolio Chart')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/payment_service_tests/portfolio_chart_test.py",
                 "TestPortfolioChart")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.payment
@pytest.mark.regression
@pytest.mark.payment_service
class TestPortfolioChart(object):

    @pytest.fixture
    @automation_logger(logger)
    def reg_conf_customer(self):
        return RegisteredCustomer(None, 'Sarah_White@guerrillamailblock.com', '1Aa@<>12', '100001100000022300')

    @allure.step("Starting: test_add_credit_card")
    @automation_logger(logger)
    def test_portfolio_chart(self, reg_conf_customer):
        portfolio_response = reg_conf_customer.postman.payment_service.get_portfolio_chat(1)
        assert portfolio_response['error'] is None
        assert isinstance(portfolio_response['result']['portfolioHistory'], list)
        portfolio = portfolio_response['result']['portfolioHistory']
        for index in portfolio:
            assert list(index.keys()) == ['x', 'y']
            assert list(index.values()) is not None
        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))
