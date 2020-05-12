from src.base import logger
from src.base.log_decorator import automation_logger
from src.base.services.svc_requests.request_constants import *
from src.base.services.svc_requests.request_schema import ApiRequestSchema


class PaymentServiceRequest(ApiRequestSchema):
    def __init__(self):
        super(PaymentServiceRequest, self).__init__()
        self.method = "Payment."

    @automation_logger(logger)
    def add_card(self, card):
        """
        Build request body for PaymentService.add_credit_card().
        :param card: Credit Card object.
        :return: Request body as json.
        """
        self.method += "AddCard"
        self.params.extend([
            {
                PHONE: card.phone,
                CUSTOMER_EMAIL: card.email,
                CARD_NUMBER: card.card_number,
                CVV: card.cvv,
                EXP_YEAR: card.expiry_year,
                EXP_MONTH: card.expiry_month,
                HOLDER_NAME: card.owner_fn + " " + card.owner_ln,
                ADDRESS: card.street,
                POSTAL_CODE: card.postal_code,
                CITY: card.city,
                COUNTRY: card.country,
                STATE: card.state,
                CURRENCY: card.card_currency,
                PHONE_PREFIX: card.phone_prefix,
                PASSPORT_NUMBER: card.passport_number,
                PERSONAL_ID: card.personal_id
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def cards(self):
        """
        Build request body for PaymentService.get_credit_cards().
        :return: Request body as json.
        """
        self.method += "Cards"
        self.params.extend([
            {
                PAGINATION: {
                    LIMIT: 20,
                    OFFSET: 0
                }
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def upload_credit_card_images(self, card_id: int, file_link: str):
        self.method += "UploadCreditCardImages"
        self.params.extend([
            {
                CARD_ID: card_id,
                FILE_INFO: [{
                    FILE_NAME: file_link,
                    REGULATION_TYPE_ID: 8,
                    REGULATION_PAGE_TYPE_ID: 1,
                    PAGE_NUM: 0
                }],
                REGULATION_TYPE: 4
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def update_credit_card_status(self, card_id: int, card_status: int):
        """
        Build request body for PaymentService.update_credit_card().
        :param card_id: Credit card ID- int.
        :param card_status: 1 - Verified, 2- unverified, 3 - Deleted, 4 - Disabled, 5- expired.
        :return: Request body as json.
        """
        self.method += "UpdateCreditCardStatus"
        self.params.extend([
            {
                CARD_ID: card_id,
                STATUS_ID: card_status
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def deposit_credit_card(self, card, deposit_amount_value, deposit_amount_decimals, currency_id: int):
        """
        Build request body for PaymentService.add_deposit_credit_card().
        :param card: CreditCard object.
        :param deposit_amount_value: Value- int.
        :param deposit_amount_decimals: Precisions- int.
        :param currency_id: Currency ID- int.
        :return: Request body as json.
        """
        self.method += "DepositCreditCard"
        self.params.extend([
            {
                CARD_ID: card.id,
                AMOUNT: {

                    VALUE: deposit_amount_value,
                    DECIMALS: deposit_amount_decimals
                },
                CVV: card.cvv,
                CURRENCY_ID: currency_id,
                ACCEPT_TERMS: True,
                REDIRECT_URL: self.redirection_url
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def withdrawal_cancel(self, withdrawal_id: int):
        """
        Build request body for PostmanClient.withdrawal_cancel().
        :param withdrawal_id: ID int.
        :return: Request body.
        """
        self.method += "WithdrawalCancel"
        self.params.extend([
            {
                WITHDRAWAL_ID: withdrawal_id
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def withdrawal_credit_card(self, card_id: int, withdrawal_amount: float, currency: str):
        """
        Build request body for PaymentService.withdrawal_credit_card().
        :param card_id: Credit card ID- int.
        :param withdrawal_amount: Amount- float.
        :param currency: Currency code- str like "EUR".
        :return: Request body as json.
        """
        self.method += "WithdrawalCreditCard"
        self.params.extend([
            {
                CARD_ID: card_id,
                AMOUNT: withdrawal_amount,
                CURRENCY_CODE: currency
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def withdrawal_credit_card_sms_confirmation(self, withdrawal_token: str):
        """
        Build request body for PaymentService.withdrawal_credit_card_sms_confirmation().
        :param withdrawal_token: Token- str.
        :return: Request body as json.
        """
        self.method += "WithdrawalCreditCardSmsConfirmation"
        self.params.extend([
            {
                TOKEN: withdrawal_token,
                SMS_CODE: "123456"
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def withdrawal_credit_card_resend_sms(self, withdrawal_token: str):
        """
        Build request body for PaymentService.withdrawal_credit_card_resend_sms().
        :param withdrawal_token:
        :return: Request body as json.
        """
        self.method += "WithdrawalCreditCardResendSms"
        self.params.extend([
            {
                TOKEN: withdrawal_token
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def deposit_crypto(self, currency_id: int):
        """
        Build request body for PaymentService.deposit_crypto().
        :param currency_id: Currency ID- int.
        :return: Request body as json.
        """
        self.method += "DepositCrypto"
        self.params.extend([
            {
                CURRENCY_ID: currency_id
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def withdrawal_crypto_sms_confirmation(self, link_: str):
        """

        @param link_:
        @return:
        """
        self.method += "WithdrawalCryptoSmsConfirmation"
        self.params.extend([
            {
                TOKEN: link_,
                SMS_CODE: "123456"
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def withdrawal_crypto_resend_sms(self, withdrawal_token: str):
        """

        @param withdrawal_token:
        @return:
        """
        self.method += "WithdrawalCryptoResendSms"
        self.params.extend([
            {
                TOKEN: withdrawal_token
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def withdrawal_crypto(self, currency_id: int, deposit_amount_value, deposit_amount_decimals, wallet_link: str):
        """

        @param currency_id:
        @param deposit_amount_value:
        @param deposit_amount_decimals:
        @param wallet_link:
        @return:
        """
        self.method += "WithdrawalCrypto"
        # amount = float(amount)
        self.params.extend([
            {
                CURRENCY_ID: currency_id,
                AMOUNT:  {

                    VALUE: deposit_amount_value,
                    DECIMALS: deposit_amount_decimals
                },
                WALLET_ADDRESS: wallet_link,
                URL: self.validation_url
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def withdrawal_wire_sms_confirmation(self, withdrawal_token: str):
        """

        @param withdrawal_token:
        @return:
        """
        self.method += "WithdrawalWireSmsConfirmation"
        self.params.extend([
            {
                TOKEN: withdrawal_token,
                SMS_CODE: "123456"
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def withdrawal_wire_resend_sms(self, withdrawal_token: str):
        """

        @param withdrawal_token:
        @return:
        """
        self.method += "WithdrawalWireResendSms"
        self.params.extend([
            {
                TOKEN: withdrawal_token
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def withdrawal_wire(self, bank, currency_id: int, withdrawal_amount_value, withdrawal_amount_decimals: float):
        """

        @param bank:
        @param currency_id:
        @param withdrawal_amount_value:
        @param withdrawal_amount_decimals:
        @return:
        """
        self.method += "WithdrawalWire"
        self.params.extend([
            {
                DESCRIPTION: "Qa Test",
                ACCOUNT_OWNER_NAME: bank.credit_card.owner_fn + " " + bank.credit_card.owner_ln,
                IBAN: bank.iban,
                BANK_NAME: bank.bank_name,
                BIC: bank.bic,
                ADDRESS: bank.address,
                CURRENCY_ID: currency_id,
                AMOUNT: {

                    "value": withdrawal_amount_value,
                    "decimals": withdrawal_amount_decimals
                },
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def withdrawal_sepa_sms_confirmation(self, withdrawal_token: str):
        """

        @param withdrawal_token:
        @return:
        """
        self.method += "WithdrawalSepaSmsConfirmation"
        self.params.extend([
            {
                TOKEN: withdrawal_token,
                SMS_CODE: "123456"
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def withdrawal_sepa_resend_sms(self, withdrawal_token: str):
        """

        @param withdrawal_token:
        @return:
        """
        self.method += "WithdrawalSepaResendSms"
        self.params.extend([
            {
                TOKEN: withdrawal_token
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def withdrawal_sepa(self, bank, currency_id: int, withdrawal_amount: float):
        """

        @param bank:
        @param currency_id:
        @param withdrawal_amount:
        @return:
        """
        self.method += "WithdrawalSepa"
        self.params.extend([
            {
                CURRENCY_ID: currency_id,
                AMOUNT: withdrawal_amount,
                DESCRIPTION: "QA Test",
                ACCOUNT_OWNER_NAME: bank.credit_card.owner_fn + " " + bank.credit_card.owner_ln,
                ACCOUNT_NUMBER: bank.bank_account,
                BANK_NAME: bank.bank_name,
                BIC: bank.bic,
                ADDRESS: bank.address,
                URL: self.validation_url
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def withdrawal_history(self, method_id, *args):
        """

        @return:
        """
        self.method += "WithdrawalHistory"
        if args and len(args[0]) > 0:
            ((limit, offset, ), ) = args
        else:
            limit, offset = 20, 0
        self.params.extend([
            {
                PAGINATION: {
                    LIMIT: limit,
                    OFFSET: offset
                },
                PAYMENT_METHOD_ID: method_id
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def deposit_history(self, method_id, *args):
        """

        @return:
        """
        self.method += "DepositHistory"
        if args and len(args[0]) > 0:
            ((limit, offset, ), ) = args
        else:
            limit, offset = 20, 0
        self.params.extend([
            {
                PAGINATION: {
                    LIMIT: limit,
                    OFFSET: offset
                },
                PAYMENT_METHOD_ID: method_id
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def fee_history(self, *args):
        """

        @return:
        """
        self.method += "FeeHistory"
        if args and len(args[0]) > 0:
            ((limit, offset, ), ) = args
        else:
            limit, offset = 20, 0
        self.params.extend([
            {
                PAGINATION: {
                    LIMIT: limit,
                    OFFSET: offset
                }
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def export_withdrawal_history(self, method_id):
        """

        @return:
        """
        self.method += "ExportWithdrawalHistory"
        self.params.extend([
            {
                PAYMENT_METHOD_ID: method_id
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def export_deposit_history(self, method_id):
        """

        @return:
        """
        self.method += "ExportDepositHistory"
        self.params.extend([
            {
                PAYMENT_METHOD_ID: method_id
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def export_fee_history(self):
        """

        @return:
        """
        self.method += "ExportFeeHistory"
        self.params.extend([{}])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def portfolio_chat(self, currency_id: int):
        """

        @param currency_id:
        @return:
        """
        self.method += "PortfolioChart"
        self.params.extend([
            {
                FRAME_TYPE: 0,
                CURRENCY: currency_id
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body
