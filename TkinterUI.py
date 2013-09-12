from Tkinter import *
from random import randint

from Life import *

# Width of the canvas, in pixels.
WIDTH = 300
# Height of the canvas, in pixels.
HEIGHT = 300
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
        self.canvas = Canvas(parent, width=WIDTH, height=HEIGHT, bd=-2, background="white")
        self.canvas.grid(row=0, column=0, pady=(0, 12))

        self.automaton = StringVar()
        self.automaton.set("pause")  # Default.
        # Conway's game of life button.
        self.life = Radiobutton(parent, text="Conway's game of life", variable=self.automaton, value="life",
                                indicatoron=0)
        self.life.grid(row=1, column=0, sticky=W + E)
        # Seeds button.
        self.seeds = Radiobutton(parent, text="Seeds", variable=self.automaton, value="seeds", indicatoron=0)
        self.seeds.grid(row=2, column=0, sticky=W + E)
        # Pause button
        self.seeds = Radiobutton(parent, text="Pause", variable=self.automaton, value="pause", indicatoron=0)
        self.seeds.grid(row=4, column=0, sticky=W + E, pady=(12, 0))

    def init_cells(self):
        """
        Creates enough cells to fill the board.
        Returns initial state of the board.
        """
        state = list()
        width = WIDTH / CELL_SIZE
        height = HEIGHT / CELL_SIZE

        for index in range(0, width * height):
            if randint(1, 100) >= 100 - CELL_DENSITY:
                # Live cell.
                status = NORMAL
                state.append(1)
            else:
                # Dead cell.
                status = HIDDEN
                state.append(0)

            cell = self.canvas.create_rectangle((index / width) * CELL_SIZE, (index % width) * CELL_SIZE,
                                                ((index / width) + 1) * CELL_SIZE, ((index % width) + 1) * CELL_SIZE,
                                                fill="black", state=status, outline="white")
            self.cells.append(cell)

        return state

    def update_cells(self, state):
        """
        Updates board to reflect a given state.
        """
        width = WIDTH / CELL_SIZE
        height = HEIGHT / CELL_SIZE

        for index in range(0, width * height):
            if state[index] != self.get_state(index):
                self.toggle_color(index)

    def get_state(self, index):
        """
        Returns the state of a given cell, True means alive, False means dead.
        """
        return self.canvas.itemcget(self.cells[index], "state") == NORMAL

    def toggle_color(self, index):
        """
        Toggles the color of a cell, hiding or revealing it.
        Doesn't actually changes the fill attribute.
        """
        if self.get_state(index):
            self.canvas.itemconfigure(self.cells[index], state=HIDDEN)
        else:
            self.canvas.itemconfigure(self.cells[index], state=NORMAL)


class Top(object):
    def __init__(self, parent, life):
        """
        Creates the board and starts animating.
        """
        self.parent = parent
        self.life = life
        self.board = Board(parent)
        self.state = self.board.init_cells()
        self.animate()

    def animate(self):
        """
        Animates the board, using the current set of rules.
        """
        if self.board.automaton.get() == "life":
            self.state = self.life.game_of_life(self.state)
        elif self.board.automaton.get() == "seeds":
            self.state = self.life.seeds(self.state)
        else:
            pass

        self.board.update_cells(self.state)
        self.parent.after(DELAY, self.animate)


if __name__ == "__main__":
    root = Tk()
    root.title("Life")
    root.resizable(width=FALSE, height=FALSE)
    top = Top(root, Life(WIDTH / CELL_SIZE, HEIGHT / CELL_SIZE))

    root.mainloop()