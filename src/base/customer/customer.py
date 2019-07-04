import time
import string
import random
import datetime
from src.base.browser import Browser
from src.base import logger, test_token
from src.base.equipment.bank import Bank
from config_definitions import BaseConfig
from src.base.equipment.order import Order
from src.base.postman import PostmanClient
from src.base.instruments import Instruments
from src.base.equipment.deposit import Deposit
from src.repository.files import customer_scripts
from src.base.log_decorator import automation_logger


class Customer(object):

    @automation_logger(logger)
    def __init__(self, row_number=None, *args):
        """
        Class constructor builds main properties and initiate main attributes.
        :param row_number: Integer, if provided - customer will be chosen from wtp_tests_customers.csv
        :param args: email- str, password- str, customer_id- int
        """
        super(Customer, self).__init__()
        self.output_file = BaseConfig.TOOL_OUTPUT_FILE
        self.customers_file = BaseConfig.WTP_TESTS_CUSTOMERS
        self.crm_users_file = BaseConfig.CRM_TESTS_USERS
        if row_number is not None:
            self.set_customer_details(row_number)
        elif args and len(args) > 0:
            if isinstance(args[0], str):
                (self.email, self.password, customer_id) = args
            elif len(args[0][0]) and isinstance(args[0][0], tuple):
                (((self.email, self.password, customer_id),),) = args
            else:
                ((self.email, self.password, customer_id),) = args
            self.customer_id = int(customer_id)
            self.username = self.email.split('@')[0]
            if '_' in self.username:
                self.first_name = self.username.split('_')[0]
                self.last_name = self.username.split('_')[1]
            else:
                self.first_name = self.username
                self.last_name = self.username
        else:
            self.user_first_last_name = Instruments.generate_user_first_last_name() + \
                                        ''.join(random.choice(string.ascii_lowercase) for _ in range(4))
            self.username = '_'.join(self.user_first_last_name.split(' '))
            self.first_name = self.username.split('_')[0]
            self.last_name = self.username.split('_')[1]
            self.email = self.username + "@sandbox7e64c317900647609c225574db67437b.mailgun.org"
            self.customer_id = 0
            self.password = "1Aa@<>12"
        self.transactions = []
        self.define_static_details()
        self.bank = Bank(self)
        self.scripts = customer_scripts
        self.credit_card = self.bank.credit_card
        self.postman = PostmanClient.get_static_postman()
        self.faked_email = self.username + "@mailinator.com"
        self.auth_token, self.api_token, self.api_secret, self.api_token_id, self.ver_token, self.api_token_state, \
        self.hashed_password, self.api_key = None, None, None, None, None, False, None, None
        self.script_test_token = "$.ajaxPrefilter(function (options) {if (!options.beforeSend) {options.beforeSend = " \
                                 "function (xhr) {xhr.setRequestHeader('Test-Token', '%s');}}})" % test_token

    @automation_logger(logger)
    def set_customer_details(self, index=0):
        """
        Setter- reads wtp_tests_customers.csv and chooses row according to provided index, if index not provided it will
        be chosen randomly.
        :param index: Row to select from file.
        :return: Customer details (properties).
        """
        if index == 0:
            average = len(Instruments.get_data(self.customers_file))
            index = 0 if average <= 2 else random.randint(0, average - 1)
        customers = Instruments.get_account_details(self.customers_file, index)
        self.email = customers['email']
        self.password = customers['password']
        self.customer_id = int(customers['customer_id'])
        self.username = self.email.split('@')[0]
        if '_' in self.username:
            self.first_name = self.username.split('_')[0]
            self.last_name = self.username.split('_')[1]
        else:
            self.first_name = self.username
            self.last_name = self.username

    @classmethod
    @automation_logger(logger)
    def define_static_details(cls, country_code=None, state_number=None):
        """
        Method as a setter to set static customer details.
        An addition also common properties as full_phone and birthday_timestamp
        :param state_number:
        :param country_code: If country_code- int provided it will build static details accordingly.
        """
        from src.base.customer import customer_details as details

        cls.gender = details.GENDER
        cls.street = details.STREET
        cls.birthday = details.BIRTHDAY
        cls.language = details.LANGUAGE
        # cls.phone = Instruments.get_faked_phone()
        cls.phone = '052' + ''.join(random.choice(string.digits) for _ in range(7))
        if country_code:
            code_details = details.choose_customer_details(country_code, state_number)
            cls.zip_ = code_details['ZIP']
            cls.city = code_details['CITY']
            cls.state = code_details['STATE']
            cls.country = code_details['COUNTRY']
            cls.state_code = code_details['STATE_CODE']
            cls.country_code = code_details['COUNTRY_CODE']
            cls.phone_prefix = code_details['PHONE_PREFIX']
        else:
            cls.zip_ = details.IL_ZIP
            cls.city = details.IL_CITY
            cls.state = details.IL_STATE
            cls.country = details.IL_COUNTRY
            cls.state_code = details.IL_STATE_CODE
            cls.country_code = details.IL_COUNTRY_CODE
            cls.phone_prefix = details.IL_PHONE_PREFIX
        cls.full_phone = cls.phone_prefix + cls.phone[1:]
        cls.birthday_timestamp = int(
            time.mktime(datetime.datetime.strptime(cls.birthday, "%d/%m/%Y").timetuple()))

    @staticmethod
    @automation_logger(logger)
    def get_browser_functionality():
        """
        Provides Browser methods (static).
        :return: Browser class.
        """
        return Browser

    @automation_logger(logger)
    def get_postman_access(self, auth_token=None):
        """
        Setter for Customer property (self.postman).
        :param auth_token: Authorization token (if provided only for authorized self.output_file).
        """
        self.postman = PostmanClient(auth_token)
        return self

    @automation_logger(logger)
    def set_api_access(self):
        """
        Setter- Creates api_token (needed for log in by token) and activate it via ApiService.
        :return: Customer api details (properties).
        """
        if self.auth_token:
            try:
                if self.api_token_state is False:
                    api_tokens = self.postman.api_service.get_api_tokens()
                    logger.logger.info("get_api_token", api_tokens)
                    assert api_tokens['error'] is None
                    if api_tokens['result']['apiToken'] is not None:
                        self.api_token_id = api_tokens['result']['apiToken'][0]['id']
                        self.api_key = api_tokens['result']['apiToken'][0]['name']
                        self.api_token = api_tokens['result']['apiToken'][0]['token']
                        _notification = self.postman.notification_service.resend_sms(self.api_key, 7, "renew")
                        assert _notification['error'] is None
                        renew_response = self.postman.api_service.renew_api_token(self.api_key, self.api_token_id)
                        logger.logger.info("renew_api_token", renew_response)
                        assert renew_response['error'] is None
                        self.api_secret, self.api_token, self.api_token_id = renew_response['result']['secret'], \
                                                                             renew_response['result']['token'], \
                                                                             renew_response['result']['id']
                        logger.logger.info(
                            "API Access: {0}, {1}, {2}".format(self.api_secret, self.api_token, self.api_token_id))
                    else:
                        self.api_key = Instruments.random_string_generator()
                        notification_ = self.postman.notification_service.resend_sms(self.api_key, 6, "create")
                        assert notification_['error'] is None
                        create_response = self.postman.api_service.create_api_token(self.api_key)
                        assert create_response['result']['token'] and create_response['result']['secret'] and \
                               create_response['result']['id']
                        self.api_token, self.api_secret, self.api_token_id = create_response['result']['token'], \
                                                                             create_response['result']['secret'], \
                                                                             create_response['result']['id']
                    api_tokens2 = self.postman.api_service.get_api_tokens()
                    if api_tokens2['result']['apiToken'][0]['isActive'] is False:
                        activate_response = self.postman.api_service.activate_api_token(self.api_token_id, True)
                        logger.logger.info("activate_response", activate_response)
                        assert activate_response['error'] is None
                    self.api_token_state = True
                return self
            except Exception as e:
                logger.logger.exception("get_api_access failed: ", e)
        else:
            logger.logger.error("get_api_access method needs activated postman client (with auth_token) !")

    @automation_logger(logger)
    def customer_registration(self):
        """
        Full registration flow and customer approval via crm service.
        :return: tuple of 0- email, 1- password, 2- customer_id, 3- sid_token, 4- time_stamp.
        """
        try:
            step1_response = self.postman.authorization_service.sign_up_step_1(self)
            assert step1_response['result']['customerId']
            self.customer_id = int(step1_response['result']['customerId'])
            self.auth_token = step1_response['result']['token']
            self.postman = PostmanClient.get_static_postman(self.auth_token)
            Instruments.get_mail_gun_item(self)
            ver_response = self.postman.authorization_service.verify_email_step_2(self.email, self.ver_token)
            assert ver_response['result']['errors'] is None and ver_response['error'] is None
            time_phone = time.perf_counter() + 60.0
            step3_response = self.postman.authorization_service.add_phone_step_3(self)
            while step3_response['error'] is not None or step3_response['result']['errors'] is not None and time_phone \
                    > time.perf_counter():
                step3_response = self.postman.authorization_service.add_phone_step_3(self)
            self.postman.authorization_service.verify_phone_step_4()
            self.postman.authorization_service.update_personal_details_step_5(self)
            step6 = self.postman.authorization_service.client_checklist_step6()
            assert step6['error'] is None and step6['result']['errors'] is None
            link1 = self.postman.file_service.upload_file(BaseConfig.DOCUMENT_PNG)['link']
            time.sleep(1.0)
            link2 = self.postman.file_service.upload_file(BaseConfig.DOCUMENT_JPG)['link']
            time.sleep(1.0)
            link3 = self.postman.file_service.upload_file(BaseConfig.DOCUMENT_PNG)['link']
            time.sleep(1.0)
            self.postman.authorization_service.upload_documents_step_7(link1, link2, link3)
            login_response = self.postman.authorization_service.login_by_credentials(self.email, self.password)
            if login_response['error'] is None:
                self.auth_token = login_response['result']['token']
                self.postman = PostmanClient.get_static_postman(self.auth_token)
                logger.logger.info(self.email + "," + self.password + "," + str(self.customer_id) + "\n")
                Instruments.save_into_file(self.email + "," + self.password + "," + str(self.customer_id) + "\n",
                                           self.output_file)
                return self
            else:
                logger.logger.exception("login_by_credentials is not passed for Customer: {0}, {1}, {2}".format(
                    self.email, self.password, self.customer_id))
                raise Exception("LOG IN DIDN't PASSED !!!")
        except Exception as e:
            logger.logger.exception("{0} customer_registration failed with error: {1}".format(e.__class__.__name__,
                                                                                              e.__cause__), e)
            raise e

    @automation_logger(logger)
    def insert_customer_new(self):
        """
        Full registration flow and customer approval via crm service.
        :return: tuple of 0- email, 1- password, 2- customer_id, 3- sid_token, 4- time_stamp.
        """
        try:
            step1_response = self.postman.authorization_service.sign_up_step_1(self)
            assert step1_response['result']['customerId']
            self.customer_id = int(step1_response['result']['customerId'])
            self.auth_token = step1_response['result']['token']
            self.postman = PostmanClient.get_static_postman(self.auth_token)
            Instruments.change_customer_phone(self.customer_id, self.full_phone)
            return self
        except Exception as e:
            logger.logger.exception("{0} customer_pending failed with error: {1}".format(e.__class__.__name__,
                                                                                         e.__cause__), e)
            raise e

    @automation_logger(logger)
    def insert_customer_sql(self):
        self.insert_customer_new()
        self.set_customer_status(3)
        return self

    @automation_logger(logger)
    def registration_from_step_2_to_8(self):
        """
        Full registration flow and customer approval via crm service.
        :return: tuple of 0- email, 1- password, 2- customer_id, 3- sid_token, 4- time_stamp.
        """
        try:
            Instruments.get_mail_gun_item(self)
            ver_response = self.postman.authorization_service.verify_email_step_2(self.email, self.ver_token)
            assert ver_response['result']['errors'] is None and ver_response['error'] is None
            time_phone = time.perf_counter() + 60.0
            step3_response = self.postman.authorization_service.add_phone_step_3(self)
            while step3_response['error'] is not None or step3_response['result']['errors'] is not None and time_phone \
                    > time.perf_counter():
                step3_response = self.postman.authorization_service.add_phone_step_3(self)
            self.postman.authorization_service.verify_phone_step_4()
            self.postman.authorization_service.update_personal_details_step_5(self)
            step6 = self.postman.authorization_service.client_checklist_step6()
            assert step6['error'] is None and step6['result']['errors'] is None
            link1 = self.postman.file_service.upload_file(BaseConfig.DOCUMENT_PNG)['link']
            time.sleep(1.0)
            link2 = self.postman.file_service.upload_file(BaseConfig.DOCUMENT_JPG)['link']
            time.sleep(1.0)
            link3 = self.postman.file_service.upload_file(BaseConfig.DOCUMENT_PNG)['link']
            time.sleep(1.0)
            self.postman.authorization_service.upload_documents_step_7(link1, link2, link3)
            login_response = self.postman.authorization_service.login_by_credentials(self.email, self.password)
            if login_response['error'] is None:
                self.auth_token = login_response['result']['token']
                logger.logger.info(self.email + "," + self.password + "," + str(self.customer_id) + "\n")
                Instruments.save_into_file(self.email + "," + self.password + "," + str(self.customer_id) + "\n",
                                           self.output_file)
                return self
            else:
                logger.logger.exception("login_by_credentials is not passed for Customer: {0}, {1}, {2}".format(
                    self.email, self.password, self.customer_id))
                raise Exception("LOG IN DIDN't PASSED !!!")
        except Exception as e:
            logger.logger.exception("{0} customer_registration failed with error: {1}".format(e.__class__.__name__,
                                                                                              e.__cause__), e)
            raise e

    @automation_logger(logger)
    def approve_via_crm(self):
        self.postman.crm.approve_customer([self.customer_id, ])
        return self

    @automation_logger(logger)
    def add_credit_card_and_deposit(self, deposit_amount, currency_id):
        """
        Sends HTTP requests to PaymentService to create customer credit card and deposit for it.
        :param deposit_amount: Float.
        :param currency_id: Integer.
        :return: tuple of 0- id, 1- deposit_id
        """
        try:
            cards = self.postman.payment_service.get_credit_cards()
            try:
                card_status = cards['result']['cards'][-1]['status']
                if card_status != 1:
                    self.set_credit_card_status(cards['result']['cards'][-1]['id'], 1)
                self.credit_card.id = cards['result']['cards'][-1]['id']
            except (IndexError, TypeError, ValueError):
                credit_card_response = self.postman.payment_service.add_credit_card(self.credit_card)
                self.credit_card.id = credit_card_response['result']['card']["id"]
                self.set_credit_card_status(self.credit_card.id, 1)

            deposit_card_response = self.postman.payment_service.add_deposit_credit_card(self.credit_card,
                                                                                         deposit_amount, currency_id)
            deposit_id = str(deposit_card_response['result']['depositId'])
            deposit_cc = Deposit(deposit_id)
            self.transactions.append(deposit_cc)
        except Exception as e:
            logger.logger.exception(
                "{0} add_credit_card_and_deposit failed with error: {1}".format(e.__class__.__name__,
                                                                                e.__cause__), e)

    # @automation_logger(logger)
    # def rollback_frozen_balance(self, balances):
    #     """
    #     # transaction_link- str, customer_id- int, currency_id- int, subtract_amount- int
    #     @param balances:
    #     """
    #     for balance in balances:
    #         if float(balance['balance']['frozen']) > 0.0:
    #             # transaction_link- str, customer_id- int, currency_id- int, subtract_amount- int
    #             rollback_response = self.postman.balance_service.subtract_transaction_partial_rollback(
    #                 "587756e2-47c9-4ff7-9c6d-77410ba636a0", self.customer_id, balance['currencyId'],
    #                 float(balance['balance']['frozen']))
    #             logger.logger.info("If result in service response: {0}".format(rollback_response['result']))

    @automation_logger(logger)
    def subtract_available_balance(self, balances):
        for balance in balances:
            if float(balance['balance']['available']) > 0.0:
                subtract_response = self.postman.balance_service.subtract_balance(
                    self.customer_id, balance['currencyId'], float(balance['balance']['available']))
                logger.logger.info("If result in service response: {0}".format(subtract_response['result']))

    @automation_logger(logger)
    def cancel_open_orders(self, orders):
        for order in orders:
            cancel_response = self.postman.order_service.cancel_order(order.internal_id)
            logger.logger.info("If error in service response: {0}".format(cancel_response['error']))
        return self

    @classmethod
    @automation_logger(logger)
    def get_open_orders_mysql(cls, customer_id):
        """
        Method return a list of all open orders by customer, unmatched an partially filled
        input: customer ID
        output: list of "order" objects.
        :return:
        """
        orders = []
        unmatched_orders = Order.orders_data_converter(Instruments.get_orders_by_customer_mysql(customer_id, 1))
        partially_filled = Order.orders_data_converter(Instruments.get_orders_by_customer_mysql(customer_id, 1, 1))

        if unmatched_orders:
            orders.extend(unmatched_orders)
        if partially_filled:
            orders.extend(partially_filled)

        return orders

    @automation_logger(logger)
    def clean_up_customer(self):
        """
        Cleans the customer. Cancels all orders, unfreezes all balance by GUIDs, removes all balance from the customer
        :return: Clean customer with no orders and empty blanace.
        """
        orders = self.get_open_orders_mysql(self.customer_id)
        if orders:
            self.cancel_open_orders(orders)
        cur_balance = self.postman.balance_service.get_all_currencies_balance(self.customer_id)
        assert isinstance(cur_balance['result'], list)
        balances = cur_balance['result']
        # self.rollback_frozen_balance(balances)
        self.unfreeze_by_GUIDs()
        self.subtract_available_balance(balances)
        return self

    @classmethod
    @automation_logger(logger)
    def count_order_book(cls, instrument_id, direction):
        """
        Counts the sum of quantities in Order Book for the selected instrument.
        Returns sum of quantities and the Best Price (both for Buy and Sell).
        :param instrument_id:
        :param direction:
        :return:
        """
        order_book = Instruments.get_orders_best_price_and_quantity(instrument_id, direction, 2)
        if order_book is not None and len(order_book) > 0:
            quantity = 0
            for record in order_book:
                quantity += record[1]

            if direction == "sell":
                price = order_book[len(order_book) - 1][0]
            elif direction == "buy":
                price = order_book[len(order_book) - 1][0]
            else:
                price = 0

            # Rounding the quantity if required to prevent order sending failure.
            tail_digits_allowed = Instruments.get_quantity_tail_digits(instrument_id)
            quantity = round(quantity, tail_digits_allowed)

            return quantity, price

    @automation_logger(logger)
    def clean_instrument(self, instrument_id, base_currency=None, quoted_currency=None):

        if base_currency is None or quoted_currency is None:
            quoted_currency = Instruments.get_currency_by_instrument(instrument_id)[1]
            base_currency = Instruments.get_currency_by_instrument(instrument_id)[0]

        buy_order_book_counted = self.count_order_book(instrument_id, "buy")
        if buy_order_book_counted is not None:
            Instruments.set_price_last_trade(instrument_id, buy_order_book_counted[1])
            Instruments.set_ticker_last_price(instrument_id, buy_order_book_counted[1])

            self.postman.balance_service.add_balance(self.customer_id, quoted_currency,
                                                     900000000000.0)
            logger.logger.info(F"Quantity to buy: {buy_order_book_counted[0]} Price to pay: {buy_order_book_counted[1]}")
            response = self.postman.order_service.create_order_sync(
                Order().set_order(1, instrument_id, buy_order_book_counted[0], buy_order_book_counted[1]))
            assert response['error'] is None, "Failed to clean the Order Book"

        sell_order_book_counted = self.count_order_book(instrument_id, "sell")
        if sell_order_book_counted is not None:
            Instruments.set_price_last_trade(instrument_id, sell_order_book_counted[1])
            Instruments.set_ticker_last_price(instrument_id, sell_order_book_counted[1])

            sell_order_book_counted = self.count_order_book(instrument_id, "sell")
            self.postman.balance_service.add_balance(self.customer_id, base_currency, 900000000000.0)
            logger.logger.info(F"Quantity to sell: {sell_order_book_counted[0]} Price to pay: {sell_order_book_counted[1]}")
            response = self.postman.order_service.create_order_sync(
                Order().set_order(2, instrument_id, sell_order_book_counted[0], sell_order_book_counted[1]))
            assert response['error'] is None, "Failed to clean the Order Book"

    @automation_logger(logger)
    def insert_new_crm_user_sql(self):
        date_ = str(datetime.date.today()) + " 00:00:00"
        query = """INSERT INTO local_users (brokerId, email, firstName, lastName, city, country, zip, streetName, 
        streetNum, aptNum, primaryPhone, secondaryPhone, extension, cellphone, username, password, userTypeId, 
        department, position, affiliateCanSee, commision, status, dateJoined, datePassword, lastLogin, lastPassword, 
        isResetPassword, resetPasswordDate, home_list_order, enableReports, assigCmpId, assigCmpFields, 
        userSelectedLang, plnxImportAccount, pbxAgentId, regulationCompliance, displayPhone, showAllCustomers, 
        displaySearch, displayDesks, displayEmail, displayCampaignList, depId, isActive, failLoginDate, 
        failLoginAttempts, permissionGroupId, lastUpdateDate, signature, departmentId, displayCountry, MFAActive, 
        MFASecret, qrSecret, associateBy, ivrExtension, modifiedByUserId, mpsUser, createdDate, createdByUserid) 
        VALUES  (100001, '""" + self.email + """', '""" + self.first_name + """', '""" + self.last_name + """', '', 
        0, 0, '', 0, 0, '""" + self.full_phone + """', '', 0, '""" + self.full_phone + """', '""" + \
        self.username + """', md5('""" + self.password + """Spider-Pig'), 1, 'manager', 'admin', 0, 0.00, 
        'Active', '""" + date_ + """', '""" + date_ + """', '""" + date_ + """', 'a7217ffaf7b859b6dbff610a1d219d7', 
        0, '""" + date_ + """', '', 0, -1, '', 'en', 0, -1, 0, 1, 0, 1, 1, 1, 1, 0, 1, '""" + date_ + """', 
        8, 1, '""" + date_ + """', '', NULL, 1, 0, '', NULL, 0, -1, 48, 0, '""" + date_ + """', 0)"""
        Instruments.run_mysql_query(query)
        logger.logger.info(F"CRM User created: Email: {self.email} Password: {self.password} USERNAME: {self.username}")
        # Instruments.save_into_file(self.email + "," + self.password + "," + self.username + "\n", self.crm_users)
        if self.postman.crm.log_in_to_crm(self.username, self.password):
            return self.username, self.password

    @automation_logger(logger)
    def add_deposit_on_customer_balance(self, currency_id, amount):
        """
        Inserts given amount into Redis and SQL DB for provided customer.
        :param currency_id: Id of currency for balance.
        :param amount: amount of deposit to insert.
        :return: True if all successful and False otherwise.
        """
        if Instruments.add_customer_deposit_sql(self.customer_id, currency_id, amount):
            if Instruments.add_customer_balance_redis(self.customer_id, currency_id, amount):
                logger.logger.info(
                    F"Deposit was added for customer- {self.customer_id} balance successfully, current deposit: {amount}")
                _response = self.postman.balance_service.add_balance(self.customer_id, currency_id, amount)
                assert _response['result']['transactionGuid']
                assert "AAAAA" in _response['result']['transactionGuid']
                return True
            else:
                logger.logger.exception("Error occurred with add_customer_deposit...")
        else:
            logger.logger.exception("Error occurred with add_customer_balance...")

    @automation_logger(logger)
    def set_customer_status(self, status):
        """
        Can be used to modify customer's status directly in SQL.
        :param status: A valid customer status (statuses can be found in "customer_status" DB table)
        :return:
        """
        if status < 0:
            return False

        query = F"UPDATE customers SET status = {status} WHERE id = {self.customer_id}"
        logger.logger.info(F"Changing customer {self.customer_id} status to {status}")

        try:
            Instruments.run_mysql_query(query)
        except Exception as e:
            logger.logger.error("setting customer_status has failed:", e)
            raise e

    @automation_logger(logger)
    def set_credit_card_status(self, credit_card_id, status):
        query = F"UPDATE customer_cards SET status = {status} WHERE id = {credit_card_id}"
        logger.logger.info(F"Changing credit card status {status}")

        try:
            Instruments.run_mysql_query(query)
        except Exception as e:
            logger.logger.error("setting credit card status has failed:", e)
            raise e

    @automation_logger(logger)
    def unfreeze_by_GUIDs(self):

        currencies = Instruments.get_currencies_list()

        for currency in currencies:
            customer_transactions = self.postman.balance_service.get_subtract_transactions(self.customer_id, currency)
            guid_list = customer_transactions['result']['subtractTransactions']

            if guid_list is not []:
                for guid in guid_list:
                    self.postman.balance_service.subtract_transaction_commit(guid['transactionGuid'], self.customer_id, currency)

        return True


# if __name__ == '__main__':
#    Instruments.add_deposit_on_customer_balance(100001100000020643, 3, '20')
#     from src.base.customer.registered_customer import RegisteredCustomer
#
#     conf_customer = RegisteredCustomer(None, "Colton_Murphy@guerrillamailblock.com", "1Aa@<>12", "100001100000022877")
#     c = conf_customer.clean_up_customer()
#     pass
