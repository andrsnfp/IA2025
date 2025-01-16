class GhostEnvironment:
    def __init__(self):
        # Initializes the ghost environment with unknown cells ('?').
        self.rows = 10
        self.cols = 10
        self.ghost_env = [['?' for _ in range(self.cols)] for _ in range(self.rows)]

    def initialize_ghost_environment(self, agents):
        # Initializes the ghost environment with agents placed as 'L'.
        for x, y in agents:
            self.ghost_env[x][y] = 'L'

    def update_ghost_environment(self, x, y, value):
        # Updates ghost environment at position (x, y) with the given value.
        self.ghost_env[x][y] = value

    def print_ghost_environment(self):
        # Prints the ghost environment in a readable format.
        for row in self.ghost_env:
            print(" ".join(row))