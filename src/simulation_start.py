from environment import *
from agent import Agent
from ghost_environment import GhostEnvironment
from env import EnvironmentManager
import random

# Function to handle entry parameters
def setup_entry_parameters():
    root = tk.Tk()
    root.title("Ambiente")

    # Number of Agents Selection
    tk.Label(root, text="Select the number of agents:", font=("Arial", 12)).pack(pady=10)
    num_agents_var = tk.IntVar(value=1)  # Default value
    tk.Scale(root, from_=1, to=10, orient=tk.HORIZONTAL, variable=num_agents_var).pack()

    # Number of Treasures Selection
    tk.Label(root, text="Select the number of treasures:", font=("Arial", 12)).pack(pady=10)
    num_treasures_var = tk.IntVar(value=10)  # Default value
    tk.Scale(root, from_=8, to=14, orient=tk.HORIZONTAL, variable=num_treasures_var).pack()

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
    approach_var = tk.StringVar(value="A")  # Default value
    approach_options = {
        "Approach A": "A",
        "Approach B": "B",
        "Approach C": "C"
    }
    for label, value in approach_options.items():
        tk.Radiobutton(root, text=label, variable=approach_var, value=value).pack(anchor="w")

    # Consume All Treasure Selection
    tk.Label(root, text="An Agent will consume all treasure?", font=("Arial", 12)).pack(pady=10)
    consume_all_treasure_var = tk.BooleanVar(value=True)  # Default is True
    tk.Radiobutton(root, text="Yes", variable=consume_all_treasure_var, value=True).pack(anchor="w")
    tk.Radiobutton(root, text="No", variable=consume_all_treasure_var, value=False).pack(anchor="w")

    # Start Button
    def on_start_button():
        start_environment(
            num_agents_var.get(),
            num_treasures_var.get(),
            bomb_ratio_var.get(),
            approach_var.get(),
            consume_all_treasure_var.get()
        )
        root.destroy()

    tk.Button(root, text="Create Environment", command=on_start_button, bg="blue", fg="white").pack(pady=20)

    # Run the main GUI loop
    root.mainloop()

# Function to start the environment creation after collecting parameters
def start_environment(num_agents, num_treasures, bomb_ratio, approach, consume_all_treasure):
    # Generate the environment
    agent_positions = tuple((random.randint(0,9),random.randint(0,9)) for _ in range(num_agents))
    environment = generate_environment(agent_positions, num_treasures, bomb_ratio, approach)

    # Generate ghost_environment
    ghost_env = GhostEnvironment()
    ghost_env.initialize_ghost_environment(agent_positions)
    ghost_env.print_ghost_environment()

    # Initialize the agents
    agents = [Agent(f"A{i+1}", agent_positions[i],consume_all_treasure, ghost_env) for i in range(num_agents)]

    # Initialize treasure tracking
    found_treasures = [0]

    #Displaying the environment
    display_environment(environment, agents, approach,num_treasures, found_treasures)

