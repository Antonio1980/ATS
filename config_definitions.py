import os
import configparser
from src import src_dir
from tests import test_dir


def get_parser(config):
    parser = configparser.ConfigParser()
    with open(config, mode='r', buffering=-1, closefd=True):
        parser.read(config)
        return parser


test_dir += "/"
repository_dir = src_dir + "/repository"
drivers_dir = src_dir + "/drivers"
scripts_dir = src_dir + "/scripts"
files_dir = src_dir + "/repository/files"
logs_dir = src_dir + "/repository/logs"


class BaseConfig:

    config_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.cfg')
    parser = get_parser(config_file)

    ME_BASE_URL = parser.get('BASE_URL', 'base_url_me')
    CRM_BASE_URL = parser.get('BASE_URL', 'base_url_crm')
    BO_BASE_URL = parser.get('BASE_URL', 'base_url_bo')
    API_BASE_URL = parser.get('BASE_URL', 'api_base_url')
    WTP_BASE_URL = parser.get('BASE_URL', 'wtp_base_url')
    BROWSER_STACK = parser.get('BASE_URL', 'browser_stack_url')
    BALANCE_SERVICE_IP = parser.get('BASE_URL', 'balance_service_ip')
    FILE_SERVICE_IP = parser.get('BASE_URL', 'file_service_ip')
    FILE_SERVICE_HOST = parser.get('BASE_URL', 'file_service_host')
    DX_SITE_URL = parser.get('BASE_URL', 'dx_site_url')
    COINS_MARKETPLACE_URL = parser.get('BASE_URL', 'coins_marketplace_url')
    GITLAB_URL = parser.get('BASE_URL', 'gitlab_url')
    GITLAB_URL_CRM = parser.get('BASE_URL', 'gitlab_url_crm')
    KAFKA_URL = parser.get('BASE_URL', 'kafka_url')
    MAIL_GUN_URL = parser.get('BASE_URL', 'mail_gun_url')
    PROD_API_URL = parser.get('BASE_URL', 'api_prod_url')
    R_DRIVER_URL = parser.get('BASE_URL', 'r_driver_url')
    F_12_DRIVER_URL = parser.get('BASE_URL', 'f_12_driver')
    K8S_HOST = parser.get('BASE_URL', 'k8s_host')

    W_CHROME_PATH = drivers_dir + parser.get('WEB_DRIVER_WIN', 'w_chrome')
    W_FIREFOX_PATH = drivers_dir + parser.get('WEB_DRIVER_WIN', 'w_firefox')
    W_IE_PATH = drivers_dir + parser.get('WEB_DRIVER_WIN', 'w_ie')
    W_EDGE_PATH = drivers_dir + parser.get('WEB_DRIVER_WIN', 'w_edge')
    W_JS_PATH = drivers_dir + parser.get('WEB_DRIVER_WIN', 'w_js')

    L_CHROME_PATH = drivers_dir + parser.get('WEB_DRIVER_LIN', 'l_chrome')
    L_FIREFOX_PATH = drivers_dir + parser.get('WEB_DRIVER_LIN', 'l_firefox')

    M_CHROME_PATH = drivers_dir + parser.get('WEB_DRIVER_MAC', 'm_chrome')
    M_FIREFOX_PATH = drivers_dir + parser.get('WEB_DRIVER_MAC', 'm_firefox')

    SELENIUM_JAR = drivers_dir + parser.get('TEST_DATA', 'selenium_jar')

    WTP_LOGIN_DATA = files_dir + parser.get('TEST_DATA', 'me_login_data')
    CRM_LOGIN_DATA = files_dir + parser.get('TEST_DATA', 'crm_login_data')
    FORGOT_PASSWORD_DATA = files_dir + parser.get('TEST_DATA', 'forgot_data')
    ME_LOGIN_DATA = files_dir + parser.get('TEST_DATA', 'me_login_data')
    OPEN_ACCOUNT_DATA = files_dir + parser.get('TEST_DATA', 'open_account_data')
    WTP_TESTS_CUSTOMERS = files_dir + parser.get('TEST_DATA', 'wtp_tests_customers')
    CRM_TESTS_USERS = files_dir + parser.get('TEST_DATA', 'crm_tests_users')
    CRM_USERS_PRECONDITIONS = files_dir + parser.get('TEST_DATA', 'crm_users_preconditions')
    BROWSERS = files_dir + parser.get('TEST_DATA', 'browsers')
    PHONES = files_dir + parser.get('TEST_DATA', 'phones')
    PHONE_CODES = files_dir + parser.get('TEST_DATA', 'phone_codes')
    TOOL_OUTPUT_FILE = files_dir + parser.get('TEST_DATA', 'tool_output_file')
    INSTRUMENT_PRICES_PROD = files_dir + parser.get('TEST_DATA', 'instrument_prices')

    MM_CONFIG = test_dir + parser.get('TEST_DATA', 'mm_config_json')

    DOCUMENT_JPG = files_dir + parser.get('FILES', 'document_jpg')
    DOCUMENT_PNG = files_dir + parser.get('FILES', 'document_png')
    DOCUMENT_PDF = files_dir + parser.get('FILES', 'document_pdf')

    TEST_TOKEN = parser.get('TOKEN', 'test_token')
    BAR_TOKEN = parser.get('TOKEN', 'bar_token')
    MAILGUN_TOKEN = parser.get("TOKEN", "mailgun_token")

    CRM_USERNAME = parser.get('CRM', 'crm_username')
    CRM_PASSWORD = parser.get('CRM', 'crm_password')

    EMAIL = parser.get('ISOLATED', 'email')
    PASSWORD = parser.get('ISOLATED', 'password')
    CUSTOMER_ID = parser.get('ISOLATED', 'customer_id')

    SQL_HOST = parser.get('SQL', 'host')
    SQL_PORT = parser.get('SQL', 'port')
    SQL_USERNAME = parser.get('SQL', 'username')
    SQL_PASSWORD = parser.get('SQL', 'password')
    SQL_DB = parser.get('SQL', 'db_name')

    REDIS_HOST = parser.get('REDIS', 'host')
    REDIS_PORT = parser.get('REDIS', 'port')

    KAFKA_HOST = parser.get('KAFKA', 'host')
    KAFKA_PASSWORD = parser.get('KAFKA', 'kafka_password')

    TEST_RAIL_URL = parser.get('TESTRAIL', 'test_rail_url')
    TESTRAIL_KEY = parser.get('TESTRAIL', 'test_rail_key')
    TESTRAIL_USER = parser.get('TESTRAIL', 'user')
    TESTRAIL_PASSWORD = parser.get('TESTRAIL', 'password')
    TESTRAIL_RUN = parser.get('TESTRAIL', 'test_run')

    CARD_NUMBER = parser.get('CREDIT_CARD', 'card_number')
    CVV = parser.get('CREDIT_CARD', 'cvv')
    CVV2 = parser.get('CREDIT_CARD', 'cvv2')
    EXPIRY_YEAR = parser.get('CREDIT_CARD', 'expiry_year')
    EXPIRY_MONTH = parser.get('CREDIT_CARD', 'expiry_month')

    IBAN = parser.get('BANK', 'iban')
    BIC = parser.get('BANK', 'bic')
    ACCOUNT = parser.get('BANK', 'account')

    MM_DELAY = parser.get('ARGS', 'mm_delay')
    UI_DELAY = parser.get('ARGS', 'ui_delay')
    CRM_DELAY = parser.get('ARGS', 'crm_delay')
    PHONE_DELAY = parser.get('ARGS', 'phone_delay')

    PROD_EMAIL = parser.get('PROD', 'email')
    PROD_PASSWORD = parser.get('PROD', 'password')
    PROD_CUSTOMER_ID = parser.get('PROD', 'customer_id')

    ME_VM_HOST = parser.get('ME', 'host')
    ME_VM_PORT = parser.get('ME', 'port')
    ME_USERNAME = parser.get('ME', 'username')
    ME_PASSWORD = parser.get('ME', 'password')

    POSTGRESQL_HOST = parser.get('POSTGRESQL', 'host')
    POSTGRESQL_USERNAME = parser.get('POSTGRESQL', 'username')
    POSTGRESQL_PASSWORD = parser.get('POSTGRESQL', 'password')
