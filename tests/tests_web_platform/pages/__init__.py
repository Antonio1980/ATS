from tests.tests_web_platform.pages.base_page import BasePage


base_url = BasePage().wtp_base_url
_self_account_url = "/openAccountDx.html"
wtp_open_account_url = base_url + _self_account_url

_self_dashboard_url = "/exchange.html"
_self_home_url = "?nr_insight=0&fullPlugin=1"
wtp_dashboard_url = base_url + _self_dashboard_url
wtp_home_page_url = wtp_dashboard_url + _self_home_url

_self_signin_url = "/login.html"
wtp_signin_page_url = base_url + _self_signin_url

_self_forgot_page_url = "/forgotPasswordDx.html"
forgot_password_page_url = base_url + _self_forgot_page_url

_self_user_page_url = "?lang=en"
user_page_url = wtp_dashboard_url + _self_user_page_url

signin_user_page_url = wtp_signin_page_url + _self_user_page_url

user_open_account_url = wtp_open_account_url + _self_user_page_url
