import random
import tkinter as tk
from ghost_environment import *

def generate_environment(bombs_ratio, approach):
    # Calculate total cells
    rows = 10
    cols = 10
    total_cells = rows * cols

    # Calculate number of bombs, free cells, and treasures
    num_bombs = int(total_cells * bombs_ratio)
    num_free_cells = total_cells - num_bombs
    num_treasures = int(num_free_cells * 0.40)

    # Adjust free cells to account for treasures
    num_free_cells -= num_treasures

    # Create the cell list
    cells = (
            ['B'] * num_bombs +  # Bomb cells
            ['T'] * num_treasures +  # Treasure cells
            ['L'] * num_free_cells  # Free cells
    )

    # Shuffle the cells for randomness
    random.shuffle(cells)
    cells[0] = 'L' #ensures the first cell is always free

    if approach == 'C':
        #Add the flag to the environment
        flag_position = random.randint(1, total_cells - 1)  # Ensure not placed at the first position
        cells[flag_position] = 'F'

    environment = [cells[i * cols:(i + 1) * cols] for i in range(rows)]

    return environment

# Function to display the environment
def display_environment(environment, agents):
    rows = len(environment)
    cols = len(environment[0])

    # Tkinter window for environment display
    env_window = tk.Tk()
    env_window.title("Ambiente com Agente")

    # Create a grid of labels to represent the environment
    labels = [[None for _ in range(cols)] for _ in range(rows)]

    def update_grid():
        for r in range(rows):
            for c in range(cols):
                cell_value = environment[r][c]
                color = "white"

                # Determine the cell's color based on its value
                if cell_value == 'L':
                    color = "white"
                elif cell_value == 'B':
                    color = "gray"
                elif cell_value == 'T':
                    color = "gold"
                elif cell_value == 'F':
                    color = "green"

                # Check if an agent is in this position
                agent_here = None
                for agent in agents:
                    if agent.alive and (r, c) == agent.position:
                        color = "purple"  # Keep the purple color for agents
                        agent_here = agent.name  # Use agent's unique name (e.g., A1, A2)

                # Update label colors and text
                labels[r][c].config(bg=color, text=agent_here if agent_here else cell_value) #type: ignore

    def move_agent(agent, direction):
        if not agent.alive:
            print(f"{agent.name} is destroyed in {agent.position} and cannot move.")
            return

        agent.move(direction, environment)
        update_grid()

    # Create the labels
    for r in range(rows):
        for c in range(cols):
            label = tk.Label(
                env_window,
                text="",
                width=6,
                height=3,
                bg="white",
                relief="solid",
                borderwidth=2
            )
            label.grid(row=r, column=c)
            labels[r][c] = label #type: ignore

    # Create controls for each agent
    controls_frame = tk.Frame(env_window)
    controls_frame.grid(row=rows, column=0, columnspan=cols, pady=10)

    for i, agent in enumerate(agents):
        #Create a row for each agent's controls
        row_frame = tk.Frame(controls_frame)
        row_frame.pack(fill="x", pady=5)

        #Add agent name Label
        tk.Label(row_frame, text=f"{agent.name}").pack(side="left", padx=5)

        #Add movement buttons
        tk.Button(row_frame, text="⬆", command=lambda a=agent: move_agent(a, "up")).pack(side="left")
        tk.Button(row_frame, text="⬅", command=lambda a=agent: move_agent(a,"left")).pack(side="left")
        tk.Button(row_frame, text="⬇", command=lambda a=agent: move_agent(a,"down")).pack(side="left")
        tk.Button(row_frame, text="➡", command=lambda a=agent: move_agent(a,"right")).pack(side="left")

    # Initial display
    update_grid()
    env_window.mainloop()