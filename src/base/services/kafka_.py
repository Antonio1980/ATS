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


# if __name__ == '__main__':
#     from src.base.equipment.transaction import Transaction
#
#     t = Transaction().set_transaction(type_id=1, customer_id=100001100000020929, currency_id=2,
#                                       amount=500.0, guid="AAA-2698ghsd7", operation_reference="")
#     k = KafkaService().send_subtract_transaction_operations(t).to_json()
#     from config_definitions import BaseConfig
#     from src.base.equipment.kafka_transaction import Transaction
#     k = KafkaService()
#     # topics = k.get_supported_topics()
#     # print(topics)
#     # records = k.get_last_topic_record("subtract_transaction_operations")
#     # print(records)
# 
#     transaction_initialize = Transaction()
#     transaction_initialize.set_transaction(
#         1, BaseConfig.CUSTOMER_ID, 1, 500.0, "0-AAAAAAA9yRY=", transaction_initialize.__repr__())
#     sub = k.send_subtract_transaction_operations(transaction_initialize)
#     print(sub)