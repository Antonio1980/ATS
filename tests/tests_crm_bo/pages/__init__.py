from tests.tests_crm_bo.pages.base_page import BasePage

self_management_url = "/dx/users/"
user_management_page_url = BasePage.crm_base_url + self_management_url

self_create_url = "createUser?"
create_user_page_url = user_management_page_url + self_create_url

self_index_url = "index"
user_index_page_url = user_management_page_url + self_index_url
