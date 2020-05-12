import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger


@pytest.mark.usefixtures("r_time_count", "r_customer")
@pytest.mark.payment_service
class TestUploadCreditCardImages(object):

    card_id = None
    link_image = None
    image = BaseConfig.DOCUMENT_PNG

    @allure.step("")
    @automation_logger(logger)
    def test_upload_image_to_file_service(self, r_customer):
        response_ = r_customer.postman.file_service.upload_file(self.image)
        assert response_['link']
        TestUploadCreditCardImages.link_image = response_['link']

    @allure.step("")
    @automation_logger(logger)
    def test_add_credit_card(self, r_customer):
        response_ = r_customer.postman.payment_service.add_credit_card(r_customer.credit_card)
        assert response_['error'] is None
        TestUploadCreditCardImages.card_id = response_['result']['card']['id']

    @allure.step("")
    @automation_logger(logger)
    def test_upload_credit_card_images_method_works(self, r_customer):
        response_ = r_customer.postman.payment_service.upload_credit_card_images(TestUploadCreditCardImages.card_id,
                                                                                 TestUploadCreditCardImages.link_image)
        assert response_['error'] is None
        