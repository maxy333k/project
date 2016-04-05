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
        print "closed"


#creating the socket and socket list
server_socket = socket.socket()
server_socket.bind(("0.0.0.0", 2300))
server_socket.listen(5)
open_client_socket = []
messages_to_send = []
num_of_players = 2
online_players = 0
port_file = open("port.txt", "w")
g_port = 2301
port_file.write(str(g_port))
port_file.close()

while True:
    #waiting for 5 players to connect to the server
    rlist, wlist, xlist = select.select([server_socket] + open_client_socket, open_client_socket, [])
    for current_socket in rlist:
        if current_socket is server_socket:
            (new_socket, address) = server_socket.accept()
            open_client_socket.append(new_socket)
            online_players += 1
        else:
            data = current_socket.recv(1024)
            if data == "":
                current_socket.close()
                open_client_socket.remove(current_socket)
                online_players -= 1

    #start the new server and restarting the client list
    if online_players == num_of_players:
        os.system("start GServer.py")
        port_file.close()
        port_file = open("port.txt", "r")
        g_port = int(port_file.readline())
        print "opened"
        send_waiting_message(open_client_socket, g_port)
        close_connection(open_client_socket)
        open_client_socket = []
        online_players = 0