import random

class Agent:
    def __init__(self, name, position, consume_all_treasure, ghost_env, ai_model, encoder):
        self.name = name
        self.position = position
        self.previous_positions = [] # Tracks previous positions to prevent loops
        self.alive = True # Tracks if the agent is alive
        self.empowered = 0 # Tracks the amount of empowerment the agent has
        self.consume_all_treasure = consume_all_treasure
        self.consumed_treasures = set() # Tracks treasure cells already used to avoid exploits
        self.ghost_env = ghost_env
        self.ai_model = ai_model
        self.encoder = encoder

    def get_neighboring_cells(self):
        x, y = self.position

        up = self.ghost_env.get_cell_value(x - 1, y) if (x - 1 >= 0) else '-'
        down = self.ghost_env.get_cell_value(x + 1, y) if (x + 1 < 9) else '-'
        left = self.ghost_env.get_cell_value(x, y - 1) if (y - 1 >= 0) else '-'
        right = self.ghost_env.get_cell_value(x, y + 1) if (y + 1 < 9) else '-'

        neighbors = [left, right, up, down]
        print(neighbors)
        return neighbors

    def is_within_bounds(self, position, grid):
        x, y = position
        return 0 <= x < len(grid) and 0 <= y < len(grid[0])

    def predict(self, data):
        data_to_encode = self.encoder.transform(data)
        return self.ai_model.predict(data_to_encode.reshape(1, -1))

    def ai_move(self):
        neighboring_cells = self.get_neighboring_cells()

        # Ensure neighboring_cells is a dictionary with correct feature names
        data = self.encoder.fit_transform(neighboring_cells)

        # Predict using the AI model
        move = self.ai_model.predict(data.reshape(1,-1))[0]
        return move

    def move(self, grid):
        if len(self.previous_positions) == 2:
            self.previous_positions.pop(0)
        self.previous_positions.append(self.position)

        x, y = self.position

        neighboring_cells = self.get_neighboring_cells()
        move = self.predict(neighboring_cells)[0]
        print(move)

        directions = {
            "up": (x - 1, y),
            "down": (x + 1, y),
            "left": (x, y - 1),
            "right": (x, y + 1)
        }

        new_position = directions.get(move, self.position)

        # Ensure new position is valid and not out of bounds
        if not self.is_within_bounds(new_position, grid):
            print(f"{self.name}: Move '{move}' is out of bounds. Skipping move.")
            return self.position

        if len(self.previous_positions) == 2:
            attempts = 0
            while new_position == self.previous_positions[0] and attempts < 5:
                possible_moves = [value for value in neighboring_cells if value != '-']

                if not possible_moves:
                    print(f"{self.name}: No valid moves left. Staying in place.")
                    return self.position  # Stay in place if no valid moves

                new_move = random.choice(possible_moves)
                new_position = directions.get(new_move, self.position)
                attempts += 1

        print(f"{self.name} moving to {new_position}")
        # Interact with the new cell
        x, y = new_position

        try:
            self.interact(grid, x, y)
        except Exception as e:
            print(f"failed to interact with {self.name}: {e}")
            return self.position #Prevents breaking the loop

        # Update position
        self.position = new_position
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