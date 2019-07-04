from src.base import logger
from src.base.log_decorator import automation_logger
from src.base.services.svc_requests.request_constants import *
from src.base.services.svc_requests.request_schema import ApiRequestSchema


class AssetServiceRequest(ApiRequestSchema):
    def __init__(self):
        super(AssetServiceRequest, self).__init__()
        self.method = "AssetManagement."

    @automation_logger(logger)
    def history(self, instrument_id=None, type_="1d"):
        """
        Builds request body for AssetService.get_history().
        :param instrument_id: ID of an instrument- int, not mandatory (without- for all instruments).
        :param type_: String ("1m", "5m", "1h", "1d") - Tenor (good till date option).
        :return: Request body as json.
        """
        self.method += "History"
        if instrument_id:
            self.params.extend([
                {
                    TIMESTAMP_FROM: self.timestamp_from,
                    TIMESTAMP_TILL: self.timestamp_to,
                    INSTRUMENT_ID: instrument_id,
                    TYPE: type_,
                    PAGINATION:
                        {
                            LIMIT: 20,
                            OFFSET: 10
                        }
                }
            ])
        else:
            self.params.extend([
                {
                    PAGINATION:
                        {
                            LIMIT: 20,
                            OFFSET: 10
                        }
                }
            ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def set_favorite_instrument(self, instrument_id: int):
        """
        Builds request body for AssetService.set_favorite_instrument().
        :param instrument_id: ID of an instrument- int.
        :return: Request body as json.
        """
        self.method += "SetFavouriteInstrument"
        self.params.extend([
            {
                INSTRUMENT_ID: instrument_id
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def remove_favorite_instrument(self, instrument_id: int):
        """
        Builds request body for AssetService.remove_favorite_instrument().
        :param instrument_id: ID of an instrument- int
        :return: Request body as json.
        """
        self.method += "RemoveFavouriteInstrument"
        self.params.extend([
            {
                ASSET_ID: instrument_id
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def get_instruments(self, symbol=None, product_id=None):
        """
        Builds request body for AssetService.get_instruments().
        :param symbol: String as "BTC/EUR, not mandatory.
        :param product_id: Integer as 2, not mandatory.
        :return: Request body as json.
        """
        self.method += "GetInstruments"
        if symbol and product_id:
            self.params.extend([
                {
                    SYMBOL: symbol,
                    PRODUCT_ID: product_id
                }
            ])
        elif symbol and product_id is None:
            self.params.extend([
                {
                    SYMBOL: symbol
                }
            ])
        elif product_id and symbol is None:
            self.params.extend([
                {
                    PRODUCT_ID: product_id
                }
            ])
        else:
            self.params.extend([])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def get_ticker(self, instrument_id: int, currency_id: int):
        """
        Builds request body for AssetService.get_ticker().
        :param instrument_id: ID of an instrument- int.
        :param currency_id: ID of a currency- int.
        :return: Request body as json.
        """
        self.method += "GetTicker"
        self.params.extend([
            {
                INSTRUMENT_IDS: [instrument_id],
                CURRENCY_ID: currency_id
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def get_last_trades(self, instrument_id: int):
        """
        Builds request body for AssetService.get_last_trade().
        :param instrument_id: ID of an instrument- int.
        :return: Request body as json.
        """
        self.method += "GetLastTrades"
        self.params.extend([
            {
                INSTRUMENT_ID: instrument_id
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body
