import csv
import time
import json
import codecs
import random
import string
import datetime
import platform
from faker import Faker
from src.base import logger
from bs4 import BeautifulSoup
from config_definitions import BaseConfig
from src.base.enums import OperationSystem
from src.base.utils.mailgun import MailGun
from src.base.log_decorator import automation_logger
from src.base.automation_error import AutomationError


class Utils:
    customer = None
    mail_gun_cli = MailGun()

    @staticmethod
    @automation_logger(logger)
    def detect_os():
        """
        Detects the OS on which Python tests will run.
        :return: enum string value of OS name.
        """
        current_platform = platform.system().lower()
        if current_platform == OperationSystem.DARWIN.value:
            return OperationSystem.DARWIN.value
        elif current_platform == OperationSystem.WINDOWS.value:
            return OperationSystem.WINDOWS.value
        elif current_platform == OperationSystem.LINUX.value:
            return OperationSystem.LINUX.value
        else:
            e = AutomationError("The OS is not detected!")
            logger.logger.exception(e)
            raise e

    @staticmethod
    @automation_logger(logger)
    def to_json(object_):
        """
        Converts a class object to JSON object.
        :param object_: a class instance.
        :return: a JSON object (python dictionary).
        """
        return json.dumps(object_, default=lambda o: vars(o), sort_keys=True, indent=4)

    @staticmethod
    @automation_logger(logger)
    def read_json_config(json_file):
        with open(json_file) as f:
            json_dict = json.load(f)
        return json_dict

    @staticmethod
    @automation_logger(logger)
    def to_timestamp():
        """
        Makes two timestamp integers.
        :return: timestamp_from- int (1 year back from now), timestamp_to- int (current date).
        """
        timestamp_from = int(time.mktime((datetime.date.today() - datetime.timedelta(days=365)).timetuple()))
        timestamp_to = int(datetime.datetime.today().timestamp())
        return timestamp_from, timestamp_to

    @staticmethod
    @automation_logger(logger)
    def get_dates():
        """

        :return:
        """
        date_ = datetime.date.today().strftime("%Y-%m-%d")
        past_date = (datetime.date.today() - datetime.timedelta(days=365)).strftime("%Y-%m-%d")
        return date_, past_date

    @staticmethod
    @automation_logger(logger)
    def get_csv_data(data_file):
        """
        Allows to get data from csv file.
        :param data_file: csv data file.
        :return: list of rows from csv.
        """
        rows = []
        with open(data_file) as csv_data:
            content = csv.reader(csv_data)
            # skipping first row
            next(content, None)
            for row in content:
                rows.append(row)
        return rows

    @staticmethod
    @automation_logger(logger)
    def get_data(data_file):
        """
        Allows to get data from csv file.
        :param data_file: csv data file.
        :return: list of rows from csv.
        """
        rows = []
        with open(data_file) as csv_data:
            content = csv.reader(csv_data)
            for row in content:
                rows.append(row)
        return rows

    @staticmethod
    @automation_logger(logger)
    def get_account_details(data_file, row):
        """
        Allows to get data from provided csv file.
        :param row: Needed row from the file.
        :param data_file: File to write data.
        :return: dictionary object: email, password, customer_id (in case of wtp file) and username (in case of crm),
        sid_token, timestamp.
        """
        rows = []
        with open(data_file) as csv_data:
            content = csv.reader(csv_data)
            for item in content:
                rows.append(item)
        email = rows[row][0]
        password = rows[row][1]
        customer_id = rows[row][2]
        return {'email': email, 'password': password, 'customer_id': customer_id}

    @staticmethod
    @automation_logger(logger)
    def save_stream_into_file(process, file):
        """
        Allows to write data into a file.
        :param process: python process in 'UTF-8' encoding
        :param file: any file.
        """
        with codecs.open(file, "a", "utf-8") as f:
            f.write(process)
            f.flush()

    @staticmethod
    @automation_logger(logger)
    def save_into_file(result, file):
        """
        Allows to insert (top) a string into the provided file.
        :param result: string to append.
        :param file: file to append for.
        """
        with open(file, "r+") as f:
            s = f.read()
            f.seek(0)
            f.write(result + s)

    @staticmethod
    @automation_logger(logger)
    def generate_user_first_last_name():
        """
        Creates random user first and last_name.
        :return: user first_last_name as a string.
        """
        fake = Faker('en_US')
        name = fake.name()
        if '.' in name:
            name = name.replace('.', '')
        return name

    @staticmethod
    @automation_logger(logger)
    def get_faked_phone(culture='he_IL'):
        """
        Creates customized phone number.
        :type culture: option for localization like: 'he_IL' for Israel
        :return: phone number as a string.
        """
        fake = Faker(culture)
        phone = fake.phone_number()
        if ' ' in phone:
            phone = phone.replace(' ', '')
        if 'x' in phone:
            phone = phone.split('x')[0]
        if '-' in phone:
            phone = phone.replace('-', '')
        if len(phone) < 10:
            phone += '0'
        return phone

    @staticmethod
    @automation_logger(logger)
    def random_string_generator(size=8, chars=string.ascii_lowercase + string.digits):
        """
        Generates random string with chars and digits.
        :param size: string length expected (default is 8).
        :param chars: string characters consistency.
        :return: random string.
        """
        return ''.join(random.choice(chars) for _ in range(size))

    @classmethod
    @automation_logger(logger)
    def write_file_preconditions(cls, rows, email_suffix):
        """
        Allows to create crm_users_preconditions.csv file with random data.
        :param rows: rows number to create.
        :param email_suffix: email service provider.
        """
        language, permissions, status, user_type = "eng", "sup", "act", "Admin"
        header = "first_last_name,phone,email,username,language,permissions,status,user_type\n"
        file = BaseConfig.CRM_USERS_PRECONDITIONS
        with open(file, "w") as f:
            f.write(header)
        with open(file, "a") as my_file:
            for i in range(rows):
                first_last_name = '_'.join(cls.generate_user_first_last_name().split(' '))
                phone = cls.get_faked_phone()
                email = first_last_name + email_suffix
                username = first_last_name
                body = F"{first_last_name},{phone},{email},{username},{language},{permissions},{status},{user_type}"
                my_file.write(body)
        return file

    @classmethod
    @automation_logger(logger)
    def parse_html(cls, html: str) -> BeautifulSoup:
        """
        HTML parser, converts a string (if it html content) to HTML object.
        :param html: string with html content.
        :return: HTML object.
        """
        return BeautifulSoup(html, 'html.parser')

    @classmethod
    @automation_logger(logger)
    def parse_ver_token(cls, html, crm=None):
        """
        Used to unpack verification url from customer email.
        :param html: BeautifulSoup html object.
        :param crm: True or False
        :return: verification url from customer email.
        """
        parsed_html = cls.parse_html(html)
        if crm:
            return parsed_html
        return parsed_html.center.find_all('a')[1]['href']

    @classmethod
    @automation_logger(logger)
    def get_mail_gun_item(cls, customer, forgot=None, crm=None, left_time_seconds=300.0):
        if left_time_seconds > 0:

            try:
                time.sleep(10.0)
                emails_response = cls.mail_gun_cli.get_events()['items']

                start_time = time.perf_counter()

                for email in emails_response:
                    if forgot:
                        if customer.email == email['message']['headers']['to'] and \
                                email['message']['headers']['subject'] == 'Forgot Password':
                            cls.this_email = email
                            break
                    elif crm:
                        if customer.email == email['message']['headers']['to'] or \
                                "CRM" in email['message']['headers']['subject']:
                            cls.this_email = email
                            break
                    else:
                        if customer.email == email['message']['headers']['to'] and \
                                email['message']['headers']['subject'] == 'Verify Email' or \
                                email['message']['headers']['subject'] == 'Email change confirmation':
                            cls.this_email = email
                            break
                else:
                    end_time = time.perf_counter() - start_time
                    cls.get_mail_gun_item(customer, forgot, left_time_seconds - end_time)

                storage_url = cls.this_email['storage']['url']
                storage_response = cls.mail_gun_cli.retrieve_stored_email(storage_url)
                html = storage_response['body-html']
                faked_url = cls.parse_ver_token(html, crm)
                if crm:
                    return faked_url
                cls.ver_url = cls.mail_gun_cli.get_true_url(faked_url)
                assert cls.ver_url is not None, "URL with ver_token not received."

                if cls.ver_url.count('=') == 2 or "changeEmailConfirmation" in cls.ver_url:
                    customer.ver_token = cls.ver_url.split('=')[1].split('&')[0]
                elif cls.ver_url.count('=') == 3:
                    customer.ver_token = cls.ver_url.split('=')[2].split('&')[0]

                return cls.ver_url
            except Exception as e:
                logger.logger.error(F"{e.__class__.__name__} get_mail_gun_item failed error: {e}")
                raise e
