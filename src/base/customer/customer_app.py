from src.base import logger
from src.base.log_decorator import automation_logger
from src.base.customer.registered_customer import RegisteredCustomer


class CustomerApplication(RegisteredCustomer):
    
    @automation_logger(logger)
    def __init__(self, row_number=0, *args):
        """
        Class instance have public api access (api_token and secret).
        :param args: email, password, customer_id - strings
        """
        if args and len(args) > 0:
            super(CustomerApplication, self).__init__(None, args)
        else:
            super(CustomerApplication, self).__init__(row_number)
        self.set_api_access()
