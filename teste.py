from collections import namedtuple

def move(dir, player):
    global d
    if dir in d:
        return (d[dir].x + player.x, d[dir].y + player.y)

a = namedtuple("player position",["x", "y"])
d = {"up" : a(0,1), "down" : a(0,-1)}
player = namedtuple("player position", ["x", "y"])
print move("down", move("up", player))