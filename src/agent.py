class Agent:
    def __init__(self, name, position, consume_all_treasure, ghost_env, ai_model, training_data, action_labels, encoder):
        self.name = name
        self.position = position
        self.previous_positions = []
        self.alive = True # Tracks if the agent is alive
        self.empowered = 0 # Tracks the amount of empowerment the agent has
        self.consume_all_treasure = consume_all_treasure
        self.consumed_treasures = set() # Tracks treasure cells already used to avoid exploits
        self.ghost_env = ghost_env
        self.ai_model = ai_model
        self.encoder = encoder
        self.train(training_data, action_labels)

    def get_neighboring_cells(self):
        x, y = self.position

        up = self.ghost_env[x-1][y] if (x - 1 > 0) else '-'
        down = self.ghost_env[x + 1][y] if (x + 1 < len(self.ghost_env)) else '-'
        left = self.ghost_env[x][y - 1] if (y - 1 > 0) else '-'
        right = self.ghost_env[x][y + 1] if (y + 1 < len(self.ghost_env[0])) else '-'

        return [up, down, left, right]

    def ai_move(self):
        neighboring_cells = self.get_neighboring_cells()
        encoded_data = self.encoder.fit_transform(neighboring_cells
                                                  )
        move = self.ai_model.predict(encoded_data.reshape(1, -1))

        return move

    def train(self, training_data, action_labels):
        self.ai_model.fit(training_data, action_labels)
        print('Agent ', self.name, ' Trained')

    def move(self, direction, grid):
        if not self.alive:
            print(f"{self.name} is destroyed and cannot move.")
            return self.position

        rows, cols = len(grid), len(grid[0])
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
        self.interact(grid, x, y)

        # Update position
        self.position = (x, y)
        self.ghost_env.print_ghost_environment()

        return self.position

    def interact(self, grid, x, y):
        cell = grid[x][y]

        if cell.type == 'L':
            self.interact_with_l(cell, x, y)
        elif cell.type == 'B':
            self.interact_with_b(cell, x, y)
        elif cell.type == 'T':
            self.interact_with_t(cell, x, y)
        elif cell.type == 'F':
            self.interact_with_f(cell, x, y)

    def interact_with_l(self, cell, x, y):
        print(f"{self.name} moved to a free cell.")
        cell.discover()
        self.ghost_env.update_ghost_environment(x, y, 'L')

    def interact_with_b(self, cell, x, y):
        if self.empowered > 0:
            print(f"{self.name} deactivated a bomb using empowerment!")
            self.empowered -= 1  # Empowerment is consumed
            cell.destroy_bomb()  # Update real environment
            self.ghost_env.update_ghost_environment(x, y, 'L')
        else:
            print(f"{self.name} hit a bomb and is destroyed!")
            self.alive = False
            if self.consume_all_treasure:
                self.ghost_env.update_ghost_environment(x, y, 'B')

    def interact_with_t(self, cell, x, y):
        if (x, y) in self.consumed_treasures:
            print(f"{self.name} stepped on an already consumed treasure. No effect.")
        else:
            print(f"{self.name} found a treasure! Empowerment acquired.")
            self.empowered += 1  # Agent becomes empowered
            self.consumed_treasures.add((x, y))  # Mark this treasure as consumed
            cell.discover()

            cell.consume_treasure(self.consume_all_treasure)  # Treasure is consumed

            if self.consume_all_treasure:
                self.ghost_env.update_ghost_environment(x, y, 'L')
            else:
                self.ghost_env.update_ghost_environment(x, y, 'T')

    def interact_with_f(self, cell, x, y):
        print(f"{self.name} reached the flag! Success!")
        cell.found_the_flag()
        self.ghost_env.update_ghost_environment(x, y, 'F')