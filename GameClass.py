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
color_list = [WHITE, GREEN, BLUE, YELLOW]


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
        self.score = 0

        # declaring the grid as a kind of 2d array but with list
        for i in xrange(row_block_num):
            self.grid.append([])
            for j in xrange(column_block_num):
                self.grid[i].append(3)

        #add the player to the grid
        self.player = player
        self.place_player(self.player)

    def draw_grid(self):  # work, don't touch it (draw the grid on the screen)
        for row in range(self.row_block_num):
            row_progress = (row * self.width) + (self.margin * row) + self.margin
            for column in range(self.column_block_num):
                progress = (column * self.width) + (self.margin * column)
                pygame.draw.rect(self.screen, color_list[self.grid[row][column]], [progress + self.margin, row_progress,
                                                                                   self.width, self.height])
                if self.grid[row][column]:
                    self.num_of_dots += 1
        return self.num_of_dots

    def move_player(self, player, direction):  # move the player according to the direction
        x, y = player.get_pose()
        new_x, new_y = direction
        self.grid[x][y] = 0
        x += new_x
        y += new_y

        if x < 0:
            x = self.column_block_num - 1
        if y < 0:
            y = self.row_block_num - 1
        if x == self.column_block_num:
            x = 0
        if y == self.row_block_num:
            y = 0

        if self.is_dot_next(x, y):
            self.num_of_dots -= 1
            self.score += 1
        self.change_pos(player, x, y)

    def place_player(self, player):  # placing the player on the grid,  works at least (place the player on the grid)
        x, y = player.get_pose()
        self.grid[x][y] = 1

    def is_dot_next(self, current_row, current_column):  # return if the next position of the player is a dot
        if self.grid[current_row][current_column] == 3:
            return True
        return False

    def change_pos(self, player, new_x, new_y):  # (change the player position)
        player.set_pose(new_x, new_y)
        self.place_player(player)