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
    def __init__(self):
        self.head = Point(1,1)
        self.head_direction = "DOWN"
        self.tail = []

    def set_direction(self, pressed_key):
        
        if pressed_key == 126:
            self.head_direction = "UP"
        if pressed_key == 125:
            self.head_direction = "DOWN"
        if pressed_key == 123:
            self.head_direction = "LEFT"
        if pressed_key == 124:
            self.head_direction = "RIGHT"
        

        
    def update_snake(self):
        current_dir = action_space_dir[self.head_direction]
        x_dir, y_dir = current_dir[0], current_dir[1]
        
        #update snake head 
        self.head.x += x_dir
        self.head.y += y_dir
        
        #update snake tail
        

action_space_dir = {
        "UP": (-1,0),
        "DOWN": (1,0),
        "LEFT": (0,1),
        "RIGHT": (0,-1)
        }

game_states = {
        "ALIVE": 1,
        "GAME OVER": 0
        }

class Environment:
    """The board itself"""
    def __init__(self, board_size = 10):
        self.board_size = board_size
        self.snake = Snake()
        self.state = 1
        self.board = self.reset_board()
        self.board[self.snake.head.x, self.snake.head.y] = 1

    def update_board(self):
        """given a point and direction return the next point"""
        
        self.board[self.snake.head.x, self.snake.head.y] = 0
        self.snake.update_snake()
        if self.board[self.snake.head.x, self.snake.head.x] != 0:
            self.state = 0
        else:
            self.board[self.snake.head.x, self.snake.head.y] = 1


    def reset_board(self):
        """ Initialize board environment and set the borders """
        board = np.zeros((self.board_size, self.board_size))
        board[:1,:] = -1
        board[-1:, :] = -1
        board[:, :1] = -1
        board[:, -1:] = -1
        return board

    def board_to_string(self):
        return np.array2string(self.board)

    def __repr__(self):
        print(self.board)

def main(screen):
    #screen.timeout(0)
    screen.nodelay(1)
    curses.noecho()
    env = Environment()
    print("\033c")  
    
    while True:
    
        if env.state == False:
            print("GAME_OVER")
            time.sleep(10)
            break

        pressed_key = screen.getch()
        if pressed_key != -1:
            env.snake.set_direction(pressed_key)
        if pressed_key == 113:
            break
        screen.addstr(0,0, env.board_to_string())
        #screen.refresh()
        env.update_board()
        time.sleep(1)

if __name__ == "__main__":
    curses.wrapper(main)
