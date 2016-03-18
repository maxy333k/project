__author__ = 'guypc'

import socket
import select
import random

#creating the socket
server_socket = socket.socket()
client_sockets = []
server_socket.listen(5)
num_of_players = 5

#waiting for all players to connect
while num_of_players != len(client_sockets):
    (new_socket, address) = server_socket.accept()
    client_sockets.append(new_socket)

#define the map size and all players starting positions
x_length = 8
y_length = 8
pos_list = []
