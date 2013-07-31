from Tkinter import *
from random import randint
import copy

# Width of the canvas, in pixels.
WIDTH = 401
# Height of the canvas, in pixels.
HEIGHT = 401
# Size of each cells in pixels. Includes border (1px).
CELL_SIZE = 3
# Delay between 'ticks', in milliseconds.
DELAY = 10
# Starting density of live cells, in %.
CELL_DENSITY = 7


class Board(Frame):
    """
    Manages board graphics and interface.
    """

    # List of lists of every square that represents a cell.
    cells = list()

    def __init__(self, parent):
        """
         Initializes interface elements.
        """
        Frame.__init__(self, parent)

        # Canvas
        self.canvas = Canvas(parent, width=WIDTH, height=HEIGHT, bd=-2)
        self.canvas.grid(row=0, column=0, pady=(0, 12))

        self.automaton = StringVar()
        self.automaton.set("life")  # Default.
        # Conway's game of life button.
        self.life = Radiobutton(parent, text="Conway's game of life", variable=self.automaton, value="life",
                                indicatoron=0)
        self.life.grid(row=1, column=0, sticky=W + E)
        # Seeds button.
        self.seeds = Radiobutton(parent, text="Seeds", variable=self.automaton, value="seeds", indicatoron=0)
        self.seeds.grid(row=2, column=0, sticky=W + E)

    def init_cells(self):
        """
        Creates enough cells to fill the board.
        Returns initial state of the board.
        """
        state = list()
        for x in range(0, WIDTH / CELL_SIZE):
            column = list()
            column_state = list()
            for y in range(0, HEIGHT / CELL_SIZE):
                if randint(1, 100) >= 100 - CELL_DENSITY:
                    # Live cell.
                    status = NORMAL
                    column_state.append(1)
                else:
                    # Dead cell.
                    status = HIDDEN
                    column_state.append(0)
                column.append(self.canvas.create_rectangle(x * CELL_SIZE, y * CELL_SIZE, (x + 1) * CELL_SIZE,
                                                           (y + 1) * CELL_SIZE, fill="black", state=status,
                                                           outline="white"))

            self.cells.append(column)
            state.append(column_state)

        return state

    def update_cells(self, state):
        """
        Updates board to reflect a given state.
        """
        for x in range(0, WIDTH / CELL_SIZE):
            for y in range(0, HEIGHT / CELL_SIZE):
                if state[x][y] != self.get_state(x, y):
                    self.toggle_color(x, y)

    def get_state(self, x, y):
        """
        Returns the state of a given cell, True means alive, False means dead.
        """
        return self.canvas.itemcget(self.cells[x][y], "state") == NORMAL

    def toggle_color(self, x, y):
        """
        Toggles the color of a cell, hiding or revealing it.
        Doesn't actually changes the fill attribute.
        """
        if self.get_state(x, y):
            self.canvas.itemconfigure(self.cells[x][y], state=HIDDEN)
        else:
            self.canvas.itemconfigure(self.cells[x][y], state=NORMAL)


class Life(object):
    """
    Manages game logic.
    """

    # List of lists representing the state of every cell.
    state = list()

    def __init__(self, parent):
        """
        Creates the board and starts animating.
        """
        self.parent = parent
        self.board = Board(parent)
        self.state = self.board.init_cells()
        self.animate()

    def animate(self):
        """
        Animates the board, using the current set of rules.
        """
        if self.board.automaton.get() == "life":
            self.game_of_life()
        elif self.board.automaton.get() == "seeds":
            self.seeds()

        self.board.update_cells(self.state)
        self.parent.after(DELAY, self.animate)

    def game_of_life(self):
        """
        Rules for Conway's game of life.
        """
        new_state = copy.deepcopy(self.state)
        for x in range(0, WIDTH / CELL_SIZE):
            for y in range(0, HEIGHT / CELL_SIZE):
                neighbours = self.count_neighbours(x, y)

                if self.state[x][y]:
                    # Any live cell with fewer than two live neighbours dies, as if caused by under-population.
                    if neighbours < 2:
                        new_state[x][y] = not self.state[x][y]
                    # Any live cell with two or three live neighbours lives on to the next generation.
                    elif neighbours == 2 or neighbours == 3:
                        pass
                    # Any live cell with more than three live neighbours dies, as if by overcrowding.
                    else:
                        new_state[x][y] = not self.state[x][y]
                else:
                    # Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
                    if neighbours == 3:
                        new_state[x][y] = not self.state[x][y]

        self.state = new_state

    def seeds(self):
        """
        Rules for Seeds.
        """
        new_state = copy.deepcopy(self.state)
        for x in range(0, WIDTH / CELL_SIZE):
            for y in range(0, HEIGHT / CELL_SIZE):
                neighbours = self.count_neighbours(x, y)

                if not self.state[x][y] and neighbours == 2:
                    # A dead cell is born if it had exactly two live neighbors.
                    new_state[x][y] = not self.state[x][y]
                else:
                    # Every other cell dies.
                    new_state[x][y] = 0

        self.state = new_state

    def count_neighbours(self, x, y):
        """
        Counts alive cells in the Moore neighborhood of a cell.
        Returns the result.
        """
        canvas = self.board.canvas
        neighbours = 0
        # North.
        if y != 0:
            if self.state[x][y - 1]:
                neighbours += 1
        # North-east.
        if x < WIDTH / CELL_SIZE - 1 and y != 0:
            if self.state[x + 1][y - 1]:
                neighbours += 1
        # North-west.
        if x != 0 and y != 0:
            if self.state[x - 1][y - 1]:
                neighbours += 1
        # South.
        if y < HEIGHT / CELL_SIZE - 1:
            if self.state[x][y + 1]:
                neighbours += 1
        # South-east.
        if x < WIDTH / CELL_SIZE - 1 and y < HEIGHT / CELL_SIZE - 1:
            if self.state[x + 1][y + 1]:
                neighbours += 1
        # South-west.
        if x != 0 and y < HEIGHT / CELL_SIZE - 1:
            if self.state[x - 1][y + 1]:
                neighbours += 1
        # East.
        if x < WIDTH / CELL_SIZE - 1:
            if self.state[x + 1][y]:
                neighbours += 1
        # West.
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
