import json
import base64
import requests
from src.base import logger
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger

tests_run = BaseConfig.TESTRAIL_RUN


class TestRail:
    user = BaseConfig.TESTRAIL_USER
    password = BaseConfig.TESTRAIL_PASSWORD
    test_rail_key = BaseConfig.TESTRAIL_KEY
    test_rail_base_url = BaseConfig.TEST_RAIL_URL
    auth = str(base64.b64encode(bytes('%s:%s' % (user, password), 'utf-8')), 'ascii').strip()
    headers = {'Content-Type': 'application/json', 'Authorization': 'Basic %s' % auth}

    @classmethod
    @automation_logger(logger)
    def update_test_case(cls, test_run=tests_run, test_case='0', status=0):
        """
        Calls TestRail API to send HTTP request with updated status of given test case..
        :param test_run: current test run.
        :param test_case: current test case.
        :param status: test actual result.
        :return: API response as json.
        """
        res = " PASSED !!!" if status == 1 else " FAILED !!!"
        try:
            uri = cls.test_rail_base_url + "/index.php?/api/v2/add_result_for_case/" + test_run + "/" + test_case
            payload = {
                "status_id": str(status),
                "comment": "This test ID: " + test_case + res
            }
            _response = requests.request("POST", uri, data=payload, headers=cls.headers)
            body = json.loads(_response.text)
            logger.logger.info("Server responded: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception("update_test_case failed with error: {0}".format(e))
            raise e

    @classmethod
    @automation_logger(logger)
    def get_test_case(cls, test_case):
        """
        Send GET request to TestRail.
        :param test_case: test case ID.
        :return: API response.
        """
        uri = cls.test_rail_base_url + "/index.php?/api/v2/get_case/" + str(test_case)
        try:
            _response = requests.request("GET", uri, headers=cls.headers)
            body = json.loads(_response.text)
            logger.logger.info("Server responded: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception("get_test_case failed with error: {0}".format(e))
            raise e
