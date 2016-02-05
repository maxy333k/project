__author__ = 'guypc'

import socket
import select
import os
import sys
import random


def send_game_port_to_players(port, wlist):
    for current_client in wlist:
        current_client.send(str(port))


#move all the players in queue to the game server
def move_to_game_server(player_list):
    player_file = open("players.txt", 'w')
    for client in player_list:
        player_file.write(client[0] + ":" + str(client[1]))


#define port for the game server
def set_port():
    return random.randint(6850, 7000)

#open the game server file (GServer.py)
def open_game_server():
    os.system("GServer.py")
    pass


print "i am queue server"
#opening server socket and listening to clients
server_socket = socket.socket()
server_socket.bind(("0.0.0.0", 6845))
server_socket.listen(5)
open_client_socket = []
messages_to_send = []
players = 2  # number of players in the game

while True:
    rlist, wlist, xlist = select.select([server_socket] + open_client_socket, open_client_socket, [])
    client_info = []
    for current_socket in rlist:
        if current_socket is server_socket:
            new_socket, new_address = server_socket.accept()
            client_info.append(new_address)
        else:
            data = current_socket.recv(1024)
            if data == "":
                open_client_socket.remove(current_socket)
                print "rip"
            print data

    #start the game at game server
    if len(client_info) == players:
        move_to_game_server(client_info)
        port = 53
       # send_game_port_to_players(port, wlist)
        open_game_server()
        client_info = []
        open_client_socket = []