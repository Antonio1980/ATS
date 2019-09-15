from _socket import *

from src.base import logger
from src.base.log_decorator import automation_logger

HOST = '127.0.0.1'
PORT = 21112
BUFSIZ = 1024
ADDR = (HOST, PORT)


class UdpServer:

    UDPServerSocket = socket(family=AF_INET, type=SOCK_DGRAM)
    msgFromServer = "Hello UDP Client"
    bytesToSend = str.encode(msgFromServer)

    @classmethod
    @automation_logger(logger)
    def udp_listen(cls):

        cls.UDPServerSocket.bind(ADDR)

        logger.logger.info("UDP server up and listening")
        while True:

            bytes_address_pair = cls.UDPServerSocket.recvfrom(BUFSIZ)

            message = bytes_address_pair[0]

            address = bytes_address_pair[1]

            client_msg = "Message from Client:{}".format(message)
            client_ip = "Client IP Address:{}".format(address)

            logger.logger.info(client_msg)
            logger.logger.info(client_ip)
            # Sending a reply to client

            cls.UDPServerSocket.sendto(cls.bytesToSend, address)
            # cls.UDPServerSocket.close()
