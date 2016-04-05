__author__ = 'guypc'

import pygame
from GameClass import *
import socket
import select
import cPickle


#declarin color variables and color list
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
color_list = [WHITE, GREEN, BLUE, YELLOW]


def connect(my_socket):  # connect to server and return the grid with all the players on it
    #establishing connection with QServer
    ip = "127.0.0.1"
    port = 2300
    my_socket.connect((ip, port))

    #reciving the new port, closing the current socket and start a new one
    print "waiting for more players to connect"
    port = my_socket.recv(1024)
    print port
    my_socket.shutdown(socket.SHUT_WR)
    my_socket = socket.socket()
    port = int(port)
    #connecting to the game server
    my_socket.connect((ip, port))
    print "connected"
    #reciving the id, positions and if the player is pac-man
    data = my_socket.recv(1024)
    number, players_pos, role = data.split("+")  # fix and add role
    number = int(number)
    role = int(role)
    print number
    players_pos = cPickle.loads(players_pos)
    players_list = []
    for temp_player in players_pos:
        temp_x, temp_y = temp_player
        players_list.append(Player(temp_x, temp_y))

    #placing the player on the board
    x_length = 8
    y_length = 8
    count = 0
    board = Greed(x_length, y_length, role)
    for temp_player in players_list:
        if count == number:
            board.place_player(temp_player, 2)
        else:
            board.place_player(temp_player, 1)
        count += 1
    return board, players_list, number, role, my_socket


#connect
grid, player_list, id_number, role, my_socket = connect(socket.socket())


#declaring general variables
row_block_num = 8
column_block_num = 8
screen_height = 25.25 * row_block_num
screen_width = 25.25 * column_block_num
size = (int(screen_width), int(screen_height))

#intilazing py-games
pygame.init()
font = pygame.font.SysFont('Calibri', 25, True, False)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("New game")
clock = pygame.time.Clock()
done = 0
"""
done:
0 - game continue
1 - ghosts won
2 - pac-man won
"""


#drawing the grid according to the server info/

grid.add_screen(screen)
num_of_dots = grid.draw_grid()
pygame.display.flip()

#declaring status dict for player movement
status_dict = {pygame.K_UP: (-1, 0),
               pygame.K_DOWN: (1, 0),
               pygame.K_LEFT: (0, -1),
               pygame.K_RIGHT: (0, 1),
               pygame.K_w: (-1, 0),
               pygame.K_s: (1, 0),
               pygame.K_a: (0, -1),
               pygame.K_d: (0, 1)}

#main game loop
while done == 0:
    read, write, error = select.select([my_socket], [my_socket], [my_socket])
    if len(write) != 0:
        write = write[0]

    #tring to read new location from the server and placing in on the board
    if len(read) != 0:
        read = read[0]
        data = ""
        try:
            data = read.recv(1024)
        finally:
            if data != "":
                new_pos, id_id, done = data.split("+")
                done = int(done)
                print done
                new_pos = cPickle.loads(new_pos)
                value = 1
                id_id = int(id_id)
                if id_id == id_number:
                    value = 2
                grid.move_player(player_list[id_id], new_pos, value)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:  # movement for the player
            if event.key in status_dict:
                to_send = cPickle.dumps(status_dict[event.key]) + "," + str(id_number)
                if write is not None:
                    write.send(to_send)

    grid.draw_grid()
    screen.blit(font.render(str(grid.score), True, RED), [10, 10])
    pygame.display.flip()
if done == 1:
    print "ghosts have won"
if done == 2:
    print "pac-man won"
my_socket.close()
raw_input("game over, you may exit")