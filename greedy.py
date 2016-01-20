__author__ = 'guypc'

import pygame


def do_grid(row_block_num, column_block_num):
    num_of_dots = 0
    for row in range(row_block_num):
        row_progress = (row * width) + (margin * row) + margin
        for column in range(column_block_num):
            progress = (column * width) + (margin * column)
            if grid[row][column] == 1:
                pygame.draw.rect(screen, GREEN, [progress + margin, row_progress, width, height])
            elif grid[row][column] == 3:
                pygame.draw.rect(screen, YELLOW, [progress + margin, row_progress, width, height])
                num_of_dots += 1
            elif grid[row][column] == 0:
                pygame.draw.rect(screen, WHITE, [progress + margin, row_progress, width, height])
    return num_of_dots


def is_dot_next(current_row, current_column):
    if grid[current_row][current_column] == 3:
        return True
    return False


def move_up(current_row, current_column, score):
    if current_row != 0:
        grid[current_row][current_column] = 0
        current_row -= 1
        if is_dot_next(current_row, current_column):
            score += 1
    grid[current_row][current_column] = 1
    return current_row, current_column, score


def move_down(current_row, current_column, score):
    if current_row != row_block_num - 1:
        grid[current_row][current_column] = 0
        current_row += 1
        if is_dot_next(current_row, current_column):
            score += 1
        grid[current_row][current_column] = 1
    return current_row, current_column, score


def move_left(current_row, current_column, score):
    if current_column != 0:
        grid[current_row][current_column] = 0
        current_column -= 1
    if is_dot_next(current_row, current_column):
        score += 1
    grid[current_row][current_column] = 1
    return current_row, current_column, score


def move_right(current_row, current_column, score):
    if current_column != column_block_num - 1:
        grid[current_row][current_column] = 0
        current_column += 1
    if is_dot_next(current_row, current_column):
        score += 1
    grid[current_row][current_column] = 1
    return current_row, current_column, score


pygame.init()
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
row_block_num = 5
column_block_num = 5
screen_height = 25.25 * row_block_num
screen_width = 25.25 * column_block_num
size = (int(screen_width), int(screen_height))
font = pygame.font.SysFont('Calibri', 25, True, False)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("New game")

score = 0
done = False
clock = pygame.time.Clock()
width = 20
height = 20
margin = 5
grid = []
for row in range(row_block_num):
    grid.append([])
    for column in range(column_block_num):
        grid[row].append(3)
current_row = 0
current_column = 0
grid[current_row][current_column] = 1
num_of_dots = do_grid(row_block_num, column_block_num)
screen.blit(font.render(str(score), True, RED), [10, 10])
pygame.display.flip()
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                current_row, current_column, score = move_up(current_row, current_column, score)
            if event.key == pygame.K_DOWN:
                current_row, current_column, score = move_down(current_row, current_column, score)
            if event.key == pygame.K_LEFT:
                current_row, current_column, score = move_left(current_row, current_column, score)
            if event.key == pygame.K_RIGHT:
                current_row, current_column, score = move_right(current_row, current_column, score)
    num_of_dots = do_grid(row_block_num, column_block_num)
    if num_of_dots == 0:
        done = True
    screen.blit(font.render(str(score), True, RED), [10, 10])
    pygame.display.flip()
