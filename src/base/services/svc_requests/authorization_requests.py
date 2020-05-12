from src.base import logger
from src.base.log_decorator import automation_logger
from src.base.services.svc_requests.request_constants import *
from src.base.services.svc_requests.request_schema import ApiRequestSchema


class AuthorizationServiceRequest(ApiRequestSchema):
    def __init__(self):
        super(AuthorizationServiceRequest, self).__init__()
        self.method = "Authorization."

    @automation_logger(logger)
    def session_data(self):
        """
        Sending a request to retrieve customer's session data.
        @return: request body as json dump string.
        """
        self.method += "SessionData"
        self.params.extend([])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def enable_tfa_step_1(self, password):
        """

        @param password: String.
        @return: request body as json dump string.
        """
        self.method += "EnableTwoFactorAuthentication"
        self.params.extend([
            {
                STEP: 1,
                SEND_CODE: {
                    TYPE: 0,
                    PASSWORD: password
                }
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def enable_tfa_step_2(self, state: bool):
        """
        # This method is used to create a request that enables the tfa . Enabled in 2 steps.  Step 2.
        :param state: Turn- On/Turn- Off
        :return: request body as json dump string.
        """
        self.method += "EnableTwoFactorAuthentication"
        self.params.extend([
            {
                STEP: 2,
                VALIDATE_CODE: {
                    TYPE: 0,
                    ENABLE: state,
                    CODE: "123456"
                }
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def login_by_credentials(self, email, password):
        """

        :param email:
        :param password:
        :return: request body as json dump string.
        """
        self.method += "LoginByCredentials"
        self.params.extend([
            {
                LOGIN: email,
                PASSWORD: password,
                CAPTCHA: "captcha"
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def login_by_tfa_token(self, tfa_token: str):
        """

        :param tfa_token:
        :return: request body as json dump string.
        """
        self.method += "LoginByTwoFactorToken"
        self.params.extend([
            {
                TOKEN: tfa_token,
                STEP: 2,
                CODE: "123456"
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def login_by_token(self, api_token: str, secret: str):
        """

        :param api_token:
        :param secret:
        :return: request body as json dump string.
        """
        self.method += "LoginByToken"
        self.params.extend([
            {
                TOKEN: api_token,
                SECRET: secret
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def log_out(self):
        """

        :return: request body as json dump string.
        """
        self.method += "Logout"
        self.params.extend([])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def generate_password_hash(self, email: str, password: str):
        """

        :param email:
        :param password:
        :return: request body as json dump string.
        """
        self.method += "GeneratePasswordHash"
        self.params.extend([
            {
                LOGIN: email,
                PASSWORD: password
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def update_personal_details(self, customer):
        """

        :param customer:
        :return: request body as json dump string.
        """
        self.method += "UpdatePersonalDetails"
        self.params.extend([
            {
                FIRST_NAME: customer.first_name,
                MIDDLE__NAME: customer.last_name,
                DATE_OF_BIRTH: customer.birthday_timestamp,
                LAST_NAME: customer.last_name,
                COUNTRY: customer.country_code,
                STATE: customer.state_code,
                GENDER: customer.gender,
                ADDRESS: customer.street,
                ADDRESS_TWO: customer.street,
                CITY: customer.city,
                ZIP_CODE: customer.zip_,
                PHONE: customer.full_phone,
                TAX_ID: "TaxId"
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def validate_token(self, auth_token: str):
        """

        :param auth_token:
        :return: request body as json dump string.
        """
        self.method += "ValidateToken"
        self.params.extend([
            {
                TOKEN: auth_token
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def step_one(self, customer):
        """

        :param customer:
        :return: request body as json dump string.
        """
        self.method += "SignUp"
        try:
            self.params.extend([
                {
                    FIRST_NAME: customer.first_name,
                    LAST_NAME: customer.last_name,
                    EMAIL: customer.email,
                    PASSWORD: customer.password,
                    ACCEPT_TERMS: True,
                    CAPTCHA: "test_test",
                    SITE_LANGUAGE: customer.language,
                    EMAIL_VALIDATION_URL: self.validation_url,
                    REFER_LINK: self.validation_url,
                    RECEIVE_PROMO_SMS: False,
                    RECEIVE_PROMO_PUSH_MOBILE: False,
                    RECEIVE_PROMO_EMAIL: False,
                    TRADING_EMAILS: False
                }
            ])
            body = self.to_json()
            logger.logger.info(REQUEST_BODY.format(body))
            return body
        except AttributeError as e:
            raise e

    @automation_logger(logger)
    def step_two(self, email: str, ver_token: str):
        """

        :param email:
        :param ver_token:
        :return: request body as json dump string.
        """
        self.method += "SignUpStep"
        self.params.extend([
            {
                STEP: 2,
                VERIFY_EMAIL:
                    {
                        TOKEN: ver_token,
                        EMAIL: email
                    }
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def step_three(self, customer):
        """

        :param customer:
        :return: request body as json dump string.
        """
        self.method += "SignUpStep"
        self.params.extend([
            {
                ADD_PHONE:
                    {
                        COUNTRY: customer.country_code,
                        PHONE: customer.full_phone,
                        SITE_LANGUAGE: customer.language
                    }
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def step_four(self):
        """

        :return: request body as json dump string.
        """
        self.method += "SignUpStep"
        self.params.extend([
            {
                VERIFY_PHONE:
                    {
                        CODE: "123456"
                    }
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def step_five(self, customer):
        """

        :param customer:
        :return: request body as json dump string.
        """
        self.method += "SignUpStep"
        self.params.extend([
            {
                "UpdatePersonalDetails":
                    {
                        FIRST_NAME: customer.first_name,
                        LAST_NAME: customer.last_name,
                        DATE_OF_BIRTH: customer.birthday_timestamp,
                        COUNTRY: customer.country_code,
                        ADDRESS: customer.street,
                        ADDRESS_TWO: customer.street,
                        GENDER: customer.gender,
                        CITY: customer.city,
                        ZIP_CODE: customer.zip_,
                        PHONE: customer.full_phone,
                        TAX_ID: "TaxId",
                        US_TAXT_REPORTER: False,
                        POLITACALLY_TAX_REPORTER: False,
                        SITE_LANGUAGE: customer.language,
                        STATE: customer.state_code
                    }
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def step_six(self):
        """

        :return: request body as json dump string.
        """
        self.method += "SignUpStep"
        self.params.extend([
            {
                "answerQuestionnaire": {
                    "formId": 1,
                    "answers": [
                        {
                            "questionId": 16,
                            "predefinedResponse": [
                                72
                            ]
                        },
                        {
                            "questionId": 18,
                            "predefinedResponse": [
                                76
                            ]
                        }
                    ]
                }
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def step_seven(self, link1: str, link2: str, link3: str):
        """

        :param link1:
        :param link2:
        :param link3:
        :return: request body as json dump string.
        """
        self.method += "SignUpStep"
        self.params.extend([
            {
                "uploadDocuments": {
                    "folderType": "regulation",
                    "fileInfo": [
                        {
                            "fileName": link1,
                            "regulationDocTypeId": 1,
                            "regulationDocPageTypeId": 1,
                            "pageNum": 0
                        },
                        {
                            "fileName": link2,
                            "regulationDocTypeId": 1,
                            "regulationDocPageTypeId": 2,
                            "pageNum": 0
                        },
                        {
                            "fileName": link3,
                            "regulationDocTypeId": 2,
                            "regulationDocPageTypeId": 1,
                            "pageNum": 0
                        }
                    ]
                }
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def get_needed_files(self):
        """

        :return: request body as json dump string.
        """
        self.method += "GetNeededFiles"
        self.params.extend([])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def get_questionnaire(self):
        """

        :return: request body as json dump string.
        """
        self.method += "GetQuestionnaire"
        self.params.extend([])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def change_email_step1(self):
        """

        :return: request body as json dump string.
        """
        self.method += "ChangeEmail"
        self.params.extend([
            {
                STEP: 1,
                SEND_SMS: {}
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def change_email_step2(self):
        """

        :return: request body as json dump string.
        """
        self.method += "ChangeEmail"
        self.params.extend([
            {
                STEP: 2,
                CHECK_SMS: {
                    CODE: "123456"
                }
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def change_email_step3(self, email_token: str, email: str):
        """

        :return: request body as json dump string.
        """
        self.method += "ChangeEmail"
        self.params.extend([
            {
                STEP: 3,
                SEND_EMAIL: {
                    TOKEN: email_token,
                    EMAIL: email,
                    LINK: self.validation_url
                }
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def change_email_step4(self, ver_token: str):
        """

        :return: request body as json dump string.
        """
        self.method += "ChangeEmail"
        self.params.extend([
            {
                STEP: 4,
                CHECK_EMAIL: {
                    TOKEN: ver_token
                }
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def change_phone_step1(self):
        """

        :return: request body as json dump string.
        """
        self.method += "ChangePhone"
        self.params.extend([
            {
                STEP: 1,
                SEND_SMS: {}
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def change_phone_step2(self):
        """

        :return: request body as json dump string.
        """
        self.method += "ChangePhone"
        self.params.extend([
            {
                STEP: 2,
                CHECK_SMS: {
                    CODE: "123456"
                }
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def change_phone_step3(self, phone_token: str, full_phone: str):
        """

        :return: request body as json dump string.
        """
        self.method += "ChangePhone"
        self.params.extend([
            {
                STEP: 3,
                SEND_NEW_SMS: {
                    TOKEN: phone_token,
                    PHONE: full_phone
                }
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def change_phone_step4(self):
        """

        :return: request body as json dump string.
        """
        self.method += "ChangePhone"
        self.params.extend([
            {
                STEP: 4,
                CHECK_NEW_SMS: {
                    CODE: "123456"
                }
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def resend_sms(self):
        """

        :return: request body as json dump string.
        """
        self.method += "ResendSms"
        self.params.extend([])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def resend_email(self):
        """

        :return: request body as json dump string.
        """
        self.method += "ResendEmail"
        self.params.extend([])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def forgot_password_step1(self, email):

        """

        :return: request body as json dump string.
        """
        self.method += "ForgotPassword"
        self.params.extend([
            {
                EMAIL: email,
                FORGOT_PASSWORD_URL: self.forgot_password_page_url
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def forgot_password_step2(self, email, ver_token, new_password):

        """

        :return: request body as json dump string.
        """
        self.method += "RestorePassword"
        self.params.extend([
            {
                EMAIL: email,
                TOKEN: ver_token,
                PASSWORD: new_password,
                CONFIRM_PASSWORD: new_password
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def reset_password(self):
        """

        :return: request body as json dump string.
        """
        self.method += "ResetPassword"
        self.params.extend([])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def change_password(self, password, new_password):
        """

        :return: request body as json dump string.
        """
        self.method += "ChangePassword"
        self.params.extend([
            {
                CURRENT_PASSWORD: password,
                NEW_PASSWORD: new_password,
                CONFIRM_PASSWORD: new_password
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def change_subscriptions(self, email_option, sms_option, mobile_option):
        """

        :return: request body as json dump string.
        """
        self.method += "ChangeCustomerSubscription"
        self.params.extend([
            {
                RECEIVE_PROMO_EMAIL: email_option,
                RECEIVE_PROMO_SMS: sms_option,
                RECEIVE_PROMO_PUSH_MOBILE: mobile_option
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def get_login_logs(self):
        """

        :return: request body as json dump string.
        """
        self.method += "GetCustomerLoginLogs"
        self.params.extend([])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def reset_phone(self):
        """

        :return: request body as json dump string.
        """
        self.method += "SignUpResetPhone"
        self.params.extend([])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def signup_step_back(self):
        """

        :return: request body as json dump string.
        """
        self.method += "SignUpStepBack"
        self.params.extend([])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body
