import arrow
import unittest
from proboscis import test
from src.base.customer import Customer
from src.base.enums import Browsers
from src.drivers.webdriver_factory import WebDriverFactory
from test_definitions import BaseConfig
from proboscis.asserts import assert_true
from src.base.instruments import Instruments
from src.base.postman_client import PostmanClient


@test(groups=['fees', ])
class CancelOrderMinimalSufficientVolumeTest(unittest.TestCase):
    def setUp(self):
        self.test_case = "6234"
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.customer = Customer()
        # Grep all customer details.
        account_details = Instruments.get_csv_data(BaseConfig.CUSTOMERS_PENDING)[-1][0].split(',')
        self.email = account_details[0]
        self.password = account_details[1]
        self.customer_id = account_details[2]
        self.auth_token = account_details[5]
        # Generate phone number.
        self.phone = Instruments.generate_phone_number()
        # SQL update customer status.
        Instruments.customer_approval(self.customer_id)
        # Turn-off DXCASH mode for customer.
        Instruments.run_mysql_query("UPDATE customers SET dxexFeesEnabled=0 WHERE id = " + self.customer_id + ";")
        self.browser = self.customer.get_browser_functionality()
        #self.browser.execute_js(self.driver, self.customer.script_storage_clear)
        # Set membership fee
        Instruments.run_mysql_query("UPDATE local_config SET VALUE = 1000 WHERE id = 10617;")
        self.postman = PostmanClient(self.auth_token)
        # Adding credit card , calling PaymentService.
        credit_card_response = self.postman.add_credit_card(self.email, self.phone)
        self.card_id = str(credit_card_response['result']['card']["id"])
        # Adding deposit EUR- 500
        deposit_card_response = self.postman.add_deposit_credit_card(self.card_id, "500", "2")
        self.deposit_id = str(deposit_card_response['result']['depositId'])
        # Adding BTC on balance, calling BalanceService.
        add_balance_response = PostmanClient.add_balance(self.customer_id, "3", "20")
        self.available_balance = str(add_balance_response['result']['balance']['available'])
        # Calculate rate, calling API.
        convert_response = self.postman.convert_rate("3", "2")
        rate_value = int(convert_response['result']['rates']['3']['value'])
        rate_precisions = int(convert_response['result']['rates']['3']['decimals'])
        self.rate = Instruments.calculate_from_decimals(rate_value, rate_precisions)

    @test(groups=['functional', 'positive', ], depends_on_groups=["sanity", ])
    def test_cancel_order_minimal_sufficient(self):
        step1, step2, step3, step4 = False, False, False, False
        try:
            # Calculating order quantity.
            quantity1 = round((100 / self.rate), 5)
            # Sending order with price 9999.
            order1 = self.postman.create_order('2', quantity1, "1018", 9999)
            quantity2 = round((600 / self.rate), 5)
            order2 = self.postman.create_order('2', quantity2, "1018", 9999)
            quantity3 = round((2500 / self.rate), 5)
            order3 = self.postman.create_order('2', quantity3, "1018", 9999)
            order1_status = order1['result']['status']
            order2_status = order2['result']['status']
            order3_status = order3['result']['status']
            if order1_status and order2_status and order3_status is True:
                step1 = True
            currency_balance_response = self.postman.get_currency_balance(self.customer_id, '3')
            available_balance = str(currency_balance_response['result']['balance']['available'])
            subtract_response = self.postman.subtract_balance(self.customer_id, '3', available_balance)
            subtract_balance = int(subtract_response['result']['balance']['available'])
            if subtract_balance == 0:
                step2 = True
            last_process_date = Instruments.run_mysql_query(
                "SELECT lastProcessDate FROM fee_scheduler WHERE fee_scheduler.customerId =" + self.customer_id)[0][0]
            last_process_date_new = arrow.get(last_process_date).shift(days=-1).format('YYYY-MM-DD HH:mm:ss')
            query = "UPDATE fee_scheduler SET lastProcessDate ='" + last_process_date_new + "';"
            Instruments.run_mysql_query(query)
            step3 = True
            self.driver = WebDriverFactory.get_driver(Browsers.CHROME.value)
            step4 = self.browser.restart_pod(self.driver, BaseConfig.KUBERNETES, "membership-fee-service")

        finally:
            if step1 and step2 and step3 and step4 is True:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

