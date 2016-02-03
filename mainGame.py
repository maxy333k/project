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
score = 0
done = False
clock = pygame.time.Clock()
screen.blit(font.render(str(score), True, RED), [10, 10])

#declaring player position and drawing the grid
current_row = 2
current_column = 4
player = Player(current_row, current_column)  # <--- declare the player, as an object, NOT A TUPLE
grid = Greed(row_block_num, column_block_num, screen, player)  # <---- the game board, NOT AN ARRAY FFS GUY
num_of_dots = grid.draw_grid()
pygame.display.flip()

#main game loop
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:

            pass
    if num_of_dots == 0:
        done = True
    grid.draw_grid()
    screen.blit(font.render(str(score), True, RED), [10, 10])
    pygame.display.flip()