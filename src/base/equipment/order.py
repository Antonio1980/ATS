import random
import datetime
from src.base import logger
from src.base.utils.calculator import Calculator
from src.base.log_decorator import automation_logger


class Order(object):
    
    def __init__(self):
        self.type = 0
        self.external_id = ""
        self.internal_id = 0
        self.direction = 0
        self.q_value = 0
        self.q_precision = 0
        self.quantity = 0
        self.p_value = 0
        self.p_precision = 0
        self.price = 0
        self.instrument_id = 0
        self.coefficient = 0
        self.date_created = datetime.date.today().strftime("%Y-%m-%d")
        self.customer_id = 0
        self.status = ""
        self.filled_quantity = 0
        self.time_in_force = ""
        self.balance_change_transaction_id = ""

    def __repr__(self):
        return F"Order(type: {self.type}, price: [pure-{self.price}, p_value-{self.p_value}, " \
            F"p_presc.-{self.p_precision}], quantity: [pure-{self.quantity}, q_value-{self.q_value}, " \
            F"q_presc.-{self.q_precision}], order_id: {self.external_id}, internal_id: {self.internal_id}, " \
            F"direction: {self.direction}, instrument_id: {self.instrument_id}, date_created: {self.date_created}), "\
            F"customer ID: {self.customer_id}, order status: {self.status}, direction: {self.direction},  "\
            F"filled quantity: {self.filled_quantity}, time in force: {self.time_in_force}," \
            F" transaction id: {self.balance_change_transaction_id}"

    @automation_logger(logger)
    def set_order(self, direction, instrument_id, quantity, price=None, *args):
        """

        @param direction:
        @param instrument_id:
        @param quantity:
        @param price:
        @return:
        """
        self.quantity = quantity
        self.direction = direction
        self.instrument_id = instrument_id
        q_res = Calculator.calculate_decimals(quantity)
        self.q_value = q_res[0]
        self.q_precision = q_res[1]
        self.type = 1
        if price:
            self.price = round(price, 4)
            p_res = Calculator.calculate_decimals(self.price)
            self.p_value = p_res[0]
            self.p_precision = p_res[1]
            self.type = 2

        if args and len(args) >= 7:
            (self.customer_id, self.status, self.filled_quantity, self.time_in_force,
             self.balance_change_transaction_id, self.internal_id, self.external_id,  *args) = args

        logger.logger.info(F"Order was set to {self.__repr__()}")
        return self

    @automation_logger(logger)
    def add_random_price_coefficient(self):
        logger.logger.info(F"Order before coefficient {self.__repr__()}")
        if self.price:
            pass
        else:
            self.price = Calculator.calculate_from_decimals(self.p_value, self.p_precision)
        self.coefficient = (self.price / 100) * random.randrange(0, 20)
        self.price += self.coefficient
        self.p_value, self.p_precision = Calculator.calculate_decimals(round(self.price, 4))
        logger.logger.info(F"Order after coefficient {self.__repr__()}")
        return self

    @automation_logger(logger)
    def clean_up_order_price(self):
        logger.logger.info(F"Order before clean up {self.__repr__()}")
        self.price -= self.coefficient
        self.p_value, self.p_precision = Calculator.calculate_decimals(round(float(self.price), 4))
        logger.logger.info(F"Order after clean up {self.__repr__()}")
        return self

    @staticmethod
    @automation_logger(logger)
    def orders_data_converter(orders):
        """
        Data converter. Converts the output received from DB when queried for orders
        to list of "order" objects. Several new properties are added to the object
        to store all the data  received  from DB.
        :param orders: FB Query result tuple
        :return: list of "order" objects
        """
        if orders:
            try:
                return [
                    Order().set_order(order[8], order[2], order[10], order[9], order[1], order[6], order[11],
                                      order[12], order[13], order[0], order[7]) for order in orders]
            except Exception as e:
                logger.logger.error("orders_data_conversion has failed:", e)
                raise e

    @staticmethod
    @automation_logger(logger)
    def orders_builder(orders_dict, direction):
        return [
            Order().set_order(direction, order["instrument_id"], order["quantity"], order["price"])
            for order in list(orders_dict["orders"])
        ]
