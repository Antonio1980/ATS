from tests.tests_crm_bo.pages.base_page import BasePage

base_url = BasePage().crm_base_url
customer_id = BasePage().customer_id

self_management_url = "/dx/users/"
user_management_page_url = base_url + self_management_url

self_create_url = "createUser?"
create_user_page_url = user_management_page_url + self_create_url

self_index_url = "index"
user_index_page_url = user_management_page_url + self_index_url

self_home_url = "/dx/dashboard"
home_page_url = base_url + self_home_url

self_login_url = "/dx/login"
login_page_url = base_url + self_login_url

self_customer_url = "/dx/customers/page/"
customer_page_url = base_url + self_customer_url
customer_admin_url = customer_page_url + "{0}#customer_admin_status".format(customer_id)
customer_deposit_url = customer_page_url + "{0}#customer_dw".format(customer_id)
customer_balance_url = customer_page_url + "{0}#customer_balance".format(customer_id)
