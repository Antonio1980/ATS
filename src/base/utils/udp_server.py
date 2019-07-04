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

        cls.UDPServerSocket.bind((ADDR))

        logger.logger.info("UDP server up and listening")
        while(True):

            bytesAddressPair = cls.UDPServerSocket.recvfrom(BUFSIZ)

            message = bytesAddressPair[0]

            address = bytesAddressPair[1]

            clientMsg = "Message from Client:{}".format(message)
            clientIP  = "Client IP Address:{}".format(address)

            logger.logger.info(clientMsg)
            logger.logger.info(clientIP)
            # Sending a reply to client

            cls.UDPServerSocket.sendto(cls.bytesToSend, address)
            # cls.UDPServerSocket.close()


if __name__ == "__main__":
    UdpServer.udp_listen()