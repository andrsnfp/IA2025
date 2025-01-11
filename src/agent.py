class Agent:
    def __init__(self, name, start_position, consume_all_treasure):
        self.name = name
        self.position = start_position
        self.alive = True # Tracks if the agent is alive
        self.empowered = False # Tracks if the agent has empowerment
        self.consume_all_treasure = consume_all_treasure
        self.consumed_treasures = set() # Tracks treasure cells already used to avoid exploits

    def move(self, direction, environment):
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
        cell = environment[x][y]

        if cell == 'L':
            print(f"{self.name} moved to a free cell.")
        elif cell == 'B':
            if self.empowered:
                print(f"{self.name} deactivated a bomb using empowerment!")
                self.empowered = False # Empowerment is consumed
                environment[x][y] = 'L'  # Bomb becomes a free cell
            else:
                print(f"{self.name} hit a bomb and is destroyed!")
                self.alive = False
                if self.consume_all_treasure:
                    environment[x][y] = 'L' #Bomb becomes free cell
        elif cell == 'T':
            if (x,y) in self.consumed_treasures:
                print(f"{self.name} stepped on this treasure already. No effect.")
            else:
                print(f"{self.name} found a treasure! Empowerment acquired.")
                self.empowered = True # Agent becomes empowered
                self.consumed_treasures.add((x,y)) # Marks this treasure as consumed
                if self.consume_all_treasure:
                    environment[x][y] = 'L' #Treasure is consumed
        elif cell == 'F':
            print(f"{self.name} reached the flag! Success!")

        # update position after interaction
        self.position = (x, y)
        return self.position
