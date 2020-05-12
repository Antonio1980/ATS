from src.base import logger
from src.base.customer.customer import Customer
from src.base.log_decorator import automation_logger


class RegisteredCustomer(Customer):
    
    @automation_logger(logger)
    def __init__(self, row_number=0, *args):
        """
        Uses parent method get_customer_details() to get existing customer details,
        Updates customer (sid_token, time_stamp) at Guerrilla API,
        Updates customer (auth_token) at Web Platform and overwrites self.postman with auth_token (authorized).
        :param row_number: Needed to choose customer from file, if not provided it will be chosen randomly.
        """
        try:
            if args and len(args) > 0:
                super(RegisteredCustomer, self).__init__(None, args)
            else:
                super(RegisteredCustomer, self).__init__(row_number)

            login_response = self.postman.authorization_service.login_by_credentials(self.email, self.password)
            if login_response['error'] is None:
                self.auth_token = login_response['result']['token']
                self.get_postman_access(self.auth_token)
            else:
                self.set_api_access()
                if self.api_token_state:
                    login_by_token = self.postman.authorization_service.login_by_token(self.api_token, self.api_secret)
                    assert login_by_token['error'] is None and login_by_token['result']['token']
                    self.auth_token = login_response['result']['token']
                    self.get_postman_access(self.auth_token)
        except Exception as e:
            logger.logger.exception(
                "__init__ for RegisteredCustomer is not passed for RegisteredCustomer: {0}, {1}, {2}".format(
                    self.email, self.password, self.customer_id))
            raise e

        self.btc_wallet = "mr8MnPXT4KubFFQiXe4SeEB6T9ymjR2Hdp"
        self.xrp_wallet = "rKE6Y81ErNYAcowFnLqLFsfSAmuoN9SUx9?tg=262"
        self.bch_wallet = "bchtest:qprqh7gnv8f5nznkuqqcfnf2tpkz4kqpjc6ltdl3e2"
        self.eth_wallet = "0x8Cfbb4d2553ad1bC822A5cB41155E917C747AA51"
        self.ltc_wallet = "n3rifHSwMExDUeMsZATKF7mLB2UMmXktDK"
        self.dgb_wallet = "DEBVqvzq5m5WE5dxcxxohpkVLPeoMEXVXk"
