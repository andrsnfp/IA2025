class Agent:
    def __init__(self, name, position,consume_all_treasure, ghost_env):
        self.name = name
        self.position = position
        self.alive = True # Tracks if the agent is alive
        self.empowered = False # Tracks if the agent has empowerment
        self.consume_all_treasure = consume_all_treasure
        self.consumed_treasures = set() # Tracks treasure cells already used to avoid exploits
        self.ghost_env = ghost_env

    def move(self, direction, environment, found_treasures, flag_found):
        if not self.alive:
            print(f"{self.name} is destroyed and cannot move.")
            return self.position

        rows, cols = len(environment), len(environment[0])
        x, y = self.position

        # Determine new position based on direction
        if direction == "up" and x > 0:
            x -= 1
        elif direction == "down" and x < rows - 1:
            x += 1
        elif direction == "left" and y > 0:
            y -= 1
        elif direction == "right" and y < cols - 1:
            y += 1
        else:
            print("Invalid move or out of bounds!")
            return self.position

        #interact with the cell at the new position
        self.interact(environment, self.ghost_env, x, y, found_treasures, flag_found)

        # Update position
        self.position = (x, y)

        # Print the ghost environment after updating it
        for row in self.ghost_env:
            print(" ".join(row))

        return self.position

    def interact(self, environment, ghost_env, x, y, found_treasures, flag_found):
        cell = environment[x][y]

        if cell == 'L':
            self.interact_with_l(ghost_env, x, y)
        elif cell == 'B':
            self.interact_with_b(environment, ghost_env, x, y)
        elif cell == 'T':
            self.interact_with_t(environment, ghost_env, x, y, found_treasures)
        elif cell == 'F':
            self.interact_with_f(ghost_env, x, y, flag_found)

    def interact_with_l(self, ghost_env, x, y):
        print(f"{self.name} moved to a free cell.")
        ghost_env[x][y] = 'L'

    def interact_with_b(self, environment, ghost_env, x, y):
        if self.empowered:
            print(f"{self.name} deactivated a bomb using empowerment!")
            self.empowered = False  # Empowerment is consumed
            environment[x][y] = 'L'  # Update real environment
            ghost_env[x][y] = 'L'  # Reflect the change in the ghost environment
        else:
            print(f"{self.name} hit a bomb and is destroyed!")
            self.alive = False
            if self.consume_all_treasure:
                ghost_env[x][y] = 'B'

    def interact_with_t(self, environment, ghost_env, x, y, found_treasures):
        if (x, y) in self.consumed_treasures:
            print(f"{self.name} stepped on an already consumed treasure. No effect.")
        else:
            print(f"{self.name} found a treasure! Empowerment acquired.")
            self.empowered = True  # Agent becomes empowered
            self.consumed_treasures.add((x, y))  # Mark this treasure as consumed

            if self.consume_all_treasure:
                environment[x][y] = 'L'  # Treasure is consumed
                ghost_env[x][y] = 'L'  # Reflect the change in the ghost environment
            else:
                ghost_env[x][y] = 'T'
            # Increment found treasures
            found_treasures[0] += 1

    def interact_with_f(self, ghost_env, x, y, flag_found):
        print(f"{self.name} reached the flag! Success!")
        ghost_env[x][y] = 'F'
        flag_found[0] = True  # Update flag status