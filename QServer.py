__author__ = 'guypc'

import socket
import select

#opening server socket and listening to clients
server_socket = socket.socket()
server_socket.bind(("0.0.0.0", 6845))
server_socket.listen(5)
open_client_socket = []

while True:
    rlist, wlist, xlist = select.select([server_socket] + open_client_socket, [], [])
    for current_socket in rlist:
        if current_socket is server_socket:
            new_socket, address = server_socket.accept()
            open_client_socket.append(new_socket)