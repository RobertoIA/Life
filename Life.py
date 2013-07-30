from Tkinter import *
from random import randint
import copy

WIDTH = 300
HEIGHT = 300
CELL_SIZE = 4
DELAY = 30
CELL_DENSITY = 7


class Board(Frame):
    """Grid area"""

    tiles = dict()

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.canvas = Canvas(parent, width=WIDTH, height=HEIGHT, bd=-2)
        self.canvas.grid(row=0, column=0)

        self.automaton = StringVar()
        self.automaton.set("life")
        self.life = Radiobutton(parent, text="Conway's game of life", variable=self.automaton, value="life")
        self.life.grid(row=1, column=0, sticky=W)

        self.seeds = Radiobutton(parent, text="Seeds", variable=self.automaton, value="seeds")
        self.seeds.grid(row=2, column=0, sticky=W)

    def draw_cell(self, position):
        # rectangle in x1 y1 x2 y2
        self.tiles[position] = self.canvas.create_rectangle(position[0] * CELL_SIZE,
                                                            position[1] * CELL_SIZE,
                                                            (position[0] + 1) * CELL_SIZE,
                                                            (position[1] + 1) * CELL_SIZE, fill="white")

    def turn_white(self, position):
        self.canvas.itemconfigure(self.tiles[position], fill="white")

    def turn_black(self, position):
        self.canvas.itemconfigure(self.tiles[position], fill="black")


class Life(object):
    """Main game loop."""

    cells = dict()

    def __init__(self, parent):
        """Initial game conditions"""
        self.parent = parent
        self.board = Board(parent)
        for x in range(0, WIDTH / CELL_SIZE):
            for y in range(0, HEIGHT / CELL_SIZE):
                self.cells[(x, y)] = False
                self.board.draw_cell((x, y))
                if randint(1, 100) >= 100 - CELL_DENSITY:
                    self.cells[(x, y)] = True
                    self.board.turn_black((x, y))

        self.animate()

    def animate(self):
        if self.board.automaton.get() == "life":
            self.game_of_life()
        elif self.board.automaton.get() == "seeds":
            self.seeds()
        self.parent.after(DELAY, self.animate)

    def game_of_life(self):
        new_cells = copy.deepcopy(self.cells)
        for x in range(0, WIDTH / CELL_SIZE):
            for y in range(0, HEIGHT / CELL_SIZE):
                neighbours = self.count_neighbours(x, y)

                if self.cells[(x, y)]:
                    # under-population
                    if neighbours < 2:
                        new_cells[(x, y)] = False
                        self.board.turn_white((x, y))
                    # survival
                    elif neighbours == 2 or neighbours == 3:
                        pass
                    # overcrowding
                    else:
                        new_cells[(x, y)] = False
                        self.board.turn_white((x, y))
                else:
                    # reproduction
                    if neighbours == 3:
                        new_cells[(x, y)] = True
                        self.board.turn_black((x, y))

        self.cells = new_cells

    def seeds(self):
        new_cells = copy.deepcopy(self.cells)
        for x in range(0, WIDTH / CELL_SIZE):
            for y in range(0, HEIGHT / CELL_SIZE):
                neighbours = self.count_neighbours(x, y)

                if not self.cells[(x, y)] and neighbours == 2:
                    new_cells[(x, y)] = True
                    self.board.turn_black((x, y))
                else:
                    new_cells[(x, y)] = False
                    self.board.turn_white((x, y))

        self.cells = new_cells

    def count_neighbours(self, x, y):
        neighbours = 0
        # north
        if y != 0:
            if self.cells[(x, y - 1)]:
                neighbours += 1
            # north-east
        if x < WIDTH / CELL_SIZE - 1 and y != 0:
            if self.cells[(x + 1, y - 1)]:
                neighbours += 1
            # north-west
        if x != 0 and y != 0:
            if self.cells[(x - 1, y - 1)]:
                neighbours += 1
            # south
        if y < HEIGHT / CELL_SIZE - 1:
            if self.cells[(x, y + 1)]:
                neighbours += 1
            # south-east
        if x < WIDTH / CELL_SIZE - 1 and y < HEIGHT / CELL_SIZE - 1:
            if self.cells[(x + 1, y + 1)]:
                neighbours += 1
            # south-west
        if x != 0 and y < HEIGHT / CELL_SIZE - 1:
            if self.cells[(x - 1, y + 1)]:
                neighbours += 1
            # east
        if x < WIDTH / CELL_SIZE - 1:
            if self.cells[(x + 1, y)]:
                neighbours += 1
            # west
        if x != 0:
            if self.cells[(x - 1, y)]:
                neighbours += 1

        return neighbours

if __name__ == "__main__":
    root = Tk()
    root.title("Life")
    life = Life(root)

    root.mainloop()
