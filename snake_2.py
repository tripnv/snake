import random
import time
import numpy as np
import cv2


action_space_dir = {
        "Up": (0,-1),
        "Down":(0,1),
        "Left":(-1,0),
        "Right":(1,0)
        }
action_space_list = ["Up", "Down", "Left", "Right"]



COLORS = {
    "GRAY":(225,225,225),
    "RED":(0,0,250),
    "LIME":(0,255,0),
    "GREEN":(0,128,0)
        }

GRID_SIZE = 10

class Unit:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def as_list(self):
        return [self.x, self.y]

class Environment:
    """ Function guide from: https://github.com/openai/gym/blob/master/gym/core.py """ 

    action_space_ids = {
        0:"Up",
        1:"Down",
        2:"Left",
        3:"Right",
        }
    
    game_states = {
        "ATE":2,
        "ALIVE":1,
        "DEAD":0,
        }

    metadata = {'render.modes': ['human', 'rgb_array', 'ansi']}
    

    def __init__(self):
        super(Environment).__init__()

        #Environment attributes
        self.gridsize = GRID_SIZE  
        self.action_range = GRID_SIZE
        self.unit_size = 10 #px
        self.unit_space = 0
        self.time_unit = 1
        self.height = self.gridsize * self.unit_size


    def reset(self):
        

        #Environment variables
        self.score = 0
        self.game_state = self.game_states['ALIVE'] 
        #Elements within the environment
        self.snake = Snake()
        self.food = Food()
        self.tail_copy = None

        self.canvas = np.ones((self.height, self.height, 3), dtype = np.float32)
        self.draw_to_canvas()

    def close(self):
        cv2.destroyAllWindows()

    def update_environment(self, direction):
        
        self.canvas = np.ones((self.height, self.height, 3), dtype = np.float32)
        
        #choose direction
        assert direction in self.action_space_ids, 'Invalid action'
        self.snake.direction = self.action_space_ids[direction]
        self.snake.update_snake()
        self.draw_to_canvas()
        
        self.game_state = self.game_states['ALIVE']
        #check game_state: border, running into itself 
        self.check_snake_state()
        #check eating  
        self.check_food_collision()
        
        return self.game_state 

    def check_snake_state (self):
        #border check
        if self.snake.head.x > self.action_range - 1  or self.snake.head.y > self.action_range - 1:
            self.game_state = self.game_states['DEAD']
        elif self.snake.head.x < 1 or self.snake.head.y < 1:
            self.game_state = self.game_states['DEAD']
        #self check
        if [self.snake.head.x, self.snake.head.y] in self.snake.tail:
            self.game_state = self.game_states['DEAD'] 


    def check_food_collision(self):
        if self.food.position.x == self.snake.head.x and self.food.position.y == self.snake.head.y:
            occ_sq = self.get_occupied_squares()
            self.food.position = self.food.generate_food(occ_sq)
            self.snake.increase_tail()
            self.game_state = self.game_states["ATE"]

    def draw_to_canvas(self):
        self.draw_snake()
        self.draw_food()

    def render(self, mode = "ansi"):

        """ 
        - human: render to the current display or terminal and
          return nothing. Usually for human consumption.
        - rgb_array: Return an numpy.ndarray with shape (x, y, 3),
          representing RGB values for an x-by-y pixel image, suitable
          for turning into a video.
        - ansi: Return a string (str) or StringIO.StringIO containing a
          terminal-style text representation. The text can include newlines
          and ANSI escape sequences (e.g. for colors).
        """
        assert mode in ['human', 'rgb_array', 'ansi']
        
        if mode == 'human':
            cv2.imshow("canvas", self.canvas)
            cv2.waitKey(100)

        elif mode == 'rgb_array':
            return self.canvas

        elif mode == 'ansi':
            print("\nSnake head: {}, tail: {}".format(self.snake.head.as_list(),self.snake.tail))
            print("\nGame state: ",  self.game_state)
            print("\nApple position: {}".format(self.food.position.as_list()))
            print("\nScore: {}".format(self.snake.length))
            print("------------------")


    def draw_borders(self):
        #explicit borders has been removed
        x_index = 0
        y_index = 0
        while x_index < self.height:

            self.cavas = cv2.rectangle(
                   self.canvas,
                   (x_index,y_index),
                   (x_index + self.unit_size, y_index + self.unit_size),
                   color = COLORS["GRAY"], thickness = -1
                   )
            self.cavas = cv2.rectangle(
                   self.canvas,
                   (x_index,self.height - y_index),
                   (x_index + self.unit_size, self.height - y_index - self.unit_size),
                   color = COLORS["GRAY"], thickness = -1
                   )
            x_index =  x_index + self.unit_size

        x_index = 0
        y_index = 0

        while x_index < self.height:
            self.cavas = cv2.rectangle(
                   self.canvas,
                   (x_index,y_index),
                   (x_index + self.unit_size, y_index + self.unit_size),
                   color = COLORS["GRAY"], thickness = -1
                   )
            self.cavas = cv2.rectangle(
                   self.canvas,
                   (self.height - x_index, y_index),
                   (self.height - x_index - self.unit_size, y_index + self.unit_size),
                   color = COLORS["GRAY"], thickness = -1)
            y_index = y_index + self.unit_size



    def draw_snake(self):
        #should include head and tail render
        self.canvas = cv2.rectangle(
                self.canvas,
                (self.snake.head.x * self.unit_size + self.unit_space, self.snake.head.y * self.unit_size + self.unit_space),
                (self.snake.head.x * self.unit_size + self.unit_size + self.unit_space, self.snake.head.y * self.unit_size + self.unit_size + self.unit_space),
                color = COLORS["GREEN"], thickness = -1
                )

        if self.snake.length > 1:
            for unit in self.snake.tail:
                self.canvas = cv2.rectangle(self.canvas,
                    (unit[0] * self.unit_size, unit[1] * self.unit_size),
                    (unit[0] * self.unit_size + self.unit_size, unit[1] * self.unit_size + self.unit_size),
                    color  = COLORS["LIME"], thickness = -1
                    )

    def draw_food(self):
        self.canvas = cv2.rectangle(
                self.canvas,
                (self.food.position.x * self.unit_size, self.food.position.y * self.unit_size),
                (self.food.position.x * self.unit_size + self.unit_size, self.food.position.y * self.unit_size + self.unit_size),
                color = COLORS["RED"], thickness = -1
                )





    @staticmethod
    def opposite(direction):
        if direction == "Up":
            return "Down"
        elif direction == "Down":
            return "Up"
        elif direction == "Right":
            return "Left"
        elif direction == "Left":
            return "Right"

    def get_occupied_squares(self):
        occ_squares = []
        occ_squares.append(self.snake.head.as_list())
        occ_squares.extend(self.snake.tail)
        return occ_squares

    def assign_direction(self, event):
        new_direction = event.keysym
        if self.snake.length > 1:
            if self.snake.direction == self.opposite(new_direction):
                pass
            else:
                self.snake.direction = new_direction
        else:
            self.snake.direction = new_direction


