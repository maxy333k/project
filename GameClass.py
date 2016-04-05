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

    def __str__(self):
        return "(" + self.x + "," + self.y + ")"


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)  # blank space, num 0
GREEN = (0, 255, 0)  # player, num 1
RED = (255, 0, 0)
BLUE = (0, 0, 255)  # you, num 2
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

    def __init__(self, row_block_num, column_block_num, role):  # work, don't touch it
        self.num_of_dots = 0
        self.width = 20
        self.height = 20
        self.margin = 5
        self.row_block_num = row_block_num
        self.column_block_num = column_block_num
        self.grid = []
        self.score = 0

        # declaring the grid as a kind of 2d array but with list
        for i in xrange(row_block_num):
            self.grid.append([])
            for j in xrange(column_block_num):
                self.grid[i].append(role)

    def add_screen(self, screen):
        self.screen = screen

    def draw_grid(self):  # work, don't touch it (draw the grid on the screen)
        for row in range(self.row_block_num):
            row_progress = (row * self.width) + (self.margin * row) + self.margin
            for column in range(self.column_block_num):
                progress = (column * self.width) + (self.margin * column)
                pygame.draw.rect(self.screen, color_list[self.grid[row][column]], [progress + self.margin, row_progress,
                                                                                   self.width, self.height])
                if self.grid[row][column] == 3:
                    self.num_of_dots += 1
        return self.num_of_dots

    def move_player(self, player, direction, value):  # move the player according to the direction
        x, y = player.get_pose()
        new_x, new_y = direction
        self.grid[x][y] = 0
        x = (x + new_x + self.column_block_num) % self.column_block_num
        y = (y + new_y + self.row_block_num) % self.row_block_num
        if self.is_dot_next(x, y):
            self.num_of_dots -= 1
            self.score += 1
        self.change_pos(player, x, y, value)

    # placing the player on the grid,  works at least (place the player on the grid)
    def place_player(self, player, value):
        x, y = player.get_pose()
        self.grid[x][y] = value

    def is_dot_next(self, current_row, current_column):  # return if the next position of the player is a dot
        if self.grid[current_row][current_column] == 3:
            return True
        return False

    def change_pos(self, player, new_x, new_y, value):  # (change the player position)
        player.set_pose(new_x, new_y)
        self.place_player(player, value)

    def get_place_info(self, x, y):
        return self.grid[x][y]

    def get_num_of_dots(self):
        return self.num_of_dots

    def check_next_pos_by_status(self, player, status):
        x, y = player.get_pose()
        new_x, new_y = status
        x = (x + new_x + self.column_block_num) % self.column_block_num
        y = (y + new_y + self.row_block_num) % self.row_block_num
        if self.is_dot_next(x, y):
            return 3
        return self.get_place_info(x, y)