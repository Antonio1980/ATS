import json
import requests
from src.base import logger
from src.base.log_decorator import automation_logger
from src.base.services.service_route import ServiceRoute
from src.base.services.svc_requests.video_requests import VideoServiceRequest


class VideoService(ServiceRoute):
    def __init__(self, auth_token=None):
        super(VideoService, self).__init__()
        self.headers.update({'Authorization': auth_token})

    @automation_logger(logger)
    def get_videos(self) -> json:
        """
        Sends HTTP POST request to VideoServiceRequest to get customer data.
        :return: Response body as a json.
        """
        payload = VideoServiceRequest().videos()
        try:
            _response = requests.post(self.api_url, data=payload, headers=self.headers)
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception(F"{e.__class__.__name__} get_videos failed with error: {e}")
            raise e

    @automation_logger(logger)
    def get_playlist_videos(self, id_1: int, id_2: int, id_3: int) -> json:
        """
        Sends HTTP POST request to VideoServiceRequest to get list of videos.
        :param id_1: ID- int.
        :param id_2: ID- int.
        :param id_3: ID- int.
        :return: Response body as a json.
        """
        payload = VideoServiceRequest().get_playlist_videos(id_1, id_2, id_3)
        try:
            _response = requests.post(self.api_url, data=payload, headers=self.headers)
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception(F"{e.__class__.__name__} get_playlist_videos failed with error: {e}")
            raise e
