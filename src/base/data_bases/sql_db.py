import random
import string
import arrow
import pymysql
from config_definitions import BaseConfig
from src.base import logger
from src.base.automation_error import AutomationError
from src.base.log_decorator import automation_logger


class SqlDb:
    # Connector for SQL DB.
    connection = pymysql.connect(host=BaseConfig.SQL_HOST, port=int(BaseConfig.SQL_PORT),
                                 user=BaseConfig.SQL_USERNAME, passwd=BaseConfig.SQL_PASSWORD,
                                 database=BaseConfig.SQL_DB, charset='utf8mb4', autocommit=True)

    @classmethod
    @automation_logger(logger)
    def run_mysql_query(cls, query):
        """
        To run SQL query on MySQL DB.
        :param query: SQL query.
        :return: data from executed query.
        """
        # Ignore "Not closed socket connection" warning.
        # warnings.simplefilter("ignore", ResourceWarning)
        # SQL client- connector for MySQL DB.
        with cls.connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            if rows:
                return rows

    @classmethod
    @automation_logger(logger)
    def get_withdrawals_by_customer(cls, customer_id, payment_method_id, currency_id=None):
        query_ = F"SELECT * FROM withdrawals WHERE customerId = {customer_id} " \
            F"AND paymentMethodId = {payment_method_id} AND currencyId LIKE '%{currency_id}' ORDER BY dateInserted DESC"
        try:
            return cls.run_mysql_query(query_)
        except Exception as e:
            error_message = "get_withdrawals_by_customer from MYSQL has failed: {0}"
            logger.logger.error(error_message.format(e))
            raise AutomationError(error_message, e)

    @classmethod
    @automation_logger(logger)
    def get_orders_by_customer_mysql(cls, customer_id, order_status, filled_quantity=None):
        """
        Get  orders by customer ID provided from MySQL DB
        :param order_status: order status
        :param filled_quantity:
        :param customer_id:
        :return: orders as they are stored in DB - a tuple. The output can be converted to list of "order" objects
        using orders_data_converter.
        filled_quantity:
        no param - get orders with zero filled quantity.
        1 - get orders where  quantity>filledQuantity > 0
        2 - get orders where  quantity = filledQuantity (filled)
        3 - get all orders with the given status disregarding of order filled quantity.
        """
        if filled_quantity == 1:
            query = F"SELECT * FROM orders WHERE customerId = {customer_id} AND filledQuantity > 0 AND filledQuantity "\
                F"< quantity AND statusId = {order_status} ORDER BY executionDate DESC;"

        elif filled_quantity == 2:
            query = F"SELECT * FROM orders WHERE customerId = {customer_id} AND filledQuantity = quantity " \
                F"and statusId = {order_status} order by executionDate DESC;"

        elif filled_quantity == 3:
            query = F"SELECT * FROM orders WHERE customerId = {customer_id} AND statusId = {order_status} " \
                F"ORDER BY executionDate DESC;"

        else:
            query = F"SELECT * FROM orders WHERE customerId = {customer_id} AND filledQuantity = 0 AND statusId = " \
                F"{order_status} ORDER BY executionDate DESC;"

        try:
            return cls.run_mysql_query(query)
        except Exception as e:
            error_message = "get_orders from MYSQL has failed: {0}"
            logger.logger.error(error_message.format(e))

    @classmethod
    @automation_logger(logger)
    def get_trades_by_customer_mysql(cls, customer_id):
        """
        Get all trades by customer ID provided from MySQL DB.
        :param customer_id:
        :return: trades as they are stored in DB - a tuple.
        """
        query = F"SELECT * FROM trades_crypto WHERE customerId = {customer_id} ORDER BY executionDate DESC;"
        try:
            return cls.run_mysql_query(query)
        except Exception as e:
            error_message = "get_trades from MYSQL has failed: {0}"
            logger.logger.error(error_message.format(e))

    @classmethod
    @automation_logger(logger)
    def get_order_by_id(cls, order_id):
        """
        Return an order from MySQL DB by order ID (tuple).
        :param order_id:
        :return: order with provided ID.
        """
        query = F"SELECT * FROM orders WHERE id = {order_id};"
        try:
            return cls.run_mysql_query(query)
        except Exception as e:
            logger.logger.error("get_order_by_id from MYSQL has failed: {0}".format(e))

    @classmethod
    @automation_logger(logger)
    def get_trade_by_order_id(cls, order_id):
        """

        :param order_id:
        :return:
        """
        query = F"SELECT * FROM trades_crypto WHERE orderId = {order_id};"
        try:
            return cls.run_mysql_query(query)
        except Exception as e:
            logger.logger.error("get_order_by_id from MYSQL has failed: {0}".format(e))

    @classmethod
    @automation_logger(logger)
    def customer_approval(cls, customer_id):
        """
        Receives list of customer ID's and updates  to status "approval".
        :param customer_id: list of customers ID's.
        :return: True if all successful and False otherwise.
        """
        if not isinstance(customer_id, list):
            customer_id = [customer_id]
        try:
            for i in customer_id:
                cls.run_mysql_query("UPDATE customers SET status = 3 WHERE id=" + str(i) + ";")
                logger.logger.info("Customer {0} successfully approved.".format(i))
            return True
        except Exception as e:
            logger.logger.error("{0} customer_approval failed with error: {1} ".format(e.__class__.__name__,
                                                                                       e.__cause__), e)

    @classmethod
    @automation_logger(logger)
    def change_customer_phone(cls, customer_id, cellphone, phone=None):
        """
        Connects to SQL and updates phone, cellphone for provided customer ID.
        :param customer_id: Customer ID- str.
        :param cellphone: Cellphone number- str.
        :param phone: Phone- str (optional, by default copy of cellphone).
        :return: True if all successful and False otherwise.
        """
        phone = cellphone if phone is None else phone
        try:
            cls.run_mysql_query(
                F"UPDATE customers SET cellphone = '{cellphone}', phone = '{phone}' WHERE id = {customer_id};")
            logger.logger.info("Cellphone of Customer {0} successfully updated.".format(customer_id))
            return True
        except Exception as e:
            logger.logger.error("{0} change_mobile failed with error: {1} ".format(e.__class__.__name__, e.__cause__),
                                e)
            return False

    @classmethod
    @automation_logger(logger)
    def add_customer_deposit_sql(cls, customer_id, currency_id, amount):
        """
        Connects to SQL DB and inserts value for provided customer_id.
        :param customer_id: Id of customer for insert.
        :param currency_id: Id of currency for balance.
        :param amount: amount of deposit to insert.
        :return: True if all successful and False otherwise.
        """
        customer_id, currency_id, amount = str(customer_id), str(currency_id), str(amount)
        date = arrow.utcnow()
        _ = "0000-00-00 00:00:00"
        cur_date = date.format('YYYY-MM-DD')
        cur_date_full = date.format('YYYY-MM-DD HH:mm:ss')
        id_ = ''.join(random.choice(string.digits) for _ in range(6))
        query = "INSERT INTO deposits(id, customerId, paymentMethodId, clearingCompanyId, currencyId, amount, rateUSD,"\
                "rateEUR, rateBTC, referenceNumber, statusId, sourceId, IPAddress, balanceChangeTransactionGuid, " \
                "comments, canceledByWId, cancelingWId, addedBy, updatedBy, confirmedBy, canceledBy, cancelReasonId, " \
                "cancelReason, declinedBy, declineReason, dateConfirmed, dateValue, dateCanceled, dateDeclined, " \
                "dateInserted, dateUpdated) VALUES(" + id_ + ", " + customer_id + ", 3, 0, " + currency_id + ", " + \
                amount + ", 0.00012500, 0.00014388, 1.00000000, '2134776', 2, 3, '10.244.10.1', '', '', 0, 0, 9, 9, 9,"\
                         "0, 0, '', 0, '', '" + cur_date_full + "', '" + cur_date + "', '" + _ + "', '" + _ + "', '" + \
                cur_date_full + "', '" + cur_date_full + "');"
        cls.run_mysql_query(query)
        logger.logger.info("Deposit {0} was added successfully, for customer: {1} ".format(amount, customer_id))
        return True

    @classmethod
    @automation_logger(logger)
    def get_quantity_tail_digits(cls, instrument_id):
        """
        Connects to SQL DB and get value for quantity tail_digits of instrument.
        :param instrument_id: Id of instrument as int.
        :return: quantity tail_digits of instrument.
        """
        base_currency = \
            cls.run_mysql_query(F"SELECT name FROM instruments WHERE id = {instrument_id};")[0][0].split('/')[0]
        tail_digits = \
            cls.run_mysql_query(F"SELECT tailDigits FROM currencies WHERE code = '{base_currency}';")[0][0]

        return tail_digits

    @classmethod
    @automation_logger(logger)
    def get_price_tail_digits(cls, instrument_id):
        """
        Connects to SQL DB and get value for price tail_digits of instrument.
        :param instrument_id: Id of instrument as int.
        :return: price tail_digits of instrument.
        """
        instrument_name_query = F"SELECT name FROM instruments WHERE id = {instrument_id};"

        instrument_name = str(cls.run_mysql_query(instrument_name_query)[0][0])

        tail_digits = \
            cls.run_mysql_query(F"SELECT tailDigits FROM assets WHERE name = '{instrument_name}';")[0][0]
        return tail_digits

    @classmethod
    @automation_logger(logger)
    def update_reference_price_by_instrument(cls, instrument_id):
        """
        Connects to SQL DB and get Reference Price value by instrument id.
        :param instrument_id: Id of instrument as int.
        :return: Reference Price value before update.
        """
        reference_price_before = float(cls.run_mysql_query(
            F"SELECT referencePriceRatio FROM instruments WHERE id = {instrument_id};")[0][0])

        cls.run_mysql_query(F"UPDATE instruments SET referencePriceRatio = 1.50000000 WHERE id = {instrument_id};")

        return reference_price_before

    @classmethod
    @automation_logger(logger)
    def get_currency_by_instrument(cls, instrument_id):
        """
        Receives an instrument ID, returns base and quoted currency ID's.
        :param instrument_id:
        :return: base currency ID, quoted currency ID.
        """
        try:

            instrument_query = f"SELECT * FROM instruments WHERE id = {instrument_id};"

            asset_name = cls.run_mysql_query(instrument_query)[0][2]

            asset_query = f"SELECT baseCurrencyId, quotedCurrencyId FROM assets WHERE name = '{asset_name}';"

            instrument_currencies = cls.run_mysql_query(asset_query)

            base_currency = str(instrument_currencies[0][0])

            quoted_currency = str(instrument_currencies[0][1])

            return int(base_currency), int(quoted_currency)

        except Exception as e:
            logger.logger.error(F"Failed to extract currencies from instrument {instrument_id}", e)
            return False

    @classmethod
    @automation_logger(logger)
    def get_transaction_fees(cls, currency_id, fee_type=None):
        """
        This method can be used to get deposit ar withdrawal fee size.
        :param currency_id:
        :param fee_type: one of the fee types that are currently exist in the system - ccDepositFee, wireWithdrawalFee.
        :return: List of fee sizes or one fee size if specific fee type is provided. Returns False on failure.
        """

        if fee_type is not None:
            query = f"SELECT {fee_type} FROM params_deposit_withdrawal_fees WHERE currencyId = {currency_id};"
        else:
            query = f"SELECT * FROM params_deposit_withdrawal_fees WHERE currencyId = {currency_id};"

        try:
            result = cls.run_mysql_query(query)
            return list(result[0])

        except Exception as e:
            logger.logger.error(F"Failed to get the required fee size for currency {currency_id}", e)
            return False

    @classmethod
    @automation_logger(logger)
    def get_min_order_amount(cls, instrument_id):
        """
        Connects to SQL DB and get value min of order amount of instrument.
        :param instrument_id: Id of instrument as int.
        :return: min order of instrument as float.
        """
        instrument_name_query = F"SELECT name FROM instruments WHERE id = {instrument_id};"
        instrument_name = str(cls.run_mysql_query(instrument_name_query)[0][0])
        min_order_amount = \
            (cls.run_mysql_query(
                F"SELECT minOrderQuantity FROM instruments WHERE name = '{instrument_name}';")[0][0])
        return float(min_order_amount)

    @classmethod
    @automation_logger(logger)
    def get_membership_fee_size(cls, fee_plan, is_discounted):
        """
        Method returns membership fee size by Fee Plan and Fee Mode (Discounted / Regular)
        :param fee_plan:
        :param is_discounted:
        :return: Membership Fee size.
        """
        if is_discounted:
            query = f"SELECT * FROM local_config WHERE `key` = 'fee.periodic.dxex.plan.{fee_plan}';"
        else:
            query = f"SELECT * FROM local_config WHERE `key` = 'fee.periodic.plan.{fee_plan}';"

        try:
            result = cls.run_mysql_query(query)
            return result[0][3]

        except Exception as e:
            logger.logger.error(F"Failed to get membership fee size: {e}")
            return False

    @classmethod
    @automation_logger(logger)
    def get_cumulative_fee_by_trade(cls, trade_id, convert=None):
        """
        Returns Cumulative Fee by Trade ID. Converts the Fee to USD if the "convert" flag is provided.
        :param convert:
        :param trade_id:
        :return:
        """
        query = F"SELECT * FROM fees WHERE fees.tradeId = {trade_id};"

        try:
            result = cls.run_mysql_query(query)
            if result is not None and convert:
                return result[0][5] * result[0][8]
            elif result is not None:
                return result[0][5]
            else:
                return 0

        except Exception as e:
            logger.logger.error(F"Failed to get cumulative fee size: {e}")
            return False

    @classmethod
    @automation_logger(logger)
    def get_currency_tail_digits(cls, currency_id):
        """
        Provides tail digits for the selected currency.

        :param currency_id:
        :return: tail digits.
        """
        query = f"select * from currencies where id = {currency_id}"

        try:
            result = cls.run_mysql_query(query)
            if result is not None:
                return result[0][8]

        except Exception as e:
            logger.logger.error(F"Failed to get currency tail digits: {e}")
            return False

    @classmethod
    @automation_logger(logger)
    def get_currencies_list(cls):

        query = f"select id from currencies"

        try:
            result = cls.run_mysql_query(query)
            if result is not None:
                return [int(x[0]) for x in result]

        except Exception as e:
            logger.logger.error(F"Failed to get currencies list: {e}")
            return False

    @classmethod
    @automation_logger(logger)
    def set_cumulative_fee_dxchash_disabled(cls, id_, step_usd=None, fee=None):
        """
        Set Fee or/and Step USD for Regular Cumulative Fee.
        :param id_: as int, 7 - step One, 8 - step Two, 11 - step Three
        :param step_usd: as float
        :param fee: as float
        :return: True. Returns False on failure.
        """
        query_1 = (F"UPDATE params_cumulative_fee SET stepUsd = {step_usd}, feeMultiplier = {fee} WHERE id = "
                   F"{id_} and feePlanId = 2;")
        query_2 = F"UPDATE params_cumulative_fee SET feeMultiplier = {fee} WHERE id = {id_} and feePlanId = 2;"
        query_3 = F"UPDATE params_cumulative_fee SET stepUsd = {step_usd} WHERE id = {id_} and feePlanId = 2;"

        try:
            if step_usd is not None and fee is not None:
                cls.run_mysql_query(query_1)
                return True
            elif step_usd is None and fee is not None:
                cls.run_mysql_query(query_2)
                return True
            elif step_usd is not None and fee is None:
                cls.run_mysql_query(query_3)
                return True
        except Exception as e:
            logger.logger.error(F"set_cumulative_fee_dxchash_enabled", e)
            return False

    @classmethod
    @automation_logger(logger)
    def get_id_trade_by_order_id(cls, order_id):
        """
        Provides trade Id from DB by order Id

        :param order_id:
        :return: trade_id as str
        """
        query = F"SELECT id FROM trades_crypto WHERE orderId = {order_id};"
        try:
            result = cls.run_mysql_query(query)
            if result is not None:
                return result[0][0]

        except Exception as e:
            logger.logger.error(F"Failed to get_id_trade_by_order_id: {e}")
            return False

    @classmethod
    @automation_logger(logger)
    def get_fee_amount_by_trade(cls, trade_id):
        """
        Provides fee amount  from DB by Trade Id

        :param trade_id:
        :return: fee amount as float
        """
        query = F"SELECT feeAmount FROM fees WHERE tradeId = {trade_id};"
        try:
            result = cls.run_mysql_query(query)
            if result is not None:
                return float(result[0][0])

        except Exception as e:
            logger.logger.error(F"Failed to get_fee_amount_by_trade: {e}")
            return False

    @classmethod
    @automation_logger(logger)
    def get_currency_name_by_currency_id(cls, currency_id):
        """
        Provides currency name by currency id

        :param currency_id: currency id
        :return: currency name as string
        """
        query = F"SELECT code FROM currencies WHERE id = {currency_id};"
        try:
            result = cls.run_mysql_query(query)
            if result is not None:
                return str(result[0][0])

        except Exception as e:
            logger.logger.error(F"Failed to get_currency_name_by_currency_id: {e}")
            return False
