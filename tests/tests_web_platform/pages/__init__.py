from tests.tests_web_platform.pages.base_page import BasePage


base_url = BasePage().wtp_base_url

_self_dashboard_url = "/exchange.html"
_self_home_url = "/exchange.html?nr_insight=0&fullPlugin=1"
wtp_home_page_url = base_url + _self_home_url
wtp_dashboard_url = base_url + _self_dashboard_url

_self_login_url = "/sign_in.html"
wtp_login_page_url = base_url + _self_login_url

_self_forgot_page_url = "/forgotPasswordDx.html"
forgot_password_page_url = base_url + _self_forgot_page_url