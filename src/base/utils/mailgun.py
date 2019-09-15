import json
import datetime
import requests
from src.base import logger
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger


class MailGun:
    domain = "sandbox7e64c317900647609c225574db67437b.mailgun.org"
    mail_gun_base_url = BaseConfig.MAIL_GUN_URL
    public_key = "pubkey-6f34963bb96ec99c1381f6ece8711924"
    headers = {'Authorization': 'Basic {0}'.format(BaseConfig.MAILGUN_TOKEN)}
    to_timestamp = int(datetime.datetime.today().timestamp())

    @classmethod
    @automation_logger(logger)
    def verify_domain(cls):
        uri = cls.mail_gun_base_url + "domains/" + cls.domain
        try:
            _response = requests.request("PUT", uri, headers=cls.headers)
            body = json.loads(_response.text)
            logger.logger.info("Server responded: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception("verify_domain failed with error: {0}".format(e))
            raise e

    @classmethod
    @automation_logger(logger)
    def get_domains(cls):
        uri = cls.mail_gun_base_url + "domains"
        try:
            _response = requests.request("GET", uri, headers=cls.headers)
            body = json.loads(_response.text)
            logger.logger.info("Server responded: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception("get_domains failed with error: {0}".format(e))
            raise e

    @classmethod
    @automation_logger(logger)
    def get_domain_by_id(cls):
        uri = cls.mail_gun_base_url + "domains/" + cls.domain
        try:
            _response = requests.request("GET", uri, headers=cls.headers)
            body = json.loads(_response.text)
            logger.logger.info("Server responded: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception("get_domain_by_id failed with error: {0}".format(e))
            raise e

    @classmethod
    @automation_logger(logger)
    def get_routes(cls):
        uri = cls.mail_gun_base_url + "routes"
        querystring = {"limit": "0", "skip": "0"}
        try:
            _response = requests.request("GET", uri, headers=cls.headers, params=querystring)
            body = json.loads(_response.text)
            logger.logger.info("Server responded: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception("get_routes failed with error: {0}".format(e))
            raise e

    @classmethod
    @automation_logger(logger)
    def get_route_by_id(cls, route_id):
        uri = cls.mail_gun_base_url + "routes/" + route_id
        querystring = {"id": route_id}
        try:
            _response = requests.request("POST", uri, headers=cls.headers, params=querystring)
            body = json.loads(_response.text)
            logger.logger.info("Server responded: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception("get_route_by_id failed with error: {0}".format(e))
            raise e

    @classmethod
    @automation_logger(logger)
    def get_mailing_lists(cls):
        uri = cls.mail_gun_base_url + "lists/pages"
        querystring = {"limit": "100"}
        try:
            _response = requests.request("GET", uri, headers=cls.headers, params=querystring)
            body = json.loads(_response.text)
            logger.logger.info("Server responded: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception("get_mailing_lists failed with error: {0}".format(e))
            raise e

    @classmethod
    @automation_logger(logger)
    def get_mailing_lists_by_address(cls, address):
        uri = cls.mail_gun_base_url + "lists/" + address
        try:
            _response = requests.request("GET", uri, headers=cls.headers)
            body = json.loads(_response.text)
            logger.logger.info("Server responded: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception("get_mailing_lists failed with error: {0}".format(e))
            raise e

    @classmethod
    @automation_logger(logger)
    def get_events(cls):
        uri = cls.mail_gun_base_url + cls.domain + "/events"
        try:
            _response = requests.request("GET", uri, headers=cls.headers)
            body = json.loads(_response.text)
            logger.logger.info("Server responded: {0}".format(_response))
            return body
        except Exception as e:
            logger.logger.exception("get_events failed with error: {0}".format(e))
            raise e

    @classmethod
    @automation_logger(logger)
    def get_app_events(cls):
        querystring = {
            "h:extended": "true", "h:query": "",
            "begin": str(cls.to_timestamp - 1), "end": str(cls.to_timestamp),
            "limit": "25", "h%3Aquery": "", "h%3Aextended": "true"
        }
        uri = cls.mail_gun_base_url + cls.domain + "/events"
        try:
            _response = requests.request("GET", uri, headers=cls.headers, params=querystring)
            body = json.loads(_response.text)
            logger.logger.info("Server responded: {0}".format(_response))
            return body
        except Exception as e:
            logger.logger.exception("get_events failed with error: {0}".format(e))
            raise e

    @classmethod
    @automation_logger(logger)
    def retrieve_stored_email(cls, storage_url):
        cls.headers.update({"Accept": "message/rfc2822."})
        try:
            _response = requests.request("GET", storage_url, headers=cls.headers)
            body = json.loads(_response.text)
            logger.logger.info("Server responded: {0}".format(_response))
            return body
        except Exception as e:
            logger.logger.exception("get_events failed with error: {0}".format(e))
            raise e

    @classmethod
    @automation_logger(logger)
    def get_logs(cls, recipient):
        uri = cls.mail_gun_base_url + cls.domain + "/events"
        params_ = {"begin": "Fri, 3 May 2013 09:00:00 -0000", "ascending": "yes", "limit": 25, "pretty": "yes",
                   "recipient": recipient}
        try:
            _response = requests.request("GET", uri, params=params_, headers=cls.headers)
            body = json.loads(_response.text)
            logger.logger.info("Server responded: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception("get_logs failed with error: {0}".format(e))
            raise e

    @classmethod
    @automation_logger(logger)
    def send_message(cls, recipient, subject, text_):
        uri = cls.mail_gun_base_url + cls.domain + "/messages"
        data_ = {
            "from": recipient,
            "to": [
                recipient,
                cls.domain],
            "subject": subject,
            "text": text_
        }
        try:
            _response = requests.request("POST", uri, data=data_, headers=cls.headers)
            body = json.loads(_response.text)
            logger.logger.info("Server responded: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception("get_logs failed with error: {0}".format(e))
            raise e

    @classmethod
    @automation_logger(logger)
    def get_true_url(cls, faked_url):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML,like Gecko)'
                                 'Chrome/39.0.2171.95 Safari/537.36'}
        try:
            _response = requests.request("GET", faked_url, headers=headers)
            return _response.request.url
        except Exception as e:
            logger.logger.exception("get_true_url failed with error: {0}".format(e))
            raise e
