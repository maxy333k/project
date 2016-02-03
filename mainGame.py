__author__ = 'guypc'

import pygame
from GameClass import *

#declarin color variables and color list
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
color_list = [WHITE, GREEN, BLUE, YELLOW]

#declaring general variables
row_block_num = 5
column_block_num = 5
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

status_dict = {pygame.K_UP: "up",
               pygame.K_DOWN: "down",
               pygame.K_LEFT: "left",
               pygame.K_RIGHT: "right",
               pygame.K_w: "up",
               pygame.K_s: "down",
               pygame.K_a: "left",
               pygame.K_d: "right"}

#main game loop
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:  # movement for the player
            if event.key in status_dict:
                grid.move_player(player, status_dict[event.key])
    if num_of_dots == 0:
        done = True
    grid.draw_grid()
    screen.blit(font.render(str(grid.score), True, RED), [10, 10])
    pygame.display.flip()