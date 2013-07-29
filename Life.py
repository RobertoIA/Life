from Tkinter import *
from random import randint

WIDTH = 500
HEIGHT = 500
CELL_SIZE = 4
DELAY = 100
CELL_DENSITY = 5


class Board(Frame):
    """Grid area"""

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.canvas = Canvas(parent, width=WIDTH, height=HEIGHT, bd=-2)
        self.canvas.pack()

    def draw_background(self):
        self.canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill="white")

    def draw_grid(self):
        for x in range(0, WIDTH, CELL_SIZE):
            self.canvas.create_line(x, 0, x, HEIGHT)
        for y in range(0, HEIGHT, CELL_SIZE):
            self.canvas.create_line(0, y, WIDTH, y)

    def draw_cell(self, position):
        # rectangle in x1 y1 x2 y2
        self.canvas.create_rectangle(position[0] * CELL_SIZE, position[1] * CELL_SIZE, (position[0] + 1) * CELL_SIZE,
                                (position[1] + 1) * CELL_SIZE, fill="black")


class Life(object):
    """Main game loop."""

    test_cell = (12, 6)
    cells = dict()

    def __init__(self, parent):
        """Initial game conditions"""
        self.parent = parent
        self.board = Board(parent)
        for x in range(0, WIDTH / CELL_SIZE):
            for y in range(0, HEIGHT / CELL_SIZE):
                self.cells[(x, y)] = False
                if randint(1, 100) >= 100 - CELL_DENSITY:
                    self.cells[(x, y)] = True

        self.animate()

    def animate(self):
        self.board.draw_background()
        self.board.draw_grid()

        self.game_of_life()

        for x in range(0, WIDTH / CELL_SIZE):
            for y in range(0, HEIGHT / CELL_SIZE):
                if self.cells[(x, y)]:
                    self.board.draw_cell((x, y))

        self.parent.after(DELAY, self.animate)
        self.parent.update()

    def game_of_life(self):
        for x in range(0, WIDTH / CELL_SIZE):
            for y in range(0, HEIGHT / CELL_SIZE):
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

                if self.cells[(x, y)]:
                    # under-population
                    if neighbours < 2:
                        self.cells[(x, y)] = False
                    # survival
                    elif neighbours == 2 or neighbours == 3:
                        pass
                    # overcrowding
                    else:
                        self.cells[(x, y)] = False
                else:
                    # reproduction
                    if neighbours == 3:
                        self.cells[(x, y)] = True

        # TODO replace with game logic
        # if not (self.test_cell[0] + 1) * CELL_SIZE > WIDTH - CELL_SIZE:
        #     self.test_cell = (self.test_cell[0] + 1, self.test_cell[1])

if __name__ == "__main__":
    root = Tk()
    root.title("Life")
    life = Life(root)

    root.mainloop()
