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

        while(True):
            cls.UDPClientSocket.sendto(cls.bytesToSend, ADDR)

            bytesAddressPair = cls.UDPClientSocket.recvfrom(BUFSIZ)

            message = bytesAddressPair[0]

            address = bytesAddressPair[1]

            serverMsg = "Message from Server:{}".format(message)
            serverIP  = "Server IP Address:{}".format(address)

            logger.logger.info(serverMsg)
            logger.logger.info(serverIP)

            # cls.UDPClientSocket.close()


if __name__ == "__main__":
    UdpClient.udp_connect()
    pass
