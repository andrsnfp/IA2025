import random
import tkinter as tk

def generate_environment(agents, num_treasures, bombs_ratio, approach):
    # Calculate total cells
    rows = 10
    cols = 10
    total_cells = (rows * cols) - num_treasures

    # Calculate number of bombs, free cells, and treasures
    num_bombs = int(total_cells * bombs_ratio)
    num_free_cells = total_cells - num_bombs

    # Create the cell list
    cells = (
            ['T'] * num_treasures +  # Treasure cells
            ['B'] * num_bombs +  # Bomb cells
            ['L'] * num_free_cells  # Free cells
    )

    # Shuffle the cells for randomness
    random.shuffle(cells)

    if approach == 'C':
        #Add the flag to the environment
        flag = random.randint(1, total_cells - 1)  # Ensure not placed at the first position
        cells[flag] = 'F'

    environment = [cells[i * cols:(i + 1) * cols] for i in range(rows)]
    for x,y in agents:
        environment[x][y] = 'L'

    return environment

# Function to display the environment
def display_environment(environment, agents, approach, total_treasures, found_treasures):
    rows = len(environment)
    cols = len(environment[0])

    # Tkinter window for environment display
    env_window = tk.Tk()
    env_window.title("Ambiente com Agente")

    # Create a grid of labels to represent the environment
    labels = [[None for _ in range(cols)] for _ in range(rows)]

    # Track if the flag has been found
    flag_found = [False]  # Use a mutable list to track flag status

    def display_success():
        # Destroy all existing widgets
        for widget in env_window.winfo_children():
            widget.destroy()

        # Add a success message
        success_label = tk.Label(env_window, text="SUCCESS", font=("Arial", 24), fg="green")
        success_label.pack(expand=True)

    def display_failure():
        for widget in env_window.winfo_children():
            widget.destroy()
        failure_label = tk.Label(env_window, text="FAILURE", font=("Arial", 24), fg="red")
        failure_label.pack(expand=True)

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

            # IF APPROACH A
            if approach == 'A':
                # SUCCESS
                if found_treasures[0] > (total_treasures // 2):
                    display_success()
                # FAILURE
                if all(not agent.alive for agent in agents) and found_treasures[0] <= (total_treasures // 2):
                    display_failure()

            #IF APPROACH C
            elif approach == 'C':
                # SUCCESS
                if flag_found[0]:
                    display_success()
                # FAILURE
                if all(not agent.alive for agent in agents) and not flag_found[0]:
                    display_failure()


    def move_agent(agent, direction):
        if not agent.alive:
            print(f"{agent.name} is destroyed in {agent.position} and cannot move.")
            return

        agent.move(direction, environment, found_treasures, flag_found)
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
    controls_frame.grid(row=rows, column=0, columnspan=cols, pady=5)

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
