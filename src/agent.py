import random

class Agent:
    def __init__(self, name, position, consume_all_treasure, ghost_env, ai_model, encoder):
        """
                Inicializa um agente no ambiente.
                :param name: Nome do agente.
                :param position: Posição inicial do agente (linha, coluna).
                :param consume_all_treasure: Define se o agente consome todos os tesouros.
                :param ghost_env: Referência ao ambiente fantasma.
                :param ai_model: Modelo de IA usado pelo agente.
                :param encoder: Codificador utilizado para os dados.
                """
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
        """
        Retorna os valores das células vizinhas do agente.
        """
        x, y = self.position

        up = self.ghost_env.get_cell_value(x - 1, y) if (x - 1 >= 0) else '-'
        down = self.ghost_env.get_cell_value(x + 1, y) if (x + 1 < 9) else '-'
        left = self.ghost_env.get_cell_value(x, y - 1) if (y - 1 >= 0) else '-'
        right = self.ghost_env.get_cell_value(x, y + 1) if (y + 1 < 9) else '-'

        neighbors = [left, right, up, down]
        print(neighbors)
        return neighbors

    def is_within_bounds(self, position):
        """
        Move o agente manualmente na direção escolhida.
        """
        x, y = position
        return 0 <= x < 10 and 0 <= y < 10

    def predict(self, data):
        """
        Faz uma previsão do próximo movimento com base no modelo de IA.
        """
        data_to_encode = self.encoder.transform(data)
        return self.ai_model.predict(data_to_encode.reshape(1, -1))

    def ai_move(self):
        """
        Move o agente usando a previsão do modelo de IA.
        """
        neighboring_cells = self.get_neighboring_cells()

        # Ensure neighboring_cells is a dictionary with correct feature names
        data = self.encoder.fit_transform(neighboring_cells)

        # Predict using the AI model
        move = self.ai_model.predict(data.reshape(1,-1))[0]
        return move

    def get_valid_moves(self):
        """Retorna os movimentos válidos que o agente pode fazer, evitando bordas e backtracking."""
        x, y = self.position

        possible_moves = {
            "up": (x - 1, y),
            "down": (x + 1, y),
            "left": (x, y - 1),
            "right": (x, y + 1)
        }

        valid_moves = {}

        for direction, (new_x, new_y) in possible_moves.items():
            # Check if move is within bounds
            if 0 <= new_x < 10 and 0 <= new_y < 10:
                if len(self.previous_positions) < 2 or (new_x, new_y) != self.previous_positions[-1]:
                    valid_moves[direction] = (new_x, new_y)  # Prevents back-and-forth movement

        return valid_moves

    def move(self, grid):
        """Movimenta o agente com base na IA, garantindo que a posição seja atualizada corretamente."""

        if not self.alive:
            print(f"{self.name} está destruído e não pode se mover.")
            return self.position  # Prevent movement if the agent is dead

        valid_moves = self.get_valid_moves()  # Get valid moves
        if not valid_moves:
            print(f"{self.name} não tem movimentos válidos e permanecerá na posição.")
            return self.position  # No valid moves, stay in place

        # Prepare AI input: Encode neighboring cells
        neighboring_cells = self.get_neighboring_cells()
        encoded_data = self.encoder.transform(neighboring_cells).reshape(1, -1)

        # Predict the move using AI
        predicted_direction = self.ai_model.predict(encoded_data)[0]
        print(f"Predicted move: {predicted_direction}")

        # Ensure the predicted move is valid
        if predicted_direction not in valid_moves:
            print(f"{self.name} tentou um movimento inválido '{predicted_direction}', escolhendo outro aleatoriamente.")
            predicted_direction = random.choice(list(valid_moves.keys()))  # Choose a valid move randomly

        new_position = valid_moves[predicted_direction]

        # Interaction with the grid
        x, y = new_position
        self.interact(grid, x, y)  # Handle interaction with new cell

        # Update agent position
        self.previous_positions.append(self.position)  # Store the last position
        if len(self.previous_positions) > 2:  # Keep history manageable
            self.previous_positions.pop(0)

        self.position = new_position  # Move agent to new position
        self.ghost_env.print_ghost_environment()  # Update ghost environment

        print(f"{self.name} moveu-se para {self.position}")
        return self.position

    # def move(self, grid):
    #     # if manual_move:
    #     #     return self.manual_move(manual_move,grid)
    #
    #     if len(self.previous_positions) == 2:
    #         self.previous_positions.pop(0)
    #     self.previous_positions.append(self.position)
    #
    #     x, y = self.position
    #
    #     neighboring_cells = self.get_neighboring_cells()
    #     move = self.predict(neighboring_cells)[0]
    #
    #     print(f"{self.name} - Current Position: {self.position}")
    #     print(f"{self.name} - Neighboring Cells: {neighboring_cells}")
    #     print(move)
    #
    #     directions = {
    #         "up": (x - 1, y),
    #         "down": (x + 1, y),
    #         "left": (x, y - 1),
    #         "right": (x, y + 1)
    #     }
    #
    #     new_position = directions.get(move, self.position)
    #
    #     if new_position == self.position:
    #         print(f"{self.name} - WARNING: Selected move does not change position!")
    #
    #     # Ensure new position is valid and not out of bounds
    #     if not self.is_within_bounds(new_position):
    #         print(f"{self.name}: Move '{move}' is out of bounds. Skipping move.")
    #         return self.position
    #
    #     if len(self.previous_positions) == 2:
    #         attempts = 0
    #         while new_position == self.previous_positions[0] and attempts < 5:
    #             possible_moves = [value for value in neighboring_cells if value != '-']
    #
    #             if not possible_moves:
    #                 print(f"{self.name}: No valid moves left. Staying in place.")
    #                 return self.position  # Stay in place if no valid moves
    #
    #             new_move = random.choice(possible_moves)
    #             new_position = directions.get(new_move, self.position)
    #             attempts += 1
    #
    #     print(f"{self.name} moving to {new_position}")
    #
    #     # Interact with the new cell
    #     x, y = new_position
    #
    #     try:
    #         self.interact(grid, x, y)
    #     except Exception as e:
    #         print(f"failed to interact with {self.name}: {e}")
    #         return self.position #Prevents breaking the loop
    #
    #     # Update position
    #     self.position = new_position
    #     self.ghost_env.print_ghost_environment()
    #     return self.position

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

    def manual_move(self, direction, grid):
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

        # interact with the cell at the new position
        self.interact(grid, x, y)

        # Update position
        self.position = (x, y)
        self.ghost_env.print_ghost_environment()

        return self.position