import math
from src.base import logger
from src.base.log_decorator import automation_logger


class Calculator:

    @staticmethod
    @automation_logger(logger)
    def value_decimal(input_):
        """
        :param input_: A dictionary with "Value" and "Decimals" representing a number: {'value': 111, 'decimals': 3}
        :return: "Value" and "Decimals" provided transformed to numeric value, float: 0.111
        """
        if len(input_) is not 2:
            return None
        try:
            value = int(input_['value'])
            decimals = int(input_['decimals'])
            result = value / 10 ** decimals
            return result
        except Exception as e:
            logger.logger.error("Value conversion no numeric format has failed:", e)
            pass

    @staticmethod
    @automation_logger(logger)
    def calculate_from_decimals(x, y):
        """
        Calculates price from decimal format to number.
        :param x: price value.
        :param y: price precisions.
        :return: price as a number.
        """
        if y != 0:
            return x / math.pow(10, y)
        else:
            return x

    @staticmethod
    @automation_logger(logger)
    def calculate_decimals(float_):
        """
        Calculates price in decimal format.
        :param float_: value for convert.
        :return: tuple where first index is price value and second index is price precision.
        """
        logger.logger.info("FLOAT".format(float_))
        if float_:
            float_ = float(float_)
        try:
            value = int(''.join(str(float_).split('.')))
            precision = len(str(float_).split('.')[1])
            return value, precision
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} calculate_price_decimals receives only a positive number! {e}")
    
    @staticmethod
    @automation_logger(logger)
    def get_total_price_for_all_order_book(all_price_and_quantity):
        """
        Sum of all prices received from order book for "sell" or "buy"
        :param all_price_and_quantity: array of arrays from order book, 'array of int'
        :return: sum as int .
        """
        sum_ = 0
        for x, y in all_price_and_quantity:
            sum_ += x * y
        return sum_
