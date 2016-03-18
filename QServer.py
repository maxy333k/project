__author__ = 'guypc'


import socket
import select
import os

#send the game server port for all the clients
def send_waiting_message(client_list, port):
    for current_client in client_list:
        current_client.send(str(port))

#close the connection for all the clients
def close_connection(socket_list):
    for that_socket in socket_list:
        that_socket.close()

#creating the socket and socket list
server_socket = socket.socket()
server_socket.bind(("0.0.0.0", 2300))
server_socket.listen(5)
open_client_socket = []
messages_to_send = []
num_of_players = 1
online_players = 0
g_port = 2301

while True:
    #waiting for 5 players to connect to the server
    rlist, wlist, xlist = select.select([server_socket] + open_client_socket, open_client_socket, [])
    for current_socket in rlist:
        if current_socket is server_socket:
            (new_socket, address) = server_socket.accept()
            open_client_socket.append(new_socket)
            online_players += 1
            print "hello"

    #start the new server and restarting the client list
    if online_players == num_of_players:
        os.system("start GServer.py")
        print "opened"
        send_waiting_message(open_client_socket, g_port)
        close_connection(open_client_socket)
        open_client_socket = []
        online_players = 0

