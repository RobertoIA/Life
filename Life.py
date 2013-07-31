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
        for x in range(0, WIDTH / CELL_SIZE):
            column = list()
            for y in range(0, HEIGHT / CELL_SIZE):
                color = "white"
                if randint(1, 100) >= 100 - CELL_DENSITY:
                    color = "black"
                column.append(self.canvas.create_rectangle(x * CELL_SIZE, y * CELL_SIZE, (x + 1) * CELL_SIZE,
                                                            (y + 1) * CELL_SIZE, fill=color))

            self.cells.append(column)

    def turn_white(self, x, y):
        self.canvas.itemconfigure(self.cells[x][y], fill="white")

    def turn_black(self, x, y):
        self.canvas.itemconfigure(self.cells[x][y], fill="black")

    #TODO en commit separado: get_color, toggle_color


class Life(object):
    """Main game loop."""

    def __init__(self, parent):
        self.parent = parent
        self.board = Board(parent)
        self.board.init_cells()
        self.animate()

    def animate(self):
        if self.board.automaton.get() == "life":
            self.game_of_life()
        elif self.board.automaton.get() == "seeds":
            self.seeds()

        self.parent.after(DELAY, self.animate)

    def game_of_life(self):
        canvas = self.board.canvas
        for x in range(0, WIDTH / CELL_SIZE):
            for y in range(0, HEIGHT / CELL_SIZE):
                neighbours = self.count_neighbours(x, y)

                if canvas.itemcget(self.board.cells[x][y], "fill") == "black":
                    # under-population
                    if neighbours < 2:
                        self.board.turn_white(x, y)
                    # survival
                    elif neighbours == 2 or neighbours == 3:
                        pass
                    # overcrowding
                    else:
                        self.board.turn_white(x, y)
                else:
                    # reproduction
                    if neighbours == 3:
                        self.board.turn_black(x, y)

    def seeds(self):
        canvas = self.board.canvas
        new_cells = copy.deepcopy(self.board.cells)
        for x in range(0, WIDTH / CELL_SIZE):
            for y in range(0, HEIGHT / CELL_SIZE):
                neighbours = self.count_neighbours(x, y)

                if canvas.itemcget(self.board.cells[x][y], "fill") == "white" and neighbours == 2:
                    self.board.turn_black(x, y)
                else:
                    self.board.turn_white(x, y)

        self.board.cells = new_cells

    def count_neighbours(self, x, y):
        canvas = self.board.canvas
        neighbours = 0
        # north
        if y != 0:
            if canvas.itemcget(self.board.cells[x][y - 1], "fill") == "black":
                neighbours += 1
            # north-east
        if x < WIDTH / CELL_SIZE - 1 and y != 0:
            if canvas.itemcget(self.board.cells[x + 1][y - 1], "fill") == "black":
                neighbours += 1
            # north-west
        if x != 0 and y != 0:
            if canvas.itemcget(self.board.cells[x - 1][y - 1], "fill") == "black":
                neighbours += 1
            # south
        if y < HEIGHT / CELL_SIZE - 1:
            if canvas.itemcget(self.board.cells[x][y + 1], "fill") == "black":
                neighbours += 1
            # south-east
        if x < WIDTH / CELL_SIZE - 1 and y < HEIGHT / CELL_SIZE - 1:
            if canvas.itemcget(self.board.cells[x + 1][y + 1], "fill") == "black":
                neighbours += 1
            # south-west
        if x != 0 and y < HEIGHT / CELL_SIZE - 1:
            if canvas.itemcget(self.board.cells[x - 1][y + 1], "fill") == "black":
                neighbours += 1
            # east
        if x < WIDTH / CELL_SIZE - 1:
            if canvas.itemcget(self.board.cells[x + 1][y], "fill") == "black":
                neighbours += 1
            # west
        if x != 0:
            if canvas.itemcget(self.board.cells[x - 1][y], "fill") == "black":
                neighbours += 1

        return neighbours

if __name__ == "__main__":
    root = Tk()
    root.title("Life")
    root.resizable(width=FALSE, height=FALSE)
    life = Life(root)

    root.mainloop()
