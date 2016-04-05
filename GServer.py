__author__ = 'guypc'

import socket
import select
import random
import cPickle
from GameClass import *


def send_message_to_all(message, socket_list):
    for client in socket_list:
        client.send(message)


#creating the socket
server_socket = socket.socket()
client_sockets = []
port_file = open("port.txt", "r")
port = int(port_file.readline())
server_socket.bind(("0.0.0.0", port))  # fix the port later
port_file.close()
port_file = open("port.txt", "w")
port += 1
port_file.write(str(port))
port_file.close()
server_socket.listen(5)
num_of_players = 2
print "hello"


#define the map and all players starting positions
x_length = 8
y_length = 8
greed = Greed(x_length, y_length, 3)
player_list = []

#place all the players in a randomly generated places
for i in xrange(num_of_players):
    x_pos = random.randint(0, x_length - 1)
    y_pos = random.randint(0, y_length - 1)
    while greed.get_place_info(x_pos, y_pos) != 3:
        x_pos = random.randint(0, x_length - 1)
        y_pos = random.randint(0, y_length - 1)
    temp_player = Player(x_pos, y_pos)
    player_list.append((x_pos, y_pos))
    greed.place_player(temp_player, 1)

#waiting for all players to connect
pac_id = random.randint(0, (num_of_players - 1))
while num_of_players != len(client_sockets):
    (new_socket, address) = server_socket.accept()
    client_sockets.append(new_socket)
    to_send = str(len(client_sockets) - 1) + "," + cPickle.dumps(player_list)  # the player ID and all players pos
    if len(client_sockets) == pac_id:
        to_send = to_send + "," + str(1)
    else:
        to_send = to_send + "," + str(0)
    new_socket.send(to_send)

#start the game loop (getting and sending updated players locations
while True:
    read_from, write_to, error_list = select.select(client_sockets, client_sockets, client_sockets)
    if len(read_from) != 0:
        for client in read_from:
            data = client.recv(1024)
            if data != "":
                status, id_id = data.split(",")
                temp_player = Player(player_list[int(id_id)][0], player_list[int(id_id)][1])
                status = cPickle.loads(status)
                greed.move_player(temp_player, status, 1)
                to_send = cPickle.dumps(status) + "+" + str(id_id)
                send_message_to_all(to_send, write_to)