from Tkinter import *
from random import randint
import copy

WIDTH = 401
HEIGHT = 401
CELL_SIZE = 4
DELAY = 10
CELL_DENSITY = 7


class Board(Frame):
    """Grid area"""

    cells = list()

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.canvas = Canvas(parent, width=WIDTH, height=HEIGHT, bd=-2)
        self.canvas.grid(row=0, column=0, pady=(0, 12))

        self.automaton = StringVar()
        self.automaton.set("life")
        self.life = Radiobutton(parent, text="Conway's game of life", variable=self.automaton, value="life",
                                indicatoron=0)
        self.life.grid(row=1, column=0, sticky=W + E)

        self.seeds = Radiobutton(parent, text="Seeds", variable=self.automaton, value="seeds", indicatoron=0)
        self.seeds.grid(row=2, column=0, sticky=W + E)

    def init_cells(self):
        state = list()
        for x in range(0, WIDTH / CELL_SIZE):
            column = list()
            column_state = list()
            for y in range(0, HEIGHT / CELL_SIZE):
                if randint(1, 100) >= 100 - CELL_DENSITY:
                    color = "black"
                    column_state.append(1)
                else:
                    color = "white"
                    column_state.append(0)
                column.append(self.canvas.create_rectangle(x * CELL_SIZE, y * CELL_SIZE, (x + 1) * CELL_SIZE,
                                                            (y + 1) * CELL_SIZE, fill=color))

            self.cells.append(column)
            state.append(column_state)

        return state

    def update_cells(self, state):
        for x in range(0, WIDTH / CELL_SIZE):
            for y in range(0, HEIGHT / CELL_SIZE):
                if state[x][y] != self.get_state(x, y):
                    self.toggle_color(x, y)

    def get_state(self, x, y):
        return self.canvas.itemcget(self.cells[x][y], "fill") == "black"

    def toggle_color(self, x, y):
        if self.get_state(x, y):
            self.canvas.itemconfigure(self.cells[x][y], fill="white")
        else:
            self.canvas.itemconfigure(self.cells[x][y], fill="black")


class Life(object):
    """Main game loop."""

    state = list()

    def __init__(self, parent):
        self.parent = parent
        self.board = Board(parent)
        self.state = self.board.init_cells()
        self.animate()

    def animate(self):
        if self.board.automaton.get() == "life":
            self.game_of_life()
        elif self.board.automaton.get() == "seeds":
            self.seeds()

        self.board.update_cells(self.state)
        self.parent.after(DELAY, self.animate)

    def game_of_life(self):
        new_state = copy.deepcopy(self.state)
        for x in range(0, WIDTH / CELL_SIZE):
            for y in range(0, HEIGHT / CELL_SIZE):
                neighbours = self.count_neighbours(x, y)

                if self.state[x][y]:
                    # under-population
                    if neighbours < 2:
                        new_state[x][y] = not self.state[x][y]
                    # survival
                    elif neighbours == 2 or neighbours == 3:
                        pass
                    # overcrowding
                    else:
                        new_state[x][y] = not self.state[x][y]
                else:
                    # reproduction
                    if neighbours == 3:
                        new_state[x][y] = not self.state[x][y]

        self.state = new_state

    def seeds(self):
        new_state = copy.deepcopy(self.state)
        for x in range(0, WIDTH / CELL_SIZE):
            for y in range(0, HEIGHT / CELL_SIZE):
                neighbours = self.count_neighbours(x, y)

                if not self.state[x][y] and neighbours == 2:
                    new_state[x][y] = not self.state[x][y]
                else:
                    new_state[x][y] = 0

        self.state = new_state

    def count_neighbours(self, x, y):
        canvas = self.board.canvas
        neighbours = 0
        # north
        if y != 0:
            if self.state[x][y - 1]:
                neighbours += 1
        # north-east
        if x < WIDTH / CELL_SIZE - 1 and y != 0:
            if self.state[x + 1][y - 1]:
                neighbours += 1
        # north-west
        if x != 0 and y != 0:
            if self.state[x - 1][y - 1]:
                neighbours += 1
        # south
        if y < HEIGHT / CELL_SIZE - 1:
            if self.state[x][y + 1]:
                neighbours += 1
        # south-east
        if x < WIDTH / CELL_SIZE - 1 and y < HEIGHT / CELL_SIZE - 1:
            if self.state[x + 1][y + 1]:
                neighbours += 1
        # south-west
        if x != 0 and y < HEIGHT / CELL_SIZE - 1:
            if self.state[x - 1][y + 1]:
                neighbours += 1
        # east
        if x < WIDTH / CELL_SIZE - 1:
            if self.state[x + 1][y]:
                neighbours += 1
        # west
        if x != 0:
            if self.state[x - 1][y]:
                neighbours += 1

        return neighbours

if __name__ == "__main__":
    root = Tk()
    root.title("Life")
    root.resizable(width=FALSE, height=FALSE)
    life = Life(root)

    root.mainloop()
