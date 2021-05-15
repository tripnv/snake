import tkinter as tk
action_space_dir = {
        "Up": (0, -1),
        "Down":(0,1),
        "Left":(-1,0),
        "Right":(1,0)
        }

game_states = {
        "ALIVE":1,
        "DEAD":0
        }

class Coord:

    def __init__(self, x, y):
        self.x = x
        self.y = y

class Environment():

    def __init__(self, pseudo_grid_size):
        #Environment attributes
        self.window = tk.Tk()
        self.gridsize = pseudo_grid_size + 2
        self.action_range = pseudo_grid_size
        self.unit_size = 30
        self.unit_space = 0
        self.time_unit = 500
        self.height = self.gridsize * self.unit_size + (self.gridsize-1) * self.unit_space

        self.game_state = 1
        self.canvas = tk.Canvas(self.window, bg = "white", height = self.height,  width = self.height)
        self.snake = Snake(1,1)
        self.render_snake()

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
            self.canvas.create_rectangle(x_index, y_index, x_index + unit_size, y_index + unit_size,
                    fill = "grey", outline = "white")
            self.canvas.create_rectangle(x_index, height - y_index,
                    x_index + unit_size, height - y_index - unit_size,
                    fill = "grey", outline = "white" )

            x_index = x_index + unit_size + unit_space

        x_index = 0
        y_index = 0

        while y_index < height:
            self.canvas.create_rectangle(x_index, y_index,
                    x_index+unit_size, y_index + unit_size, fill = "grey", outline = "white")

            self.canvas.create_rectangle(height - x_index, y_index,
                    height - x_index - unit_size, y_index + unit_size, fill = "grey", outline = "white")

            y_index = y_index + unit_size + unit_space

    def render_snake(self):
        return self.canvas.create_rectangle(\
                self.snake.head.x * self.unit_size + self.unit_space,
                self.snake.head.y * self.unit_size + self.unit_space,
                self.snake.head.x * self.unit_size + self.unit_size + self.unit_space,
                self.snake.head.y * self.unit_size + self.unit_size + self.unit_space,
                                            fill = "green", outline = "white")
    def check_game_state(self):
        #border check
        if self.snake.head.x > self.action_range + 1 or self.snake.head.y > self.action_range + 1:
            self.game_state = 0
        elif self.snake.head.x < 1 or self.snake.head.y < 1:
            self.game_state = 0

        #self check
    def action(self):
        self.canvas.delete(tk.ALL)
        if self.game_state:
            self.canvas.after(self.time_unit, self.action)
            self.draw_borders(self.gridsize, self.height, self.unit_size, self.unit_space)
            self.render_snake()
            self.snake.update_head_position()
            self.check_game_state()
        else:
            self.canvas.create_text(self.height/2, self.height/2, text = 'GAME OVER')
            self.canvas.update()
            return 0

    def assign_direction(self, event):
        new_direction = event.keysym
        self.snake.direction = new_direction


class Snake:
    def __init__(self, x, y):
        self.direction = "Right"
        self.init_head(x,y)
        self.init_tail()

    def init_head(self, x, y):
        self.head = Coord(x,y)

    def init_tail(self):
        #list of unit coordinates
        #each unit takes the place of the previous unit
        #special case: only head
        pass

    def update_head_position(self):
        direction_tuple = action_space_dir[self.direction]
        x_dir, y_dir = direction_tuple[0], direction_tuple[1]
        self.head.x += x_dir
        self.head.y += y_dir

    def render(self):
        pass

def main():
    env = Environment(20)
if __name__ == "__main__":
    main()
