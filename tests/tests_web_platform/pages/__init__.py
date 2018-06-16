from tests.tests_web_platform.pages.base_page import BasePage


base_url = BasePage().wtp_base_url

self_home_url = "exchange.html?nr_insight=0&fullPlugin=1"
wtp_home_page_url = base_url + self_home_url

self_login_url = "login.html"
wtp_login_page_url = base_url + self_login_url

self_account_url = "openAccountDx.html"
wtp_open_account_url = base_url + self_account_url