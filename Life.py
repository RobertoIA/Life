class Life(object):
    """
    Manages game logic.
    """

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def game_of_life(self, state):
        """
        Rules for Conway's game of life.
        """
        new_state = state[:]

        for index in range(0, self.width * self.height):
            neighbours = self.count_neighbours(state, index)

            if state[index]:
                # Any live cell with fewer than two live neighbours dies, as if caused by under-population.
                if neighbours < 2:
                    new_state[index] = not state[index]
                # Any live cell with two or three live neighbours lives on to the next generation.
                elif neighbours == 2 or neighbours == 3:
                    pass
                # Any live cell with more than three live neighbours dies, as if by overcrowding.
                else:
                    new_state[index] = not state[index]
            else:
                # Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
                if neighbours == 3:
                    new_state[index] = not state[index]

        return new_state

    def seeds(self, state):
        """
        Rules for Seeds.
        """
        new_state = state[:]

        for index in range(0, self.width * self.height):
            neighbours = self.count_neighbours(state, index)

            if not state[index] and neighbours == 2:
                # A dead cell is born if it had exactly two live neighbors.
                new_state[index] = not state[index]
            else:
                # Every other cell dies.
                new_state[index] = 0

        return new_state

    def count_neighbours(self, state, index):
        """
        Counts alive cells in the Moore neighborhood of a cell.
        Returns the result.
        """
        neighbours = 0

        for i in range(-1, 2):
            for j in range(-1, 2):
                neighbour_index = index + (i * self.width) + j
                if not (i == 0 and j == 0) and neighbour_index >= 0 and neighbour_index < len(state):
                    neighbours += state[index + (i * self.width) + j]

        return neighbours