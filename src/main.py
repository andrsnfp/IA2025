from environment import *
from agent import Agent

# Function to start the environment creation after collecting parameters
def start_environment():
    bomb_ratio_value = bomb_ratio_var.get()
    approach_value = approach_var.get()
    num_agents = num_agents_var.get()
    consume_all_treasure = consume_all_treasure_var.get()

    # Generate and display the environment
    environment = generate_environment(bomb_ratio_value, approach_value)
    agents = [Agent(f"A{i+1}",(0,0), consume_all_treasure) for i in range(num_agents)] #Initializing the Agent

    #Displaying the environment
    display_environment(environment, agents)

# Main GUI for parameter entry
root = tk.Tk()
root.title("Ambiente")

# Number of Agents Selection
tk.Label(root, text="Select the number of agents:", font=("Arial", 12)).pack(pady=10)
num_agents_var = tk.IntVar(value=1)  # Default value
tk.Scale(root, from_=1, to=10, orient=tk.HORIZONTAL, variable=num_agents_var).pack()

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

# Consume All Treasure Selection
tk.Label(root, text="An Agent will consume all treasure?", font=("Arial", 12)).pack(pady=10)
consume_all_treasure_var = tk.BooleanVar(value=True)  # Default is True
tk.Radiobutton(root, text="Yes", variable=consume_all_treasure_var, value=True).pack(anchor="w")
tk.Radiobutton(root, text="No", variable=consume_all_treasure_var, value=False).pack(anchor="w")

# Start Button
start_button = tk.Button(root, text="Create Environment", command=start_environment, bg="blue", fg="white")
start_button.pack(pady=20)

# Run the main GUI loop
root.mainloop()