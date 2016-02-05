__author__ = 'guypc'

import socket
import select
import os
import sys

def send_waiting_message(wlist):
    for message in messages_to_send:
        (client_socket, data) = message
        for current_client in wlist:
            if client_socket is not current_client:
                current_client.send(data)
        messages_to_send.remove(message)


#move all the players in queue to the game server
def move_to_game_server(player_list):
    player_file = open("players.txt", 'w')
    for client in player_list:
        ip, port = client
        player_file.write(client[0] + ":" + str(client[1]))
    pass


#open the game server file (GServer.py)
def open_game_server():
    os.system("GServer.py")
    pass

#opening server socket and listening to clients
server_socket = socket.socket()
server_socket.bind(("0.0.0.0", 6845))
server_socket.listen(5)
open_client_socket = []
messages_to_send = []
players = 1  # number of players in the game

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

    #start the game
    if len(client_info) == players:
        print "all done"
        open_game_server()
        move_to_game_server(client_info)
        client_info = []
        open_client_socket = []