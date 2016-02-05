__author__ = 'guypc'

import pygame
from GameClass import *
import socket
import select

#declarin color variables and color list
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
color_list = [WHITE, GREEN, BLUE, YELLOW]

#establishing connection with QServer
my_socket = socket.socket()
my_socket.connect(("127.0.0.1", 6845))
my_socket.send("ip:port")

print "waiting for more players to connect"



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
done = False
clock = pygame.time.Clock()


#declaring player position and drawing the grid
current_row = 1
current_column = 1
player = Player(current_row, current_column)  # <--- declare the player, as an object, NOT A TUPLE
grid = Greed(row_block_num, column_block_num, screen, player)  # <---- the game board, NOT AN ARRAY FFS GUY
num_of_dots = grid.draw_grid()
screen.blit(font.render(str(grid.score), True, RED), [10, 10])
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
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:  # movement for the player
            if event.key in status_dict:
                grid.move_player(player, direction=status_dict[event.key])
    if num_of_dots == 0:
        done = True
    grid.draw_grid()
    screen.blit(font.render(str(grid.score), True, RED), [10, 10])
    pygame.display.flip()