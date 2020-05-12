import json
import requests
from src.base import logger
from src.base import file_svc_url
from src.base.log_decorator import automation_logger


class FileService:
    file_svc_headers = {}
    file_svc_url = file_svc_url
    file_svc_headers.update({'connection': 'close'})

    @automation_logger(logger)
    def upload_file(self, file_: str) -> json:
        """
        Sends HTTP POST request to FileService to upload file (needed for registration).
        :param file_: Path to the file to upload.
        :return: Response body as a json.
        """
        try:
            with open(file_, 'rb') as f:
                return json.loads(
                    requests.post(
                        self.file_svc_url, files={'file': f}, headers=self.file_svc_headers, timeout=10).text)
        except Exception as e:
            logger.logger.exception(F"{e.__class__.__name__} upload_file failed with error: {e}")
            raise e
