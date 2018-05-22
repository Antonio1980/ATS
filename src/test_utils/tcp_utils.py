# !/usr/bin/env python
# -*- coding: utf8 -*-


import socket


socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_client.connect(("192.168.14.165", 4444))
data = socket_client.recv(2048)
print(data)
socket_client.send(bytes("This from Client.", 'UTF-8'))
socket_client.close()

socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_server.bind(("192.168.14.165", 4444))
socket_server.listen(5)
(client,(ip,port)) = socket_server.accept()
client.send(bytes("Knock knock, I'm server.", 'UTF-8'))
data = client.recv(2048)
print(data)
socket_server.close()


class TcpClient():
    query = "This from Client."

    def __init__(self):
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def tcp_connect(self, ip, port):
        self.socket_client.connect((ip, port))
        # needed
        data = self.socket_client.recv(2048)
        return data

    def send_message(self, query, *code):
        self.socket_client.send(bytes(query, 'UTF-8'))

    def close_connection(self):
        self.socket_client.close()




class TcpServer:
    query = "Knock knock, I'm server."

    def __init__(self, ip, port):
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_server.bind((ip, port))
        self.socket_server.listen(5)

    def receive_message(self, query, *code):
        (client, (ip, port)) = self.socket_server.accept()
        client.send(bytes(query, 'UTF-8'))
        data = client.recv(2048)
        return data

    def close_connection(self):
        self.socket_server.close()


    