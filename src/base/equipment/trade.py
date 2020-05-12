from src.base import logger
from src.base.log_decorator import automation_logger


class Trade(object):
    
    def __init__(self):
        self.id = 0
        self.direction = ""
        self.customer_id = ""
        self.instrument_id = ""
        self.price = ""
        self.quantity = ""
        self.status_id = ""
        self.rate_usd_base = ""
        self.rate_usd_quoted = ""
        self.rate_dxex_base = ""
        # self.rate_dxex_quoted = ""
        self.balance_change_transaction = ""
        self.execution_date = ""
        self.orderId = ""

    def __repr__(self):
        return F"Trade ID: {self.id}, direction: {self.direction}, customer ID: {self.customer_id}, " \
               F"Execution Date: {self.execution_date}, Price: {self.price}, Quantity: {self.quantity}, " \
               F"Trade Status: {self.status_id}, Rate USD Base: {self.rate_usd_base}, Rate USD Quoted: " \
               F"{self.rate_usd_quoted}, Balance Transaction: {self.balance_change_transaction}, Instrument ID: " \
               F"{self.instrument_id}, Order ID: {self.orderId}, Rate DXEX Base: {self.rate_dxex_base}"

    @automation_logger(logger)
    def set_trade(self, direction, instrument_id, quantity, price, *args):
        self.quantity = quantity
        self.direction = direction
        self.instrument_id = instrument_id
        self.price = price

        if args and len(args) >= 9:
            (self.id, self.customer_id, self.status_id, self.rate_usd_base,
             self.rate_usd_quoted, self.orderId, self.execution_date,
             self.balance_change_transaction, self.rate_dxex_base, *args) = args

        logger.logger.info(F"Trade was set to {self.__repr__()}")
        return self

    @staticmethod
    @automation_logger(logger)
    def trades_data_converter(trades):
        """
        Data converter. Converts the output received from DB when queried for trades
        to list of "trade" objects. Several new properties are added to the object
        to store all the data  received  from DB.
        :param trades: FB Query result tuple
        :return: list of "trade" objects
        """
        if trades:
            try:
                return [
                    Trade().set_trade(trade[1], trade[3], trade[8], trade[7], trade[0],
                                      trade[2], trade[9], trade[10], trade[13], trade[4],
                                      trade[5], trade[16], trade[12]) for trade in trades
                ]

            except Exception as e:
                logger.logger.error("trades_data_conversion has failed:", e)
                raise e
