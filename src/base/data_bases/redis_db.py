import json
import time
import redis
import datetime
from src.base import logger
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger


class RedisDb:
    # Connector for Redis DB.
    redis_client = redis.StrictRedis(host=BaseConfig.REDIS_HOST, decode_responses=True, port=BaseConfig.REDIS_PORT)

    @classmethod
    @automation_logger(logger)
    def delete_redis_key(cls, key):
        """
        Deletes the provided Key  in Redis.
        Related value is removed as well 
        :param key:
        """
        key = str(key) if not isinstance(key, str) else key
        try:
            cls.redis_client.delete(key)
        except Exception as e:
            logger.logger.error(f"Failed to delete the provided Redis key: {e}")
            raise e

    @classmethod
    @automation_logger(logger)
    def get_orders_by_customer_redis(cls, customer_id):
        """
        Get all orders by customer ID  provided from redis.
        :param customer_id:
        :return: list of orders in JSON
        """
        redis_param = "orders_{" + str(customer_id) + "}"
        try:
            orders = cls.redis_client.hgetall(redis_param)
            result = list(orders.values())
            return result
        except Exception as e:
            logger.logger.error(f"get_orders from Redis has failed: {e}")
            raise e

    @classmethod
    @automation_logger(logger)
    def add_customer_balance_redis(cls, customer_id: int, currency_id: int, amount: float) -> bool:
        """
        Connects to Redis DB to set value by provided key:_customer_id.
        :param customer_id: redis DB key.
        :param currency_id: Id of currency for balance.
        :param amount: amount of deposit - float
        """
        customer_id = str(customer_id)
        cur_balance = cls.redis_client.hget('balance_{' + customer_id + '}', currency_id)
        balance = float(cur_balance) + float(amount) if cur_balance else float(amount)
        cls.redis_client.hset('balance_{' + customer_id + '}', currency_id, balance)
        added_balance = cls.redis_client.hget('balance_{' + customer_id + '}', currency_id)
        if float(added_balance) == balance:
            logger.logger.info(F"Balance was added successfully, current balance: {added_balance}")
            return True
        else:
            logger.logger.error("Error occurred with add_customer_balance...")
            return False

    @classmethod
    @automation_logger(logger)
    def get_customer_balance_redis(cls, customer_id, currency_id):
        """
        Method can be used to check customer's balance in Redis for selected currency.
        Returns customer's available and frozen balance as a tuple: (available_balance, frozen_balance).

        :param customer_id:
        :param currency_id:
        :return:
        """
        customer_id = str(customer_id)

        try:
            total_balance = cls.redis_client.hget('balance_{' + customer_id + '}', currency_id)
            frozen_balance = cls.redis_client.hget('frozen_balance_{' + customer_id + '}', currency_id)

        except Exception as e:
            logger.logger.error(f"Get balance  from Redis has failed: {e}")
            raise e

        if total_balance is None: total_balance = 0
        if frozen_balance is None: frozen_balance = 0

        return float(total_balance) - float(frozen_balance), float(frozen_balance)

    @classmethod
    @automation_logger(logger)
    def get_orders_best_price_and_quantity(cls, instrument_id, direction, consistence):
        """
        Get price and quantity from order book (redis), direction accordingly.
        :param instrument_id: Instrument ID- int.
        :param direction: "sell" or "buy" - str.
        :param consistence: 1 - for single price, 2 - for array of prices
        :return: if consistence = 1 - array where [0] - "best price" and [1] - "quantity" for order (item),
        else - array of arrays with all items from order book.
        """
        try:
            flag = None
            if direction.lower() == 'buy':
                flag = direction
                order_book = cls.redis_client.execute_command(
                    'cx.sdrange orderbook_' + str(instrument_id) + '_sell 0 -1')
            else:
                order_book = cls.redis_client.execute_command(
                    'cx.sdrrange  orderbook_' + str(instrument_id) + '_buy 0 -1')

            temp_list = [(lambda x: float(x))(x) for x in order_book]

            temp_list = [temp_list[i:i + 2] for i in range(0, len(temp_list), 2)]

            order_book = sorted([[z, y] for z, y in temp_list if y != 0.0])

            if flag:
                if len(order_book) >= 1:
                    return order_book[0] if consistence == 1 else order_book
            else:
                if len(order_book) >= 1:
                    return sorted(order_book, reverse=True)[0] if consistence == 1 else sorted(order_book, reverse=True)
        except Exception as e:
            logger.logger.error(f"get_orders_best_price_and_quantity failed: {e}")
            raise e

    @classmethod
    @automation_logger(logger)
    def get_price_last_trade(cls, instrument_id):
        """
        Get price of last trade from Last trades (redis).
        :param instrument_id: Instrument ID- int.
        :return:  price of last trade - float
        """
        try:
            return json.loads(cls.redis_client.execute_command('lrange lastTrades_' + str(instrument_id) + ' 0 -1')[0])[
                'price']
        except ValueError or IndexError or TypeError as e:
            logger.logger.error(F"get_price_last_trade failed with error: {e}")
            raise e

    @classmethod
    @automation_logger(logger)
    def set_price_last_trade(cls, instrument_id, price):
        """
        Sets the price of the last trade on the selected instrument to the desired value.
        :param instrument_id:
        :param price:
        """
        if price:
            try:
                '''{"price":0.00030000, "quantity": 2, "direction": "BUY", "timestamp": 1560341871275051}'''
                instrument = F"lastTrades_{str(instrument_id)}"
                param_buy = ' { "price": ' + str(price) + ', "quantity": 0.25, ' \
                            '"direction": "BUY", "timestamp": ' + str(int(datetime.datetime.today().timestamp())) + ' }'

                param_sell = ' { "price": ' + str(price) + ', "quantity": 0.25, ' \
                             '"direction": "SELL", "timestamp": ' + str(int(datetime.datetime.today().timestamp())) +'}'
                cls.redis_client.lpush(instrument, param_buy)
                cls.redis_client.lpush(instrument, param_sell)
            except Exception as e:
                logger.logger.error(f"set_price_last_trade has failed: {e}")
                raise e

    @classmethod
    @automation_logger(logger)
    def set_ticker_last_price(cls, instrument_id, price):
        """
        Modifies the ticker on the selected instrument the Redis.
        All params on Platform taken from ticker are change accordingly
        :param instrument_id:
        :param price:
        """
        if price:
            timestamp = str(int(datetime.datetime.today().timestamp()))
            try:
                instrument = F"ticker_{str(instrument_id)}"
                price = str(price)
                cls.redis_client.execute_command('publish ' + instrument + '_last ' + timestamp + '|' + price)
                cls.redis_client.execute_command('hset ' + instrument + ' last ' + price)
            except Exception as e:
                logger.logger.error(f"set_ticker_last_price has failed: {e}" )
                raise e

    @classmethod
    @automation_logger(logger)
    def get_ticker_last_price(cls, instrument_id):
        """
        Returns the ticker on the selected instrument the Redis.
        :param instrument_id:
        :return: "last" parameter from ticker
        """
        try:
            instrument = F"ticker_{str(instrument_id)}"
            result = float(cls.redis_client.execute_command('hget ' + instrument + ' last'))
            if result is not None:
                return result
        except Exception as e:
            logger.logger.error(f"get_ticker_last_price has failed: {e}")
            raise e

    @classmethod
    @automation_logger(logger)
    def get_ticker_volume_24(cls, instrument_id):
        """
        Returns the ticker volume on the selected instrument the Redis.
        :param instrument_id:
        :return: "volume" parameter from ticker as float
        """
        try:
            return float(cls.redis_client.execute_command('hget ticker_' + str(instrument_id) + ' volume24'))
        except Exception as e:
            logger.logger.error(F"get_ticker_volume_24 method has failed: {e}")
            raise e

    @classmethod
    @automation_logger(logger)
    def get_ticker_change_24(cls, instrument_id):
        """
        Returns the ticker change 24H on the selected instrument the Redis.
        :param instrument_id:
        :return: "change" parameter from ticker as float
        """
        try:
            return float(cls.redis_client.execute_command('hget ticker_' + str(instrument_id) + ' change'))
        except Exception as e:
            logger.logger.error(F"get_ticker_change_24 method has failed: {e}")
            raise e

    @classmethod
    @automation_logger(logger)
    def get_ticker_high_24(cls, instrument_id):
        """
        Returns the ticker high 24 on the selected instrument the Redis.
        :param instrument_id:
        :return: "24 high" parameter from ticker as float
        """
        try:
            return float(cls.redis_client.execute_command('hget ticker_' + str(instrument_id) + ' high24'))
        except Exception as e:
            logger.logger.error(F"get_ticker_high_24 method has failed: {e}")
            raise e

    @classmethod
    @automation_logger(logger)
    def get_ticker_low_24(cls, instrument_id):
        """
        Returns the ticker low 24 on the selected instrument the Redis.
        :param instrument_id:
        :return: "24 low" parameter from ticker as float
        """
        try:
            return float(cls.redis_client.execute_command('hget ticker_' + str(instrument_id) + ' low24'))
        except Exception as e:
            logger.logger.error(F"get_ticker_low_24 method has failed: {e}")
            raise e

    @classmethod
    @automation_logger(logger)
    def get_key_value(cls, key):
        """
        Connects to Redis DB to get value by provided key.
        :param key: neede redis key.
        :return: value of given key.
        """
        return cls.redis_client.get(key)

    @classmethod
    @automation_logger(logger)
    def get_hash_key_value(cls, key1, key2):
        """
        Connects to Redis DB to get value by provided key.
        :param key1: neede redis key.
        :param key2: neede redis key.
        :return: value of given key.
        """
        return cls.redis_client.hget(key1, key2)

    @classmethod
    @automation_logger(logger)
    def validate_auth_token(cls, token):
        """

        :param token:
        :return:
        """
        return cls.redis_client.ttl(token)

    @classmethod
    @automation_logger(logger)
    def get_me_state(cls):
        """
        :return: value as int  if 1 -  trading time   or  2 -  maintenance time
        """
        return int(cls.get_key_value('me_state'))
