from Tkinter import *
from random import randint

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
        else:
            pass

        self.board.update_cells(self.state)
        self.parent.after(DELAY, self.animate)

    def game_of_life(self):
        """
        Rules for Conway's game of life.
        """
        new_state = self.state[:]
        width = WIDTH / CELL_SIZE
        height = HEIGHT / CELL_SIZE

        for index in range(0, width * height):
            neighbours = self.count_neighbours(index)

            if self.state[index]:
                # Any live cell with fewer than two live neighbours dies, as if caused by under-population.
                if neighbours < 2:
                    new_state[index] = not self.state[index]
                # Any live cell with two or three live neighbours lives on to the next generation.
                elif neighbours == 2 or neighbours == 3:
                    pass
                # Any live cell with more than three live neighbours dies, as if by overcrowding.
                else:
                    new_state[index] = not self.state[index]
            else:
                # Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
                if neighbours == 3:
                    new_state[index] = not self.state[index]

        self.state = new_state

    def seeds(self):
        """
        Rules for Seeds.
        """
        new_state = self.state[:]
        width = WIDTH / CELL_SIZE
        height = HEIGHT / CELL_SIZE

        for index in range(0, width * height):
            neighbours = self.count_neighbours(index)

            if not self.state[index] and neighbours == 2:
                # A dead cell is born if it had exactly two live neighbors.
                new_state[index] = not self.state[index]
            else:
                # Every other cell dies.
                new_state[index] = 0

        self.state = new_state

    def count_neighbours(self, index):
        """
        Counts alive cells in the Moore neighborhood of a cell.
        Returns the result.
        """
        canvas = self.board.canvas
        width = WIDTH / CELL_SIZE
        height = HEIGHT / CELL_SIZE
        neighbours = 0

        x, y = (index / width), (index % width)  # Temporary crutch.

        # North.
        if index - width >= 0:
            if self.state[index - width]:
                neighbours += 1
        # North-east.
        if index - width + 1 >= 0:
            if self.state[index - width + 1]:
                neighbours += 1
        # North-west.
        if index - width - 1 >= 0:
            if self.state[index - width - 1]:
                neighbours += 1
        # South.
        if index + width < height * width:
            if self.state[index + width]:
                neighbours += 1
        # South-east.
        if index + width + 1 < height * width:
            if self.state[index + width + 1]:
                neighbours += 1
        # South-west.
        if index + width - 1 < height * width:
            if self.state[index + width - 1]:
                neighbours += 1
        # East.
        if index + 1 < height * width:
            if self.state[index + 1]:
                neighbours += 1
        # West.
        if index - 1 >= 0:
            if self.state[index - 1]:
                neighbours += 1

        return neighbours

if __name__ == "__main__":
    root = Tk()
    root.title("Life")
    root.resizable(width=FALSE, height=FALSE)
    life = Life(root)

    root.mainloop()
