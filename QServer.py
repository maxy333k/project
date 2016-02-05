__author__ = 'guypc'

import socket
import select


def send_waiting_message(wlist):
    for message in messages_to_send:
        (client_socket, data) = message
        for current_client in wlist:
            if client_socket is not current_client:
                current_client.send(data)
        messages_to_send.remove(message)


#move all the players in queue to the game server
def move_to_game_server(player_list):
    pass

#opening server socket and listening to clients
server_socket = socket.socket()
server_socket.bind(("0.0.0.0", 6845))
server_socket.listen(5)
open_client_socket = []
messages_to_send = []
players = 5  # number of players in the game

while True:
    rlist, wlist, xlist = select.select([server_socket] + open_client_socket, open_client_socket, [])
    for current_socket in rlist:
        if current_socket is server_socket:
            (new_socket, address) = server_socket.accept()
            open_client_socket.append(new_socket)
        else:
            data=current_socket.recv(1024)
            if data == "":
                open_client_socket.remove(current_socket)

    #start the game
    if len(open_client_socket) == players:
        move_to_game_server(open_client_socket)
        open_client_socket = []