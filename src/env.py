import random
import tkinter as tk

class EnvironmentManager:
    def __init__(self, num_treasures, bombs_ratio, approach):
        self.rows = 10
        self.cols = 10
        self.num_treasures = num_treasures
        self.total_cells = (self.rows * self.cols) - self.num_treasures
        self.num_bombs = int(bombs_ratio * self.total_cells)
        self.num_free_cells = self.total_cells - self.num_bombs
        self.approach = approach
        self.environment = []

        self.found_treasures = 0

    def generate_environment(self, agents):
        # Create the cell list
        cells = (
            ['T'] * self.num_treasures +  # Treasure cells
            ['B'] * self.num_bombs +  # Bomb cells
            ['L'] * self.num_free_cells  # Free cells
        )

        # Shuffle cells for randomness
        random.shuffle(cells)

        if self.approach == 'C':
            # Add the flag to the environment
            flag = random.randint(0, self.total_cells)  # Ensure not placed at the first position
            cells[flag] = 'F'

        self.environment = [cells[i * self.cols:(i + 1) * self.cols] for i in range(self.rows)]
        for x, y in agents:
            self.environment[x][y] = 'L'

    def display_environment(self, agents, found_treasures):
        # Tkinter window for environment display
        env_window = tk.Tk()
        env_window.title("Ambiente com Agente")

        # Create a grid of labels to represent the environment
        labels = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        flag_found = [False]  # Track if the flag has been found

        def display_success():
            for widget in env_window.winfo_children():
                widget.destroy()
            success_label = tk.Label(env_window, text="SUCCESS", font=("Arial", 24), fg="green")
            success_label.pack(expand=True)

        def display_failure():
            for widget in env_window.winfo_children():
                widget.destroy()
            failure_label = tk.Label(env_window, text="FAILURE", font=("Arial", 24), fg="red")
            failure_label.pack(expand=True)

        def update_grid():
            for r in range(self.rows):
                for c in range(self.cols):
                    cell_value = self.environment[r][c]
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
                            color = "purple"
                            agent_here = agent.name

                    labels[r][c].config(bg=color, text=agent_here if agent_here else cell_value) #type: ignore

            # Check win/lose conditions
            if self.approach == 'A':
                if found_treasures[0] > (self.num_treasures // 2):
                    display_success()
                if all(not agent.alive for agent in agents) and found_treasures[0] <= (self.num_treasures // 2):
                    display_failure()

            elif self.approach == 'C':
                if flag_found[0]:
                    display_success()
                if all(not agent.alive for agent in agents) and not flag_found[0]:
                    display_failure()

        def move_agent(agent, direction):
            if not agent.alive:
                print(f"{agent.name} is destroyed in {agent.position} and cannot move.")
                return

            agent.move(direction, self.environment, found_treasures, flag_found)
            update_grid()

        for r in range(self.rows):
            for c in range(self.cols):
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

        controls_frame = tk.Frame(env_window)
        controls_frame.grid(row=self.rows, column=0, columnspan=self.cols, pady=5)

        for i, agent in enumerate(agents):
            row_frame = tk.Frame(controls_frame)
            row_frame.pack(fill="x", pady=5)

            tk.Label(row_frame, text=f"{agent.name}").pack(side="left", padx=5)

            tk.Button(row_frame, text="⬆", command=lambda a=agent: move_agent(a, "up")).pack(side="left")
            tk.Button(row_frame, text="⬅", command=lambda a=agent: move_agent(a, "left")).pack(side="left")
            tk.Button(row_frame, text="⬇", command=lambda a=agent: move_agent(a, "down")).pack(side="left")
            tk.Button(row_frame, text="➡", command=lambda a=agent: move_agent(a, "right")).pack(side="left")

        update_grid()
        env_window.mainloop()

    def found_a_treasure(self):
        self.found_treasures += 1