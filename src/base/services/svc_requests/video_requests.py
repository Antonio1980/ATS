from src.base import logger
from src.base.log_decorator import automation_logger
from src.base.services.svc_requests.request_constants import *
from src.base.services.svc_requests.request_schema import ApiRequestSchema


class VideoServiceRequest(ApiRequestSchema):
    def __init__(self):
        super(VideoServiceRequest, self).__init__()
        self.method = "Video."

    @automation_logger(logger)
    def videos(self):
        """

        @return:
        """
        self.method += "Videos"
        self.params.extend([
            {
                PAGINATION: {
                    LIMIT: 20,
                    OFFSET: 10
                }
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def get_playlist_videos(self, id_1: int, id_2: int, id_3: int):
        """

        @param id_1:
        @param id_2:
        @param id_3:
        @return:
        """
        self.method += "GetPlaylistVideos"
        self.params.extend([
            {
                IDS:
                    [
                        id_1,
                        id_2,
                        id_3
                    ]
            }
        ])
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body
