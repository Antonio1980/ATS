import requests
from src.base import logger
from config_definitions import BaseConfig
from src.base.automation_error import AutomationError
from src.base.log_decorator import automation_logger

kubernetes_host = BaseConfig.K8S_HOST


class Kubernetes:
    kubernetes_url_prefix = "http://" + kubernetes_host

    @classmethod
    @automation_logger(logger)
    def get_pods_by_name(cls, pod_name):
        label_selector = f"app={pod_name}"

        url = cls.kubernetes_url_prefix + "/api/v1/namespaces/default/pods?labelSelector=" + label_selector
        response = requests.get(url=url)
        data = response.json()
        logger.logger.info(f"{data}")
        # pods matching given labelSelector
        pods = data["items"]

        if len(pods) == 0:
            error_message = "POD restarting Error: no POD with such name"
            logger.logger.error(error_message)
            raise AutomationError(error_message)
        else:
            return pods

    @classmethod
    @automation_logger(logger)
    def restart_pod(cls, pod_name):
        pods = cls.get_pods_by_name(pod_name)
        if pods:
            logger.logger.info(f"{pods}")

            for pod in pods:
                pod_link = pod["metadata"]["selfLink"]

                pod_url = cls.kubernetes_url_prefix + pod_link
                logger.logger.info("deleting pod " + pod_url + " ...")

                delete_response = requests.delete(pod_url)
                logger.logger.info("result is: " + str(delete_response))

            return True
    