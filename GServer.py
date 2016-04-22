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
server_socket.bind(("", port))  # fix the port later
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
greed = Greed(x_length, y_length, 0)
pac_board = Greed(x_length, y_length, 3)
player_list = []
num_of_dots = pac_board.get_num_of_dots() - num_of_players
#place all the players in a randomly generated places
pac_id = random.randint(0, (num_of_players - 1))
for i in xrange(num_of_players):
    x_pos = random.randint(0, x_length - 1)
    y_pos = random.randint(0, y_length - 1)
    while greed.get_place_info(x_pos, y_pos) != 0:
        x_pos = random.randint(0, x_length - 1)
        y_pos = random.randint(0, y_length - 1)
    temp_player = Player(x_pos, y_pos)
    player_list.append((x_pos, y_pos))
    if i == pac_id:
        greed.place_player(temp_player, 2)
        pac_board.place_player(temp_player, 2)
    else:
        greed.place_player(temp_player, 1)
        pac_board.place_player(temp_player, 0)

#everyone spawn points already pickled
pickled_player_list = cPickle.dumps(player_list)
#waiting for all players to connect
while num_of_players != len(client_sockets):
    (new_socket, address) = server_socket.accept()
    player_id = len(client_sockets)
    to_send = str(player_id) + "+" + pickled_player_list
    #background color, pac-man sees yellow, while the ghost see blank (0)
    if player_id == pac_id:
        to_send = to_send + "+" + str(3)
    else:
        to_send = to_send + "+" + str(0)
    client_sockets.append(new_socket)
    new_socket.send(to_send)

#testing the pac board DELETE when can
pygame.init()
screen_height = 25.25 * x_length
screen_width = 25.25 * y_length
size = (int(screen_width), int(screen_height))
screen = pygame.display.set_mode(size)
pygame.display.set_caption("test")
clock = pygame.time.Clock()
pac_board.add_screen(screen)
something = pac_board.draw_grid()
pygame.display.flip()
#end

done = 0
"""
done:
0 - game continue
1 - ghosts won
2 - pac-man won
"""


#start the game loop (getting and sending updated players locations)
while done == 0:
    read_from, write_to, error_list = select.select(client_sockets, client_sockets, client_sockets)
    pac_pos = player_list[pac_id]
    if len(read_from) != 0:
        for client in read_from:
            data = client.recv(1024)
            if data != "":
                status, id_id = data.split(",")
                id_id = int(id_id)
                temp_player = Player(player_list[id_id][0], player_list[id_id][1])
                status = cPickle.loads(status)
                #if current player is pac man or not
                if id_id == pac_id:
                    next_x, next_y = pac_board.calc_next_pos((pac_pos[0], pac_pos[1]), status)
                    state = pac_board.get_place_info(next_x, next_y)
                    pac_board.move_player(temp_player, status, 2, 0)
                    greed.move_player(temp_player, status, 2, 0)
                    #problems with it, no real reason
                    if state == 3:
                        num_of_dots -= 1
                    if num_of_dots == 0:
                        done = 2
                    print num_of_dots

                else:
                    greed.move_player(temp_player, status, 1, 0)
                    if temp_player.get_pose() == pac_pos:
                        done = 1
                new_pos = temp_player.get_pose()
                player_list[id_id] = new_pos
                pac_pos = player_list[pac_id]
                replace = pac_board.get_place_info(new_pos[0], new_pos[1])
                to_send = (cPickle.dumps(status), str(id_id), str(done), replace)
                send_message_to_all(cPickle.dumps(to_send), write_to)

                #pygame stuffs
                something = pac_board.draw_grid()
                pygame.display.flip()
                #end of #pygame

print "game over"