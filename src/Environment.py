import random
import tkinter as tk

def generate_environment(bombs_ratio):
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
    cells[0] = 'L'

    environment = [cells[i * cols:(i + 1) * cols] for i in range(rows)]

    return environment


# Function to display the environment
def display_environment(environment):
    rows = len(environment)
    cols = len(environment[0])

    # Create a new window for the environment display
    env_window = tk.Tk()
    env_window.title("Ambiente")

    # Create a grid of labels to represent the environment
    for r in range(rows):
        for c in range(cols):
            cell_value = environment[r][c]
            color = "white"  # Default color
            if cell_value == 'L':
                color = "white"
            elif cell_value == 'B':
                color = "gray"
            elif cell_value == 'T':
                color = "gold"

            # Create a label for each cell
            label = tk.Label(
                env_window,
                text=cell_value,
                width=6,
                height=3,
                bg=color,
                relief="solid",
                borderwidth=2
            )
            label.grid(row=r, column=c)

# Function to start the environment creation after collecting parameters
def start_environment():
    bomb_ratio_value = bomb_ratio_var.get()
    treasure_ratio = 0.2  # Fixed for simplicity
    free_cells_ratio = 1 - bomb_ratio_value  # Free cells are what's left after bombs

    # Generate and display the environment
    environment = generate_environment(bomb_ratio_value)
    display_environment(environment)

# Main GUI for parameter entry
root = tk.Tk()
root.title("AI Environment Configuration")

# Instruction Label
instruction_label = tk.Label(root, text="Seleccionar a percentagem de bombas no ambiente:", font=("Arial", 12))
instruction_label.pack(pady=10)

# Bomb Ratio Options
bomb_ratio_var = tk.DoubleVar(value=0.5)  # Default value
bomb_options = {
    "50% Bombs": 0.5,
    "60% Bombs": 0.6,
    "70% Bombs": 0.7,
    "80% Bombs": 0.8
}

for label, value in bomb_options.items():
    tk.Radiobutton(root, text=label, variable=bomb_ratio_var, value=value).pack(anchor="w")

# Start Button
start_button = tk.Button(root, text="Create Environment", command=start_environment, bg="blue", fg="white")
start_button.pack(pady=20)

# Run the main GUI loop
root.mainloop()

