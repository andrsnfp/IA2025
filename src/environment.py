import random
import tkinter as tk
from agent import Agent

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
                if cell_value == 'L':
                    color = "white"
                elif cell_value == 'B':
                    color = "gray"
                elif cell_value == 'T':
                    color = "gold"
                elif cell_value == 'F':
                    color = "green"
                for agent in agents:
                    if (r, c) == agent.position:
                        color = "purple"

                # Update label colors and text
                labels[r][c].config(bg=color, text= cell_value)

    def move_agent(agent, direction):
        if not agent.alive:
            print(f"{agent.name} is destroyed in {agent.position} and cannot move.")
            return

        x, y = agent.position
        environment[x][y] = 'L'  # Clear the agent's previous position
        new_position = agent.move(direction, environment)

        if agent.alive:
            environment[new_position[0]][new_position[1]] = 'L'  # Mark new position
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

# Function to start the environment creation after collecting parameters
def start_environment():
    bomb_ratio_value = bomb_ratio_var.get()
    approach_value = approach_var.get()
    num_agents = num_agents_var.get()

    # Generate and display the environment
    environment = generate_environment(bomb_ratio_value, approach_value)
    agents = [Agent(f"Agent {i+1}",(0,0)) for i in range(num_agents)] #Initializing the Agent

    #Displaying the environment
    display_environment(environment, agents)

# Main GUI for parameter entry
root = tk.Tk()
root.title("Ambiente")

# Bomb Ratio Selection
tk.Label(root, text="Seleccionar a percentagem de bombas no ambiente:", font=("Arial", 12)).pack(pady=10)
bomb_ratio_var = tk.DoubleVar(value=0.5)  # Default value
bomb_options = {
    "50% Bombs": 0.5,
    "60% Bombs": 0.6,
    "70% Bombs": 0.7,
    "80% Bombs": 0.8
}
for label, value in bomb_options.items():
    tk.Radiobutton(root, text=label, variable=bomb_ratio_var, value=value).pack(anchor="w")

# Approach Selection
tk.Label(root, text="Select the approach for the environment:", font=("Arial", 12)).pack(pady=10)
approach_var = tk.StringVar(value="A") #default value
approach_options = {
    "Approach A": "A",
    "Approach B": "B",
    "Approach C": "C"
}
for label, value in approach_options.items():
    tk.Radiobutton(root, text=label, variable=approach_var, value=value).pack(anchor="w")

# Number of Agents Selection
tk.Label(root, text="Select the number of agents:", font=("Arial", 12)).pack(pady=10)
num_agents_var = tk.IntVar(value=1)  # Default value
tk.Scale(root, from_=1, to=10, orient=tk.HORIZONTAL, variable=num_agents_var).pack()

# Start Button
start_button = tk.Button(root, text="Create Environment", command=start_environment, bg="blue", fg="white")
start_button.pack(pady=20)

# Run the main GUI loop
root.mainloop()