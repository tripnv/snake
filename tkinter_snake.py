import tkinter as tk
import random
import copy

action_space_dir = {
        "Up": (0,-1),
        "Down":(0,1),
        "Left":(-1,0),
        "Right":(1,0)
        }

game_states = {
        "ALIVE":1,
        "DEAD":0
        }

class Unit:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def as_list(self):
        return [self.x, self.y]

class Environment():

    def __init__(self, pseudo_grid_size):
        #Environment attributes
        self.window = tk.Tk()
        self.gridsize = pseudo_grid_size + 2
        self.action_range = pseudo_grid_size
        self.unit_size = 30
        self.unit_space = 0
        self.time_unit = 250
        self.diagnostics = 0
        self.height = self.gridsize * self.unit_size + (self.gridsize-1) * self.unit_space
        
        self.score = 0
        self.game_state = 1
        self.canvas = tk.Canvas(self.window, bg = "white", height = self.height,  width = self.height)
        self.snake = Snake(1,1)
        self.food = Food()
        self.tail_copy = None
        self.canvas.pack()
        self.action()

        self.window.bind("<Up>", self.assign_direction)
        self.window.bind("<Down>",self.assign_direction)
        self.window.bind("<Left>", self.assign_direction)
        self.window.bind("<Right>", self.assign_direction)

        self.window.mainloop()



    def draw_borders(self, grid_size, height, unit_size, unit_space):

        x_index = 0
        y_index = 0

        while x_index < height:
            self.canvas.create_rectangle(x_index, y_index,
                    x_index + unit_size, y_index + unit_size,
                    fill = "grey", outline = "white")
            self.canvas.create_rectangle(x_index, height - y_index,
                    x_index + unit_size, height - y_index - unit_size,
                    fill = "grey", outline = "white" )

            x_index = x_index + unit_size + unit_space

        x_index = 0
        y_index = 0

        while y_index < height:
            self.canvas.create_rectangle(x_index, y_index,
                    x_index+unit_size, y_index + unit_size,
                    fill = "grey", outline = "white")

            self.canvas.create_rectangle(height - x_index, y_index,
                    height - x_index - unit_size, y_index + unit_size,
                    fill = "grey", outline = "white")

            y_index = y_index + unit_size + unit_space

    def render_snake(self):
        #should include head and tail render
        self.canvas.create_rectangle(\
                self.snake.head.x * self.unit_size + self.unit_space,
                self.snake.head.y * self.unit_size + self.unit_space,
                self.snake.head.x * self.unit_size + self.unit_size + self.unit_space,
                self.snake.head.y * self.unit_size + self.unit_size + self.unit_space,
                                            fill = "green3", outline = "white")
        if self.snake.length > 1:
            for unit in self.snake.tail:
                self.canvas.create_rectangle(
                    unit[0] * self.unit_size,
                    unit[1] * self.unit_size,
                    unit[0] * self.unit_size + self.unit_size,
                    unit[1] * self.unit_size + self.unit_size,
                    fill = "green2", outline = "white"
                    )

        if self.diagnostics == 1:
            self.canvas.create_text(self.height/2, self.height/2, text = str(self.snake.tail))
            self.canvas.create_text(self.height/2 + 15, self.height/2 + 15, text = str(self.snake.state), fill ="red")
            self.canvas.create_text(self.height/2, self.height/2, text = str(self.get_occupied_squares()))
    
    def render_food(self):
        self.canvas.create_rectangle(\
                self.food.position.x * self.unit_size,
                self.food.position.y * self.unit_size,
                self.food.position.x * self.unit_size + self.unit_size,
                self.food.position.y * self.unit_size + self.unit_size,
                                            fill = "red", outline = "white")


    def check_game_state(self):
        #border check
        if self.snake.head.x > self.action_range  or self.snake.head.y > self.action_range:
            self.game_state = 0
        elif self.snake.head.x < 1 or self.snake.head.y < 1:
            self.game_state = 0

        #self check
        if [self.snake.head.x, self.snake.head.y] in self.snake.tail:
            self.game_state = 0

    def action(self):
        self.canvas.delete(tk.ALL)
        if self.game_state:
            self.snake.update_snake()
            self.draw_borders(self.gridsize, self.height, self.unit_size, self.unit_space)
            self.canvas.create_text(self.unit_size/2 + 1, self.unit_size/2 + 1,font = ("gregorian", 12, "bold"), text = str(self.snake.length), fill = "red")
            self.render_food()
            self.render_snake()

            self.check_game_state()

            if self.food.position.x == self.snake.head.x and self.food.position.y == self.snake.head.y:
                occ_sq = self.get_occupied_squares()
                self.food.position = self.food.generate_food(occ_sq)
                self.snake.increase_tail()

        else:
            self.score = self.snake.length
            self.canvas.create_text(self.height/2, self.height/2, font = ("microsoft tai lee", 25), text = 'GAME OVER')
            self.canvas.create_text(self.height/2, self.height/2 + 25,font = ("gregorian", 12, "bold"), text = "Score: {}".format(self.score), fill = "red")
            self.canvas.update()
            return 0


        self.canvas.after(self.time_unit, self.action)

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
    def __init__(self, x, y):
        self.direction = "Right"
        self.length = 1
        self.head = Unit(1,1)
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
        x = [random.randrange(1,21), random.randrange(1,21)]
        while True:
            if x not in occupied_squares:
                return Unit(x[0], x[1])


def main():
    env = Environment(20)

if __name__ == "__main__":
    main()
