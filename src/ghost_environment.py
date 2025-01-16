def initialize_ghost_environment(agents):
    # Initializes the ghost environment with unknown cells ('?').
    rows = 10
    cols = 10
    ghost_env = [['?' for _ in range(cols)] for _ in range(rows)]
    for x,y in agents:
        ghost_env[x][y] = 'L'
    return ghost_env

def update_ghost_environment(ghost_env, x, y, value):
    # Updates ghost environment at position (x,y) with the given value
    ghost_env[x][y] = value

def print_ghost_environment(ghost_env):
    # Prints the ghost environment in a readable format.
    for row in ghost_env:
        print(" ".join(row))
