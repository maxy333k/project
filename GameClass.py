__author__ = 'User'


import pygame


class Player:  # class that deals with the player
    def __init__(self, current_row, current_column):
        self.x = current_row
        self.y = current_column

    def get_pose(self):
        return self.x, self.y

    def set_pose(self, x, y):
        self.x = x
        self.y = y

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)  # blank space, num 0
GREEN = (0, 255, 0)  # player, num 1
RED = (255, 0, 0)
BLUE = (0, 0, 255)  # wall, num 2
YELLOW = (255, 255, 0)  # dot that a player need to eat, num 3


class Greed:  # game-board class
    def __init__(self, row_block_num, column_block_num, screen, player):  # work, don't touch it
        self.num_of_dots = 0
        self.width = 20
        self.height = 20
        self.margin = 5
        self.row_block_num = row_block_num
        self.column_block_num = column_block_num
        self.screen = screen
        self.grid = []

        # declaring the grid as a kind of 2d array but with list
        for i in xrange(row_block_num):
            self.grid.append([])
            for j in xrange(column_block_num):
                self.grid[i].append(3)

        #add the player to the grid
        self.player = player
        self.place_player(self.player)

    def draw_grid(self):  # work, don't touch it
        for row in range(self.row_block_num):
            row_progress = (row * self.width) + (self.margin * row) + self.margin
            for column in range(self.column_block_num):
                progress = (column * self.width) + (self.margin * column)
                if self.grid[row][column] == 1:  # player spot
                    pygame.draw.rect(self.screen, GREEN, [progress + self.margin, row_progress, self.width, self.height])
                elif self.grid[row][column] == 3:  # point that pac-man will eat
                    pygame.draw.rect(self.screen, YELLOW, [progress + self.margin, row_progress, self.width, self.height])
                    self.num_of_dots += 1
                elif self.grid[row][column] == 0:  # blank space
                    pygame.draw.rect(self.screen, WHITE, [progress + self.margin, row_progress, self.width, self.height])
        return self.num_of_dots

    def change_pos(self, player, new_x, new_y):  # MUST BE DONE

        pass

    def place_player(self, player):  # placing the player on the grid,  works at least
        x, y = player.get_pose()
        self.grid[x][y] = 1