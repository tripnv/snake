import math
import numpy as np


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Snake:
    pass

action_space_dir = {
        "up": (-1,0),
        "down": (1,0),
        "left": (0,-1),
        "right": (0,1)
        }

class Environment:
    """The board itself"""
    def __init__(self, board_size = 10):
        self.board_size = board_size
        self.board = self.initialize_board()

    def initialize_board(self):
        """ Initialize board environment and set the borders """
        board = np.zeros((self.board_size, self.board_size))
        board[:1,:] = -1
        board[-1:, :] = -1
        board[:, :1] = -1
        board[:, -1:] = -1
        return board

    def update_board(self):
        pass
    def __repr__(self):
        print(self.board)

env = Environment()
env.__repr__()
