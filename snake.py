import math
import time
import numpy as np
import curses

class Point:
    """ Coordinates of a snake unit """
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Snake:
    """ Contains head and tail """
    pass

action_space_dir = {
        "UP": (-1,0),
        "DOWN": (1,0),
        "LEFT": (0,-1),
        "RIGHT": (0,1)
        }

class Environment:
    """The board itself"""
    def __init__(self, board_size = 10):
        self.board_size = board_size
        self.point =  Point(1,1)
        self.direction = "RIGHT"
        self.screen.
        while(True):
            #game logic and display should be separated
            print("\033c")
            self.board = self.reset_board()
            self.update_board(self.point)
            self.__repr__()
            self.user_input()
            self.point = self.update_point(self.point,action_space_dir[self.direction])
            time.sleep(1)
            if self.board[self.point.x,self.point.y] == -1:
                #game_state should be added
                print("GAME OVER")
                break

    def update_point(self, point, direction):
        """given a point and direction return the next point"""
        x_dir, y_dir = direction[0], direction[1]
        point.x += x_dir
        point.y += y_dir
        return point

    def reset_board(self):
        """ Initialize board environment and set the borders """
        board = np.zeros((self.board_size, self.board_size))
        board[:1,:] = -1
        board[-1:, :] = -1
        board[:, :1] = -1
        board[:, -1:] = -1
        return board

    def update_board(self, initial_point):
        self.board[initial_point.x, initial_point.y] = 5
    def user_input(self):
        pass
    def __repr__(self):
        print(self.board)

env = Environment()
