__author__ = 'guypc'

import socket
import select
import os
import sys
import random

import socket
import select


def send_waiting_message(wlist):
    for message in messages_to_send:
        (client_socket, data) = message
        for current_client in wlist:
            if client_socket is not current_client:
                current_client.send(data)
        messages_to_send.remove(message)


print "i'm queue server"
server_socket = socket.socket()
server_socket.bind(("0.0.0.0", 23))
server_socket.listen(5)
open_client_socket = []
messages_to_send = str(random.randint(6900, 7001))
while True:
    rlist, wlist, xlist = select.select([server_socket] + open_client_socket, open_client_socket, [])
    for current_socket in rlist:
        if current_socket is server_socket:
            (new_socket, address) = server_socket.accept()
            open_client_socket.append(new_socket)
        else:
            data = current_socket.recv(1024)
            if data == "":
                open_client_socket.remove(current_socket)
                print "connection was closed"
            else:
                messages_to_send.append((current_socket, data))
    send_waiting_message(wlist)

