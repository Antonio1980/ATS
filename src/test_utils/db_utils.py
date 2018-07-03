import pymysql
from tests.test_definitions import BaseConfig


def run_mysql_query(self, query):
    _host = BaseConfig.DB_HOST
    _username = BaseConfig.DB_USERNAME
    _password = BaseConfig.DB_PASSWORD
    _db_name = BaseConfig.DB_NAME
    _port = 30002
    connection = pymysql.connect(host=_host, port=_port, user=_username, passwd=_password,
                                 database=_db_name)
    rows = []
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
    finally:
        connection.commit()
        connection.close()
        return rows
