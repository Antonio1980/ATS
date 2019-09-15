import time
import random
import pytest
from src.base import logger
from src.base.utils.utils import Utils
from config_definitions import BaseConfig
from src.base.data_bases.sql_db import SqlDb
from src.base.customer.customer import Customer
from src.base.log_decorator import automation_logger


def get_customer():
    return Customer()


@pytest.mark.tool
@pytest.mark.parametrize('i', range(1))
@automation_logger(logger)
def test_generate_customers(i):
    orig_state = random.getstate()
    customer = get_customer()
    random.seed(i)
    step1_response = customer.postman.authorization_service.sign_up_step_1(customer)
    assert step1_response['error'] is None and step1_response['result']['errors'] is None
    customer.customer_id = step1_response['result']['customerId']
    customer.auth_token = step1_response['result']['token']
    customer.get_postman_access(customer.auth_token)
    Utils.get_mail_gun_item(customer)
    step2_response = customer.postman.authorization_service.verify_email_step_2(customer.email, customer.ver_token)
    assert step2_response['error'] is None and step2_response['result']['errors'] is None
    time_ = time.perf_counter() + float(BaseConfig.PHONE_DELAY)
    step3_response = customer.postman.authorization_service.add_phone_step_3(customer)
    while step3_response['error'] is not None or step3_response['result']['errors'] is not None and time_ > \
            time.perf_counter():
        step3_response = customer.postman.authorization_service.add_phone_step_3(customer)
    step4_response = customer.postman.authorization_service.verify_phone_step_4()
    assert step4_response['error'] is None and step4_response['result']['errors'] is None
    step5_response = customer.postman.authorization_service.update_personal_details_step_5(customer)
    assert step5_response['error'] is None and step5_response['result']['errors'] is None
    step6 = customer.postman.authorization_service.client_checklist_step6()
    assert step6['error'] is None and step6['result']['errors'] is None
    link1 = customer.postman.file_service.upload_file(BaseConfig.DOCUMENT_PNG)['link']
    link2 = customer.postman.file_service.upload_file(BaseConfig.DOCUMENT_JPG)['link']
    link3 = customer.postman.file_service.upload_file(BaseConfig.DOCUMENT_PNG)['link']
    step7_response = customer.postman.authorization_service.upload_documents_step_7(link1, link2, link3)
    assert step7_response['error'] is None and step7_response['result']['errors'] is None
    step8_response = customer.postman.authorization_service.login_by_credentials(customer.email, customer.password)
    assert step8_response['error'] is None
    customer.auth_token = step8_response['result']['token']
    assert SqlDb.customer_approval(customer.customer_id)

    random.setstate(orig_state)
    
    logger.logger.info("Customer successfully created.")
    logger.logger.info("{0}, {1}, {2}".format(customer.email, customer.password, customer.customer_id))
    Utils.save_into_file(customer.email + "," + customer.password + "," + str(customer.customer_id) + "\n",
                         customer.output_file)
