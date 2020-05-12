from src.base import logger
from src.base.log_decorator import automation_logger
from src.base.services.svc_requests.request_constants import *
from src.base.services.svc_requests.request_schema import ApiRequestSchema


class OrderServiceRequest(ApiRequestSchema):
    def __init__(self):
        super(OrderServiceRequest, self).__init__()
        self.method = "OrderManagement."

    @automation_logger(logger)
    def create_order(self, order):
        """
        Build request body for PostmanClient.create_order().
        :param order: Order object.
        :return: Request body.
        """
        self.method += "Create"
        if order.p_value and order.p_precision:
            order.type = 2
            self.params.extend([
                {
                    ORDER:
                        {
                            DIRECTION: order.direction,
                            QUANTITY:
                                {
                                    VALUE: order.q_value,
                                    DECIMALS: order.q_precision
                                },
                            ORDER_TYPE: order.type,
                            PRICE:
                                {
                                    VALUE: order.p_value,
                                    DECIMALS: order.p_precision
                                },
                            INSTRUMENT_ID: order.instrument_id
                        }
                }
            ])
        else:
            order.type = 1
            self.params.extend([
                {
                    ORDER:
                        {
                            DIRECTION: order.direction,
                            QUANTITY:
                                {
                                    VALUE: order.q_value,
                                    DECIMALS: order.q_precision
                                },
                            ORDER_TYPE: order.type,
                            INSTRUMENT_ID: order.instrument_id
                        }
                }
            ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def create_order_sync(self, order):
        """
        Build request body for PostmanClient.create_order_sync().
        :param order: Order object.
        :return: Request body.
        """
        self.method += "SyncCreate"
        if order.p_value and order.p_precision:
            self.params.extend([
                {
                    ORDER:
                        {
                            DIRECTION: order.direction,
                            QUANTITY:
                                {
                                    VALUE: order.q_value,
                                    DECIMALS: order.q_precision
                                },
                            ORDER_TYPE: 2,
                            PRICE:
                                {
                                    VALUE: order.p_value,
                                    DECIMALS: order.p_precision
                                },
                            INSTRUMENT_ID: order.instrument_id
                        }
                }
            ])
        else:
            self.params.extend([
                {
                    ORDER:
                        {
                            DIRECTION: order.direction,
                            QUANTITY:
                                {
                                    VALUE: order.q_value,
                                    DECIMALS: order.q_precision
                                },
                            ORDER_TYPE: 1,
                            INSTRUMENT_ID: order.instrument_id
                        }
                }
            ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def cancel_order(self, order_id):
        """
        Build request body for PostmanClient.cancel_order()
        :param order_id: If String it will be sent as External ID , in case of Integer will be used internal ID.
        :return: Request body.
        """
        self.method += "Cancel"
        if isinstance(order_id, str) and "A" in order_id:
            self.params.extend([
                {
                    EXTERNAL_ORDER_ID: order_id
                }
            ])
        else:
            self.params.extend([
                {
                    ID: str(order_id),
                }
            ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def order_history(self, direction=None, product_id=None, instrument_id=None, *args):
        """
        Build request body for PostmanClient.get_order_history().
        :param direction: Sell or Buy as a string.
        :param product_id: Product ID- int.
        :param instrument_id: 
        :return: Request body.
        """
        self.method += "OrderHistory"
        if args and len(args[0]) > 0:
            ((limit, offset, ), ) = args
        else:
            limit, offset = 20, 0
        if direction and instrument_id and product_id:
            self.params.extend([
                {
                    PRODUCT_ID: product_id,
                    ORDER_CREATED_FROM: self.timestamp_from,
                    ORDER_CREATED_TO: self.timestamp_to,
                    INSTRUMENT_ID: instrument_id,
                    DIRECTION: direction
                }
            ])
        elif direction and product_id is None and instrument_id is None:
            self.params.extend([
                {
                    ORDER_CREATED_FROM: self.timestamp_from,
                    ORDER_CREATED_TO: self.timestamp_to,
                    DIRECTION: direction
                }
            ])
        elif direction is None and instrument_id and product_id is None:
            self.params.extend([
                {
                    ORDER_CREATED_FROM: self.timestamp_from,
                    ORDER_CREATED_TO: self.timestamp_to,
                    INSTRUMENT_ID: instrument_id
                }
            ])
        elif direction is None and instrument_id is None and product_id is not None:
            self.params.extend([
                {
                    PRODUCT_ID: product_id,
                    ORDER_CREATED_FROM: self.timestamp_from,
                    ORDER_CREATED_TO: self.timestamp_to
                }
            ])
        elif direction and instrument_id and product_id is None:
            self.params.extend([
                {
                    INSTRUMENT_ID: instrument_id,
                    ORDER_CREATED_FROM: self.timestamp_from,
                    ORDER_CREATED_TO: self.timestamp_to,
                    DIRECTION: direction
                }
            ])
        elif direction and instrument_id is None and product_id:
            self.params.extend([
                {
                    PRODUCT_ID: product_id,
                    ORDER_CREATED_FROM: self.timestamp_from,
                    ORDER_CREATED_TO: self.timestamp_to,
                    DIRECTION: direction
                }
            ])
        elif direction is None and instrument_id and product_id:
            self.params.extend([
                {
                    PRODUCT_ID: product_id,
                    ORDER_CREATED_FROM: self.timestamp_from,
                    ORDER_CREATED_TO: self.timestamp_to,
                    INSTRUMENT_ID: instrument_id
                }
            ])
        else:
            self.params.append({})
        pagination = {PAGINATION: {LIMIT: limit, OFFSET: offset}}
        self.params[0].update(pagination)
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def export_order_history(self, direction, product_id=None, instrument_id=None):
        """
        Build request body for PostmanClient.get_order_history().
        :param direction: Sell or Buy as a string.
        :param product_id: Product ID- int.
        :param instrument_id:
        :return: Request body.
        """
        self.method += "ExportOrderHistory"
        if product_id and instrument_id:
            self.params.extend([
                {
                    PRODUCT_ID: product_id,
                    ORDER_CREATED_FROM: self.timestamp_from,
                    ORDER_CREATED_TO: self.timestamp_to,
                    INSTRUMENT_ID: instrument_id,
                    DIRECTION: direction
                }
            ])
        elif product_id and instrument_id is None:
            self.params.extend([
                {
                    PRODUCT_ID: product_id,
                    ORDER_CREATED_FROM: self.timestamp_from,
                    ORDER_CREATED_TO: self.timestamp_to,
                    INSTRUMENT_ID: instrument_id
                }
            ])
        elif instrument_id and product_id is None:
            self.params.extend([
                {
                    ORDER_CREATED_FROM: self.timestamp_from,
                    ORDER_CREATED_TO: self.timestamp_to,
                    INSTRUMENT_ID: instrument_id,
                    DIRECTION: direction
                }
            ])
        else:
            self.params.extend([
                {
                    ORDER_CREATED_FROM: self.timestamp_from,
                    ORDER_CREATED_TO: self.timestamp_to,
                    DIRECTION: direction
                }
            ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def trades_history(self, direction=None, product_id=None, instrument_id=None, *args):
        """
        Build request body for PostmanClient.get_trades_history()
        :param direction: Sell or Buy as a string.
        :param product_id: Product ID- int.
        :param instrument_id:
        :return: Request body.
        """
        self.method += "TradeHistory"
        if args and len(args[0]) > 0:
            ((limit, offset,),) = args
        else:
            limit, offset = 20, 0
        if direction and product_id and instrument_id:
            self.params.extend([
                {
                    PRODUCT_ID: product_id,
                    TRADE_CREATED_FROM: self.timestamp_from,
                    TRADE_CREATED_TO: self.timestamp_to,
                    DIRECTION: direction,
                    INSTRUMENT_ID: instrument_id
                }
            ])
        elif direction and product_id and instrument_id is None:
            self.params.extend([
                {
                    PRODUCT_ID: product_id,
                    TRADE_CREATED_FROM: self.timestamp_from,
                    TRADE_CREATED_TO: self.timestamp_to,
                    DIRECTION: direction
                }
            ])
        elif direction and product_id is None and instrument_id is not None:
            self.params.extend([
                {
                    TRADE_CREATED_FROM: self.timestamp_from,
                    TRADE_CREATED_TO: self.timestamp_to,
                    DIRECTION: direction,
                    INSTRUMENT_ID: instrument_id
                }
            ])
        elif direction is None and product_id and instrument_id:
            self.params.extend([
                {
                    PRODUCT_ID: product_id,
                    TRADE_CREATED_FROM: self.timestamp_from,
                    TRADE_CREATED_TO: self.timestamp_to,
                    INSTRUMENT_ID: instrument_id
                }
            ])
        elif direction and product_id is None and instrument_id is None:
            self.params.extend([
                {
                    TRADE_CREATED_FROM: self.timestamp_from,
                    TRADE_CREATED_TO: self.timestamp_to,
                    DIRECTION: direction,
                }
            ])
        elif direction is None and product_id is None and instrument_id:
            self.params.extend([
                {
                    TRADE_CREATED_FROM: self.timestamp_from,
                    TRADE_CREATED_TO: self.timestamp_to,
                    INSTRUMENT_ID: instrument_id
                }
            ])
        elif direction is None and product_id and instrument_id is None:
            self.params.extend([
                {
                    PRODUCT_ID: product_id,
                    TRADE_CREATED_FROM: self.timestamp_from,
                    TRADE_CREATED_TO: self.timestamp_to,
                }
            ])
        else:
            self.params.append({})
        pagination = {PAGINATION: {LIMIT: limit, OFFSET: offset}}
        self.params[0].update(pagination)
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def export_trade_history(self, direction, product_id=None, instrument_id=None):
        """
        Build request body for PostmanClient.get_order_history().
        :param direction: Sell or Buy as a string.
        :param product_id: Product ID- int.
        :param instrument_id: Instrument ID- int.
        :return: Request body.
        """
        self.method += "ExportTradeHistory"
        if product_id and instrument_id:
            self.params.extend([
                {
                    PRODUCT_ID: product_id,
                    TRADE_CREATED_FROM: self.timestamp_from,
                    TRADE_CREATED_TO: self.timestamp_to,
                    DIRECTION: direction,
                    INSTRUMENT_ID: instrument_id
                }
            ])
        elif product_id and instrument_id is None:
            self.params.extend([
                {
                    PRODUCT_ID: product_id,
                    TRADE_CREATED_FROM: self.timestamp_from,
                    TRADE_CREATED_TO: self.timestamp_to,
                    INSTRUMENT_ID: instrument_id
                }
            ])
        elif instrument_id and product_id is None:
            self.params.extend([
                {
                    TRADE_CREATED_FROM: self.timestamp_from,
                    TRADE_CREATED_TO: self.timestamp_to,
                    DIRECTION: direction,
                    INSTRUMENT_ID: instrument_id
                }
            ])
        else:
            self.params.extend([
                {
                    TRADE_CREATED_FROM: self.timestamp_from,
                    TRADE_CREATED_TO: self.timestamp_to,
                    DIRECTION: direction
                }
            ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def open_orders(self, product_id=None, *args):
        """
        Build request body for PostmanClient.get_open_orders()
        :return: Request body.
        """
        self.method += "OpenOrders"
        if args and len(args[0]) > 0:
            ((limit, offset,),) = args
        else:
            limit, offset = 20, 0
        if product_id:
            self.params.extend([
                {
                    FOR_CUSTOMER: True,
                    PRODUCT_ID: product_id,
                    SINCE_UNIX_DATE: self.timestamp_from
                }
            ])
        else:
            self.params.extend([
                {
                    FOR_CUSTOMER: True,
                    SINCE_UNIX_DATE: self.timestamp_from
                }
            ])
        pagination = {PAGINATION: {LIMIT: limit, OFFSET: offset}}
        self.params[0].update(pagination)
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def export_open_orders(self, product_id=None):
        """
        Build request body for PostmanClient.get_open_orders()
        :return: Request body.
        """
        self.method += "ExportOpenOrders"
        if product_id:
            self.params.extend([
                {
                    PRODUCT_ID: product_id
                }
            ])
        else:
            self.params.extend([{}])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def get_order_book(self, instrument_id=None):
        """
        Build request body for PostmanClient.get_order_book()
        :return: Request body.
        """
        self.method += "GetOrderBook"
        self.params.extend([
            {
                INSTRUMENT_ID: instrument_id
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

# if __name__ == '__main__':
#     from src.base.equipment.order import Order
#
#     o = Order().set_order(1, 1012, 0.25, 3800.0)
#     r = OrderServiceRequest().create_order(o).to_json()
#     r2 = OrderServiceRequest().order_history()
#     pass
