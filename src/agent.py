class Agent:
    def __init__(self, name, start_position):
        self.name = name
        self.position = start_position
        self.alive = True #T racks if the agent is alive
        self.empowered = False # Tracks if the agent has empowerment

    def move(self, direction, environment):
        if not self.alive:
            print(f"{self.name} is destroyed and cannot move.")
            return self.position

        rows, cols = len(environment), len(environment[0])
        x, y = self.position

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

        self.interact(environment, x, y)
        self.position = (x, y)
        return self.position

    def interact(self, environment, x, y):
        cell = environment[x][y]

        if cell == 'L':
            print(f"{self.name} moved to a free cell.")
        elif cell == 'B':
            if self.empowered:
                print(f"{self.name} deactivated a bomb using empowerment!")
                self.empowered = False # Empowerment is consumed
                #environment[x][y] = 'L' #Change the bomb cell to a free cell
            else:
                print(f"{self.name} hit a bomb and is destroyed!")
                self.alive = False
        elif cell == 'T':
            print(f"{self.name} found a treasure! Boost acquired.")
            self.empowered = True # Agent becomes empowered
        elif cell == 'F':
            print(f"{self.name} reached the flag! Success!")