__author__ = 'User'

class Player:
    def __init__(self, current_row, current_column):
        self.x = current_row
        self.y = current_column

    def get_pose(self):
        return self.x, self.y
    