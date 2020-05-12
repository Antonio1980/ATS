import paramiko
from src.base import logger
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger


"""
    Implementation of SSH connector with paramiko.SSHClient.
"""


class ParamicoConnector:

    ssh_connector = paramiko.SSHClient()
    ssh_connector.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_connector.connect(hostname=BaseConfig.ME_VM_HOST, port=int(BaseConfig.ME_VM_PORT), allow_agent=False,
                          password=BaseConfig.ME_PASSWORD, look_for_keys=False, username=BaseConfig.ME_USERNAME,
                          timeout=10.0)

    @classmethod
    @automation_logger(logger)
    def execute_ssh_command(cls, command: str):
        """
        Executes Bash command front of Matching Engine using SSH protocol.
        @param command: Bash command as a string.
        """
        try:
            cls.ssh_connector.invoke_shell()

            (stdin, stdout, stderr) = cls.ssh_connector.exec_command(command)

            if stderr:
                logger.logger.error(f"{stderr}")

            for line in stdout.readlines():
                logger.logger.info(f"{line}")

                yield line
        finally:
            cls.ssh_connector.close()
