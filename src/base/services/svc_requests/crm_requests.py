from src.base import logger
from src.base.log_decorator import automation_logger
from src.base.services.svc_requests.request_constants import *
from src.base.services.svc_requests.request_schema import CrmRequestSchema


class CrmRequest(CrmRequestSchema):
    def __init__(self):
        super(CrmRequest, self).__init__()
        self.username = "username="
        self.password = "password="
        self.type = "type="
        self.type_id = "typeid="
        self.transaction_id = "transactionid="
        self.payment_method_id = "paymentmethodid="
        self.payment_method = "paymentMethod="
        self.hidecustomer_id = "hidecustomerid="
        self.currency_name = "currencyname="
        self.currency = "currency="
        self.amount = "amount="
        self.status_id = "statusid="
        self.edit_cancellation_reason = "editCancellationReason="
        self.name_bank_account = "nameBankAccount="
        self.iban = "iban="
        self.ref_number = "referenceNumber="
        self.bank_name = "bankName="
        self.bic = "bic="
        self.bank_address = "bankAddress="
        self.clearing_company = "clearingCompany="
        self.transaction_status = "trasactionStatus="
        self.date_ = self.date_from
        self.edit_date_ = self.edit_date
        self.past_date = self.date_to
        self.value_date = "dateValueDate=" + self.date_
        self.comments = "comments="
        self.customer_desc = "customerDesc="
        self.customer_id = "customerid="
        self.edit_transaction_status = "editTransactionStatus="
        self.edit_date_value_date = "editDateValueDate=" + self.edit_date_
        self.decline_reason = "declineReason="
        self.comments = "comments="
        self.a0, self.a1, self.a2, self.a3, self.a4, self.a5, self.a6, self.a7, self.a8, self.a9, self.a10, self.a11,  \
        self.a12, self.a13, self.a14, self.a15, self.a16, self.a17, self.a18, self.a19, self.a20, self.a21, self.a22,  \
        self.a23, self.a24, self.a25, self.a26, self.a27, self.a28, self.a29, self.a30, self.a31, self.a32, self.a33,  \
        self.a34, self.a35, self.a36, self.a37, self.a38, self.a39, self.a40, self.a41, self.a42, self.a43, self.a44,  \
        self.a45, self.a46, self.a47, self.a48, self.a49, self.a50, self.a51, self.a52, self.a53, self.a54, self.a55,  \
        self.a56, self.a57, self.a58, self.a59, self.a60, self.a61, self.a62, self.a63, self.a64, self.a65, self.a66,  \
        self.a67, self.a68, self.a69, self.a70, self.a71, self.a72, self.a73, self.a74, self.a75, self.a76, self.a77,  \
        self.a78, self.a79, self.a80, self.a81, self.a82 = None, None, None, None, None, None, None, None, None, None, \
        None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    \
        None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    \
        None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    \
        None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,    \
        None

    @automation_logger(logger)
    def log_in(self, username: str, password: str):
        """
        Builds request body for Crm.log_in_to_crm()
        :param username: CRM username.
        :param password: CRM password
        :return: Request body.
        """
        self.body.extend([
            self.username + username,
            self.password + password
        ])
        querystring = self.__repr__()
        logger.logger.info(REQUEST_BODY.format(querystring))
        return querystring

    @automation_logger(logger)
    def approve_customer_deposit(self, customer_id: int, customer, *args):
        """
        Builds request body for Crm.update_customer_deposit()
        :param customer_id: customer id registered.
        :param customer: Customer object contains bank object.
        :param args: deposit_id, payment_method_id, currency_name, currency_id, deposit_amount
        :return: Request body.
        """
        (deposit_id, payment_method_id, currency_name, currency_id, deposit_amount, *args) = args
        self.body.extend([
            self.type + "deposit",
            self.type_id + "deposit",
            self.transaction_id + str(deposit_id),
            self.payment_method_id + str(payment_method_id),
            self.hidecustomer_id + str(customer_id),
            self.currency_name + currency_name,
            self.currency + str(currency_id),
            self.amount + str(deposit_amount),
            self.status_id + "2",
            self.edit_cancellation_reason + "1",
            self.name_bank_account + customer.bank.bank_name,
            self.iban + customer.bank.iban,
            self.bank_name + customer.bank.bank_name,
            self.bic + customer.bank.bic,
            self.bank_address + customer.street
        ])
        querystring = self.__repr__()
        logger.logger.info(REQUEST_BODY.format(querystring))
        return querystring

    @automation_logger(logger)
    def approve_customer_withdrawal(self, customer_id: int, status_id, *args):
        """
        Builds request body for Crm.update_customer_withdrawal()
        :param customer_id: customer id registered.
        :param args: withdrawal_id, payment_method_id, currency_name, currency_id, withdrawal_amount.
        :param status_id: 1- pending system, 2- approved, 3- declined, 4- cancelled, 5- pending customer.
        :return: Request body.
        """
        ((withdrawal_id, payment_method_id, currency_name, currency_id, withdrawal_amount, ), ) = args
        self.body.extend([
            self.type + "withdrawal",
            self.type_id + "2",
            self.transaction_id + str(withdrawal_id),
            self.payment_method_id + str(payment_method_id),
            self.hidecustomer_id + str(customer_id),
            self.currency_name + str(currency_name),
            self.currency + str(currency_id),
            self.amount + str(withdrawal_amount),
            self.status_id + str(status_id),
            self.edit_cancellation_reason + "1",
            self.edit_transaction_status + "2",
            self.edit_date_value_date + "2019-06-19",
            self.decline_reason + " ",
            self.comments + "approved"
        ])
        querystring = self.__repr__()
        logger.logger.info(REQUEST_BODY.format(querystring))
        return querystring

    @automation_logger(logger)
    def add_new_deposit(self, customer, *args):
        """
        Builds request body for Crm.add_new_deposit()
        :param customer: Customer object.
        :param args: payment_method_id, currency_name, currency_id, deposit_amount
        :return: Request body.
        """
        (payment_method_id, currency_name, currency_id, deposit_amount) = args
        self.body.extend([
            self.type + "deposit",
            self.currency_name + currency_name,
            self.payment_method + str(payment_method_id),
            self.transaction_status + "2",
            self.currency + str(currency_id),
            self.amount + str(deposit_amount),
            self.ref_number + str(customer.customer_id),
            self.value_date,
            self.comments + "TestQATest",
            self.name_bank_account + customer.bank.bank_name,
            self.iban + customer.bank.iban,
            self.bank_name + customer.bank.bank_name,
            self.bic + customer.bank.bic,
            self.bank_address + customer.street,
            self.customer_desc + "TestQATest"
        ])
        querystring = self.__repr__()
        logger.logger.info(REQUEST_BODY.format(querystring))
        return querystring

    @automation_logger(logger)
    def get_deposit_by_id(self, customer_id: int):
        """
        Builds request body for Crm.get_deposit_by_id()
        :param customer_id: ID of customer.
        :return: Request body.
        """
        self.body.extend([
            self.type + "deposit",
            self.customer_id + str(customer_id)
        ])
        querystring = self.__repr__()
        logger.logger.info(REQUEST_BODY.format(querystring))
        return querystring

    @automation_logger(logger)
    def get_customer_deposits(self):
        """
        Builds request body for Crm.get_customer_deposits()
        :return: Request body.
        """
        self.a0 = "Echo=3"
        self.a1 = "iColumns=14"
        self.a2 = "sColumns="
        self.a3 = "iDisplayStart=0"
        self.a4 = "iDisplayLength=10"
        self.a5 = "mDataProp_0=id"
        self.a6 = "mDataProp_1=requesteddate"
        self.a7 = "mDataProp_2=confirmeddate"
        self.a8 = "mDataProp_3=datecandec"
        self.a9 = "mDataProp_4=paymentmethod"
        self.a10 = "mDataProp_5=clearingcompany"
        self.a11 = "mDataProp_6=netamount"
        self.a12 = "mDataProp_7=code"
        self.a13 = "mDataProp_8=feeAmount"
        self.a14 = "mDataProp_9=transstatus"
        self.a15 = "mDataProp_10=requestedby"
        self.a16 = "mDataProp_11=ccend"
        self.a17 = "mDataProp_12=referenceNumber"
        self.a18 = "mDataProp_13=comments"
        self.a19 = "sSearch="
        self.a20 = "bRegex=false"
        self.a21 = "sSearch_0="
        self.a22 = "bRegex_0=false"
        self.a23 = "bSearchable_0=true"
        self.a24 = "sSearch_1="
        self.a25 = "bRegex_1=false"
        self.a26 = "bSearchable_1=true"
        self.a27 = "sSearch_2="
        self.a28 = "bRegex_2=false"
        self.a29 = "bSearchable_2=true"
        self.a30 = "sSearch_3="
        self.a31 = "bRegex_3=false"
        self.a32 = "bSearchable_3=true"
        self.a33 = "sSearch_4="
        self.a34 = "bRegex_4=false"
        self.a35 = "bSearchable_4=true"
        self.a36 = "sSearch_5="
        self.a37 = "bRegex_5=false"
        self.a38 = "bSearchable_5=true"
        self.a39 = "sSearch_6="
        self.a40 = "bRegex_6=false"
        self.a41 = "bSearchable_6=true"
        self.a42 = "sSearch_7="
        self.a43 = "bRegex_7=false"
        self.a44 = "bSearchable_7=true"
        self.a45 = "sSearch_8="
        self.a46 = "bRegex_8=false"
        self.a47 = "bSearchable_8=true"
        self.a48 = "sSearch_9="
        self.a49 = "bRegex_9=false"
        self.a50 = "bSearchable_9=true"
        self.a51 = "sSearch_10="
        self.a52 = "bRegex_10=false"
        self.a53 = "bSearchable_10=true"
        self.a54 = "sSearch_11="
        self.a55 = "bRegex_11=false"
        self.a56 = "bSearchable_11=true"
        self.a57 = "sSearch_12="
        self.a58 = "bRegex_12=false"
        self.a59 = "bSearchable_12=true"
        self.a60 = "sSearch_13="
        self.a61 = "bRegex_13=false"
        self.a62 = "bSearchable_13=true"
        self.a63 = "iSortCol_0=1"
        self.a64 = "sSortDir_0=desc"
        self.a65 = "iSortingCols=1"
        self.a66 = "bSortable_0=true"
        self.a67 = "bSortable_1=true"
        self.a68 = "bSortable_2=true"
        self.a69 = "bSortable_3=true"
        self.a70 = "bSortable_4=true"
        self.a71 = "bSortable_5=true"
        self.a72 = "bSortable_6=true"
        self.a73 = "bSortable_7=true"
        self.a74 = "bSortable_8=true"
        self.a75 = "bSortable_9=true"
        self.a76 = "bSortable_10=true"
        self.a77 = "bSortable_11=true"
        self.a78 = "bSortable_12=true"
        self.a79 = "bSortable_13=true"
        self.a80 = "transactionStatuses="
        self.a81 = "datefrom=" + self.past_date + "+00%3A00%3A00"
        self.a82 = "dateto=" + self.date_ + "+23%3A59%3A59"
        self.body.extend([self.a0, self.a1, self.a2, self.a3, self.a4, self.a5, self.a6, self.a7, self.a8, self.a9,
                          self.a10, self.a11, self.a12, self.a13, self.a14, self.a15, self.a16, self.a17, self.a18,
                          self.a19, self.a20, self.a21, self.a22, self.a23, self.a24, self.a25, self.a26, self.a27,
                          self.a28, self.a29, self.a30, self.a31, self.a32, self.a33, self.a34, self.a35, self.a36,
                          self.a37, self.a38, self.a39, self.a40, self.a41, self.a42, self.a43, self.a44, self.a45,
                          self.a46, self.a47, self.a48, self.a49, self.a50, self.a51, self.a52, self.a53, self.a54,
                          self.a55, self.a56, self.a57, self.a58, self.a59, self.a60, self.a61, self.a62, self.a63,
                          self.a64, self.a65, self.a66, self.a67, self.a68, self.a69, self.a70, self.a71, self.a72,
                          self.a73, self.a74, self.a75, self.a76, self.a77, self.a78, self.a79, self.a80, self.a81,
                          self.a82, ])
        querystring = self.__repr__()
        logger.logger.info(REQUEST_BODY.format(querystring))
        return querystring

    @automation_logger(logger)
    def get_customer_withdrawals(self):
        """
        Builds request body for Crm.get_customer_withdrawals()
        :return: Request body.
        """
        self.a0 = "Echo=2"
        self.a1 = "iColumns=14"
        self.a2 = "sColumns="
        self.a3 = "iDisplayStart=0"
        self.a4 = "iDisplayLength=10"
        self.a5 = "mDataProp_0=id"
        self.a6 = "mDataProp_1=requesteddate"
        self.a7 = "mDataProp_2=confirmeddate"
        self.a8 = "mDataProp_3=datecandec"
        self.a9 = "mDataProp_4=paymentmethod"
        self.a10 = "mDataProp_5=clearingcompany"
        self.a11 = "mDataProp_6=netamount"
        self.a12 = "mDataProp_7=code"
        self.a13 = "mDataProp_8=feeAmount"
        self.a14 = "mDataProp_9=transstatus"
        self.a15 = "mDataProp_10=requestedby"
        self.a16 = "mDataProp_11=ccend"
        self.a17 = "mDataProp_12=referenceNumber"
        self.a18 = "mDataProp_13=comments"
        self.a19 = "sSearch="
        self.a20 = "bRegex=false"
        self.a21 = "sSearch_0="
        self.a22 = "bRegex_0=false"
        self.a23 = "bSearchable_0=true"
        self.a24 = "sSearch_1="
        self.a25 = "bRegex_1=false"
        self.a26 = "bSearchable_1=true"
        self.a27 = "sSearch_2="
        self.a28 = "bRegex_2=false"
        self.a29 = "bSearchable_2=true"
        self.a30 = "sSearch_3="
        self.a31 = "bRegex_3=false"
        self.a32 = "bSearchable_3=true"
        self.a33 = "sSearch_4="
        self.a34 = "bRegex_4=false"
        self.a35 = "bSearchable_4=true"
        self.a36 = "sSearch_5="
        self.a37 = "bRegex_5=false"
        self.a38 = "bSearchable_5=true"
        self.a39 = "sSearch_6="
        self.a40 = "bRegex_6=false"
        self.a41 = "bSearchable_6=true"
        self.a42 = "sSearch_7="
        self.a43 = "bRegex_7=false"
        self.a44 = "bSearchable_7=true"
        self.a45 = "sSearch_8="
        self.a46 = "bRegex_8=false"
        self.a47 = "bSearchable_8=true"
        self.a48 = "sSearch_9="
        self.a49 = "bRegex_9=false"
        self.a50 = "bSearchable_9=true"
        self.a51 = "sSearch_10="
        self.a52 = "bRegex_10=false"
        self.a53 = "bSearchable_10=true"
        self.a54 = "sSearch_11="
        self.a55 = "bRegex_11=false"
        self.a56 = "bSearchable_11=true"
        self.a57 = "sSearch_12="
        self.a58 = "bRegex_12=false"
        self.a59 = "bSearchable_12=true"
        self.a60 = "sSearch_13="
        self.a61 = "bRegex_13=false"
        self.a62 = "bSearchable_13=true"
        self.a63 = "iSortCol_0=1"
        self.a64 = "sSortDir_0=desc"
        self.a65 = "iSortingCols=1"
        self.a66 = "bSortable_0=true"
        self.a67 = "bSortable_1=true"
        self.a68 = "bSortable_2=true"
        self.a69 = "bSortable_3=true"
        self.a70 = "bSortable_4=true"
        self.a71 = "bSortable_5=true"
        self.a72 = "bSortable_6=true"
        self.a73 = "bSortable_7=true"
        self.a74 = "bSortable_8=true"
        self.a75 = "bSortable_9=true"
        self.a76 = "bSortable_10=true"
        self.a77 = "bSortable_11=true"
        self.a78 = "bSortable_12=true"
        self.a79 = "bSortable_13=true"
        self.a80 = "transactionStatuses="
        self.a81 = "datefrom=" + self.past_date + "+00%3A00%3A00"
        self.a82 = "dateto=" + self.date_ + "+23%3A59%3A59"
        self.body.extend([self.a0, self.a1, self.a2, self.a3, self.a4, self.a5, self.a6, self.a7, self.a8, self.a9,
                          self.a10, self.a11, self.a12, self.a13, self.a14, self.a15, self.a16, self.a17, self.a18,
                          self.a19, self.a20, self.a21, self.a22, self.a23, self.a24, self.a25, self.a26, self.a27,
                          self.a28, self.a29, self.a30, self.a31, self.a32, self.a33, self.a34, self.a35, self.a36,
                          self.a37, self.a38, self.a39, self.a40, self.a41, self.a42, self.a43, self.a44, self.a45,
                          self.a46, self.a47, self.a48, self.a49, self.a50, self.a51, self.a52, self.a53, self.a54,
                          self.a55, self.a56, self.a57, self.a58, self.a59, self.a60, self.a61, self.a62, self.a63,
                          self.a64, self.a65, self.a66, self.a67, self.a68, self.a69, self.a70, self.a71, self.a72,
                          self.a73, self.a74, self.a75, self.a76, self.a77, self.a78, self.a79, self.a80, self.a81,
                          self.a82, ])
        querystring = self.__repr__()
        logger.logger.info(REQUEST_BODY.format(querystring))
        return querystring

    @automation_logger(logger)
    def save_customer_information(self, customer, phone: str):
        """
        Builds request body for Crm.update_customer_details()
        :param customer: Customer object.
        :param phone: Customer phone - str (should be without '+' at the began).
        :return:
        """
        self.a0 = "customerData%5B0%5D%5Bid%5D=setFirstname"
        self.a1 = "customerData%5B0%5D%5Bvalue%5D=" + customer.first_name
        self.a2 = "customerData%5B1%5D%5Bid%5D=setLastname"
        self.a3 = "customerData%5B1%5D%5Bvalue%5D=" + customer.last_name
        self.a4 = "customerData%5B2%5D%5Bid%5D=setPersonalid"
        self.a5 = "customerData%5B2%5D%5Bvalue%5D=N%2FA"
        self.a6 = "customerData%5B3%5D%5Bid%5D=setTaxid"
        self.a7 = "customerData%5B3%5D%5Bvalue%5D=TaxId"
        self.a8 = "customerData%5B4%5D%5Bid%5D=setEmail"
        self.a9 = "customerData%5B4%5D%5Bvalue%5D=" + customer.first_name + "_" + customer.last_name + \
                  "%40guerrillamailblock.com"
        self.a10 = "customerData%5B5%5D%5Bid%5D=setPhone"
        self.a11 = "customerData%5B5%5D%5Bvalue%5D=%2B" + phone
        self.a12 = "customerData%5B6%5D%5Bid%5D=setCellphone"
        self.a13 = "customerData%5B6%5D%5Bvalue%5D=%2B" + phone
        self.a14 = "customerData%5B7%5D%5Bid%5D=setHomePhone"
        self.a15 = "customerData%5B7%5D%5Bvalue%5D="
        self.a16 = "customerData%5B8%5D%5Bid%5D=setCity"
        self.a17 = "customerData%5B8%5D%5Bvalue%5D=" + customer.city
        self.a18 = "customerData%5B9%5D%5Bid%5D=setStreet"
        self.a19 = "customerData%5B9%5D%5Bvalue%5D=" + customer.street
        self.a20 = "customerData%5B10%5D%5Bid%5D=setStreettwo"
        self.a21 = "customerData%5B10%5D%5Bvalue%5D=" + customer.street
        self.a22 = "customerData%5B11%5D%5Bid%5D=setPostcode"
        self.a23 = "customerData%5B11%5D%5Bvalue%5D=" + customer.credit_card.postal_code
        self.a24 = "customerData%5B12%5D%5Bid%5D=setGender"
        self.a25 = "customerData%5B12%5D%5Bvalue%5D=" + customer.gender
        self.a26 = "customerData%5B13%5D%5Bid%5D=setCountry"
        self.a27 = "customerData%5B13%5D%5Bvalue%5D=" + str(customer.country_code)
        self.a28 = "customerData%5B14%5D%5Bid%5D=setState"
        self.a29 = "customerData%5B14%5D%5Bvalue%5D=" + customer.state
        self.a30 = "customerData%5B15%5D%5Bid%5D=setLanguage"
        self.a31 = "customerData%5B15%5D%5Bvalue%5D=" + customer.language
        self.a32 = "customerData%5B16%5D%5Bid%5D=setEmployeeinchargeid"
        self.a33 = "customerData%5B16%5D%5Bvalue%5D=" + "0"
        self.body.extend([self.a0, self.a1, self.a2, self.a3, self.a4, self.a5, self.a6, self.a7, self.a8, self.a9,
                          self.a10, self.a11, self.a12, self.a13, self.a14, self.a15, self.a16, self.a17, self.a18,
                          self.a19, self.a20, self.a21, self.a22, self.a23, self.a24, self.a25, self.a26, self.a27,
                          self.a28, self.a29, self.a30, self.a31, self.a32, self.a33, ])
        querystring = self.__repr__()
        logger.logger.info(REQUEST_BODY.format(querystring))
        return querystring

    @automation_logger(logger)
    def save_permissions(self):
        querystring = {
            "sEcho": 1, "iColumns": 6, "sColumns": "", "iDisplayStart": 0, "iDisplayLength": 10, "mDataProp_0": 0,
            "mDataProp_1": 1, "mDataProp_2": 2, "mDataProp_3": 3, "mDataProp_4": 4, "mDataProp_5": 5, "sSearch": "",
            "bRegex": False, "sSearch_0": "", "bRegex_0": False, "bSearchable_0": True, "sSearch_1": "",
            "bRegex_1": False, "bSearchable_1": True, "sSearch_2": "", "bRegex_2": False, "bSearchable_2": True,
            "sSearch_3": "", "bRegex_3": False, "bSearchable_3": True, "sSearch_4": "", "bRegex_4": False,
            "bSearchable_4": True, "sSearch_5": "", "bRegex_5": False, "bSearchable_5": True, "iSortCol_0": 3,
            "sSortDir_0": "desc", "iSortingCols": 1, "bSortable_0": True, "bSortable_1": True, "bSortable_2": True,
            "bSortable_3": True, "bSortable_4": True, "bSortable_5": False, "_": 1559140213845
        }
        logger.logger.info(REQUEST_BODY.format(querystring))
        return querystring
