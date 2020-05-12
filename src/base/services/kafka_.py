import json
import requests
import datetime
from src.base import logger, kafka_base_url
from src.base.log_decorator import automation_logger


class KafkaService:
    kafka_proxy = "/kafka/"
    kafka_url = kafka_base_url + kafka_proxy
    kafka_headers = {'Content-Type': 'application/json'}
    
    @automation_logger(logger)
    def get_supported_topics(self):
        """

        :return:
        """
        _url = self.kafka_url + "supported-topics"
        try:
            _response = requests.get(_url, headers=self.kafka_headers)
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception(F"{e.__class__.__name__} get_supported_topics failed with error: {e}")
            raise e

    @automation_logger(logger)
    def get_last_topic_record(self, topic):
        """

        @param topic:
        @return:
        """
        _url = self.kafka_url + "topics/" + topic + "/last-records"
        try:
            _response = requests.get(_url, headers=self.kafka_headers)
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception(F"{e.__class__.__name__} get_last_topic_record failed with error: {e}")
            raise e

    @automation_logger(logger)
    def send_subtract_transaction_operations(self, kafka_transaction):
        """

        :param kafka_transaction:
        :return:
        """
        _url = self.kafka_url + "topics/subtract_transaction_operations"
        payload = {
            "amount": str(kafka_transaction.amount),
            "currencyId": kafka_transaction.currency_id,
            "customerId": kafka_transaction.customer_id,
            "operationReference": kafka_transaction.operation_reference,
            "time": int(datetime.datetime.today().timestamp()),
            "transactionGuid": kafka_transaction.guid,
            "type": kafka_transaction.type_id
        }
        try:
            _response = requests.post(_url, data=json.dumps(payload), headers=self.kafka_headers)
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} send_subtract_transaction_operations failed with error: {e}")
            raise e
