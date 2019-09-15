from socket import *
from src.base import logger
from src.base.log_decorator import automation_logger

HOST = '127.0.0.1'
PORT = 21112
BUFSIZ = 1024
ADDR = (HOST, PORT)


class UdpClient:

    UDPClientSocket = socket(family=AF_INET, type=SOCK_DGRAM)
    msgFromClient = "Hello UDP Server"
    bytesToSend = str.encode(msgFromClient)

    @classmethod
    @automation_logger(logger)
    def udp_connect(cls):
        logger.logger.info("UDP client up and listening")

        while True:
            cls.UDPClientSocket.sendto(cls.bytesToSend, ADDR)

            bytes_address_pair = cls.UDPClientSocket.recvfrom(BUFSIZ)

            message = bytes_address_pair[0]

            address = bytes_address_pair[1]

            server_msg = "Message from Server:{}".format(message)
            server_ip = "Server IP Address:{}".format(address)

            logger.logger.info(server_msg)
            logger.logger.info(server_ip)

            # cls.UDPClientSocket.close()
