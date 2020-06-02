# -*- coding: utf-8 -*-
# @File  : Test.py
# @Author: 周璐
# @Date  : 2019/8/5
# @Desc  :
import socket


def start_tcp_server(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (ip, port)
    print('starting listen on ip %s, port %s' % server_address)
    sock.bind(server_address)
    sock.listen(1)
    while True:
        print("waiting for connection")
        client, addr = sock.accept()
        print('having a connection:', addr)
        client.send("{you connect success}".encode())
        client.close()

if __name__ == '__main__':
    start_tcp_server('192.168.92.237', 53168)
