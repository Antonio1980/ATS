from src.base import logger
from src.base.services.crm import Crm
from src.base.services.kafka_ import KafkaService
from src.base.log_decorator import automation_logger
from src.base.services.api_service import ApiService
from src.base.automation_error import AutomationError
from src.base.services.feed_service import FeedService
from src.base.services.file_service import FileService
from src.base.services.order_service import OrderService
from src.base.services.trade_service import TradeService
from src.base.services.asset_service import AssetService
from src.base.services.video_service import VideoService
from src.base.services.balance_service import BalanceService
from src.base.services.payment_service import PaymentService
from src.base.services.tracking_service import TrackingService
from src.base.services.customer_service import CustomerService
from src.base.services.i_balance_service import IBalanceService
from src.base.services.coins_marketplace import CoinsMarketplace
from src.base.services.obligation_service import ObligationService
from src.base.services.notification_service import NotificationService
from src.base.services.authorization_service import AuthorizationService


class PostmanClient(object):
    def __init__(self, auth_token=None):
        super(PostmanClient, self).__init__()
        self.crm = Crm()
        self.kafka = KafkaService()
        self.file_service = FileService()
        self.balance_service = IBalanceService()
        self.coins_marketplace = CoinsMarketplace()
        self.api_service = ApiService(auth_token)
        self.feed_service = FeedService(auth_token)
        self.order_service = OrderService(auth_token)
        self.video_service = VideoService(auth_token)
        self.asset_service = AssetService(auth_token)
        self.trade_service = TradeService(auth_token)
        self.payment_service = PaymentService(auth_token)
        self.tracking_service = TrackingService(auth_token)
        self.customer_service = CustomerService(auth_token)
        self.obligation_service = ObligationService(auth_token)
        self.p_balance_service = BalanceService(auth_token)
        self.notification_service = NotificationService(auth_token)
        self.authorization_service = AuthorizationService(auth_token)

    @staticmethod
    def get_static_postman(auth_token=None):
        """
        Provides ability to use PostmanClient separately from Customer class
        :param auth_token: Authorization token (if provided only for authorized self.output_file).
        :return: PostmanClient class instance.
        """
        return PostmanClient(auth_token)

    @automation_logger(logger)
    def get_instrument_data(self, instrument_id):
        """
        The method can be used to get the following instrument data from AssetManagement service API:
        (instrument_name, base_currency, quoted_currency, tail_digits, min_order_quantity, max_order_quantity,
        initial_rate, reference_price)
        :param instrument_id: ID of an Instrument- int
        :return: A tuple with data on given instrument.
        """
        response = self.asset_service.get_instruments()
        assert response['error'] is None

        all_instruments = response['result']['instruments']

        for instrument in all_instruments:

            if instrument['id'] == instrument_id:
                return (instrument['name'], instrument['asset']['baseCurrencyId'],
                        instrument['asset']['quotedCurrencyId'], instrument['asset']['tailDigits'],
                        instrument['minOrderQuantity'], instrument['maxOrderQuantity'], instrument['initialRate'],
                        instrument['referencePriceParameter'])

        error_message = f"No instrument with such ID: {instrument_id} "
        logger.logger.error(error_message)
        raise AutomationError(error_message)
