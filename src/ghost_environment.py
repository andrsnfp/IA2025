def initialize_ghost_environment():
    # Initializes the ghost environment with unknown cells ('?').
    rows = 10
    cols = 10
    env = [['?' for _ in range(cols)] for _ in range(rows)]
    env[0][0] = 'L'
    return env

def update_ghost_environment(ghost_env, x, y, value):
    # Updates ghost environment at position (x,y) with the given value
    ghost_env[x][y] = value

def print_ghost_environment(ghost_env):
    # Prints the ghost environment in a readable format.
    for row in ghost_env:
        print(" ".join(row))
