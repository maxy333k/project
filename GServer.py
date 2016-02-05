__author__ = 'guypc'

import socket
import select


#recive all ips and ports form txt file
def get_clients_address():
    ip_file = open("players.txt", 'r')
    client_list = []
    for line in ip_file:
        client_list.append(line.split(":"))
    return client_list

#creting sockets
GServer_socket = socket.socket()
client_address = get_clients_address()

#connecting with each client by the ip
for client_socket in client_address:
    pass

while True:
    pass

print "done"