class Snake:
    def __init__(self):
        self.direction = random.choice(action_space_list)
        self.length = 1
        self.head = Unit(random.randrange(0,GRID_SIZE),random.randrange(0,GRID_SIZE))
        
        self.tail = []
        self.state = 0  #Switch it to true once the snake ate

    def increase_tail(self):
        #list of unit coordinates
        #special case: only head

        if self.length == 1:
            self.tail.append(self.head.as_list())
        else:
            self.state = 1

        self.length += 1


    def update_snake(self):
        direction_tuple = action_space_dir[self.direction]
        x_dir, y_dir = direction_tuple[0], direction_tuple[1]
        head_previous_state = [self.head.x, self.head.y]
        self.head.x += x_dir
        self.head.y += y_dir
        if self.length > 1:
            if self.state == 0:
                tail_copy = self.tail
                self.tail.insert(0, head_previous_state)
                self.tail.pop()
            else:
                self.tail.insert(0, head_previous_state)
                self.state = 0

    def body_to_list(self):
        body = self.tail.insert(0, self.head.as_list())
        return body

class Food:
    def __init__(self):
        self.position = self.generate_food([])

    @staticmethod
    def generate_food(occupied_squares):
        x = [random.randrange(0,GRID_SIZE), random.randrange(0, GRID_SIZE)]
        while True:
            if x not in occupied_squares:
                return Unit(x[0], x[1])

# Test function
# def main():
    # env = Environment()
    # env.reset()
    # while(env.game_state):
        # env.update_environment(random.sample([0, 1, 2, 3], 1)[0])
        # env.render(mode = "human")

# if __name__ == "__main__":
    # main()
