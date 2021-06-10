import random
import time
import gym
import numpy as np
import cv2
import matplotlib.pyplot as plt

action_space_dir = {
        "Up": (0,-1),
        "Down":(0,1),
        "Left":(-1,0),
        "Right":(1,0)
        }
action_space_list = ["Up", "Down", "Left", "Right"]

action_space_ids = {
        0:"Up",
        1:"Down",
        2:"Left",
        3:"Right",
        }

game_states = {
        "ALIVE":1,
        "DEAD":0
        }

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

class Environment(gym.Env):

    def __init__(self):
        super(Environment).__init__()

        #Environment attributes
        self.gridsize = GRID_SIZE + 2
        self.action_range = GRID_SIZE
        self.unit_size = 30 #px
        self.unit_space = 0
        self.time_unit = 1
        self.height = self.gridsize * self.unit_size + self.gridsize-1
        #Gym Env attributes
        self.observation_shape = (self.height, self.height, 3)
        self.observation_space = gym.spaces.Box(
                low = 0,
                high = 255,
                shape = (self.height, self.height, 3),
                dtype = np.float16)

        self.action_space = gym.spaces.Discrete(4,)


        self.reset() # is this the way? - Probably not


    def reset(self):


        #Environment variables
        self.score = 0
        self.game_state = 1

        #Elements within the environment
        self.canvas = np.ones(self.observation_shape)
        self.snake = Snake()
        self.food = Food()
        self.tail_copy = None
        self.reward = 0
        self.game_loop()

        #should  return observation
        return self.observation_space

    def close(self):
        cv2.destroyAllWindows()

    def step(self, direction = random.choice(action_space_list)):

        #choose direction
        self.snake.direction = direction
        self.snake.update_snake()

        if self.check_game_state():
            pass
            #return self.reward + 1

        #should return  observation, reward, done, info

    def game_loop(self):
        while(self.game_state):
            self.step()
            self.add_elements_to_canvas()
            self.render()

            if self.food.position.x == self.snake.head.x and self.food.position.y == self.snake.head.y:
                occ_sq = self.get_occupied_squares()
                self.food.position = self.food.generate_food(occ_sq)
                self.snake.increase_tail()
                self.reward += 10

            self.canvas = np.ones([self.height, self.height,3])

    def add_elements_to_canvas(self):
        self.draw_snake()
        self.draw_food()

    def render(self, mode = "human"):
        assert mode in ['human', 'console']
        if mode == 'human':
            cv2.imshow("canvas", self.canvas)
            cv2.waitKey(1000)
        elif mode == 'console':
            print("\n")
            print("Snake head: {}, tail: {}".format(self.snake.head.as_list(),self.snake.tail))

            print("\n")
            print("Apple position: {}".format(self.food.position.as_list()))

            print("\n")
            print("Score: {}".format(self.snake.length))
            print("------------------")
        #self.draw_borders()


        #  font = cv2.FONT_HERSHEY_SIMPLEX
        #  text_pos = (10,0)
        #  text_scale = 1
        #  text_color = (255,0,0)
        #  line_type = 2

        #  cv2.putText(self.canvas, str(self.score),
            #  text_pos,
            #  font,
            #  text_scale,
            #  text_color,
            #  line_type)


    def draw_borders(self):

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

    def check_game_state(self):
        #border check
        if self.snake.head.x > self.action_range  or self.snake.head.y > self.action_range:
            self.game_state = 0
            return True
        elif self.snake.head.x < 1 or self.snake.head.y < 1:
            self.game_state = 0
            return True
        #self check
        if [self.snake.head.x, self.snake.head.y] in self.snake.tail:
            self.game_state = 0
            return False





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
        self.head = Unit(random.randrange(1,GRID_SIZE + 1),random.randrange(1,GRID_SIZE + 1))
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
        x = [random.randrange(1,11), random.randrange(1,11)]
        while True:
            if x not in occupied_squares:
                return Unit(x[0], x[1])


def main():
    env = Environment()
if __name__ == "__main__":
    main()
