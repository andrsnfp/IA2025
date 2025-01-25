import random
import tkinter as tk
from cell import Cell

class EnvironmentManager:
    def __init__(self, agents_positions, num_treasures, bombs_ratio, approach):
        self.rows = 10
        self.cols = 10
        self.num_treasures = num_treasures
        self.total_cells = (self.rows * self.cols) - self.num_treasures
        self.num_bombs = int(bombs_ratio * self.total_cells)
        self.num_free_cells = self.total_cells - self.num_bombs
        self.cells_to_discover = self.num_free_cells + self.num_treasures
        self.approach = approach
        self.agents_positions = agents_positions # Position of all agents
        self.grid = self.generate_grid()

    def receive_agents(self,agents, model):
        self.agents = agents # The Agents running in the environment
        self.model = model

    def generate_grid(self):
        # Create a list of cell types
        cells = (
                ['T'] * self.num_treasures +
                ['B'] * self.num_bombs +
                ['L'] * self.num_free_cells
        )

        # Shuffle the cells
        random.shuffle(cells)

        if self.approach == 'C':
            # Place the flag
            flag_index = random.randint(0, self.total_cells)
            cells[flag_index] = 'F'

        # Create the grid
        grid = [
            [Cell(cells[r * self.cols + c], (r, c)) for c in range(self.cols)]
            for r in range(self.rows)
        ]

        # Mark agents' starting positions
        for x, y in self.agents_positions:
            grid[x][y] = Cell('L', (x, y)) # Create the agent's starting cell
            grid[x][y].discover() # Mark the cell as discovered

        return grid

    # Helper functions for verification of success
    def count_consumed_treasures(self):
        return sum(1 for row in self.grid for cell in row if (cell.type == 'T' or 'L') and cell.is_consumed)

    def count_discovered_cells(self):
        return sum(1 for row in self.grid for cell in row if cell.is_discovered)

    def is_flag_found(self):
        return any (cell.type == 'F' and cell.is_flag_found for row in self.grid for cell in row)

    def verify_success(self, agents):
        if self.approach == 'A' and self.count_consumed_treasures() > self.num_treasures // 2:
            # Count discovered and consumed treasures
            return 0

        elif self.approach == 'B':
            # Success if all L and T cells are discovered
            total_discoverable_cells = self.num_free_cells + self.num_treasures
            if self.count_discovered_cells() == total_discoverable_cells:
                return 0  # Success

        elif self.approach == 'C' and self.is_flag_found():
            return 0

        if all(not agent.alive for agent in agents):
            return 1

        return None

    def display(self, agents, env_window):

        labels = [[None for _ in range(self.cols)] for _ in range(self.rows)]

        def display_success():
            for widget in env_window.winfo_children():
                widget.destroy()
            tk.Label(env_window, text="SUCCESS", font=("Arial", 24), fg="green").pack(expand=True)
            display_stats()

        def display_failure():
            for widget in env_window.winfo_children():
                widget.destroy()
            tk.Label(env_window, text="FAILURE", font=("Arial", 24), fg="red").pack(expand=True)
            display_stats()

        def display_stats():
            discovered_percentage = ( self.count_discovered_cells() / self.num_free_cells) * 100 if self.num_free_cells else 0
            treasures_percentage = (self.count_consumed_treasures() / self.num_treasures) * 100 if self.num_treasures else 0

            tk.Label(env_window, text=f"Abordagem: {self.approach}", font=("Arial", 15), fg="black").pack(expand=False)
            tk.Label(env_window, text=f"Número de Agentes: {len(self.agents)}", font=("Arial", 15), fg="black").pack(expand=False)
            tk.Label(env_window, text=f"Algoritmo IA: {self.model}", font=("Arial", 15), fg="black").pack(expand=False)
            tk.Label(env_window, text=f"Células descobertas: {discovered_percentage:.2f}%", font=("Arial", 15), fg="black").pack(expand=False)
            tk.Label(env_window, text=f"Tesouros descobertos: {treasures_percentage:.2f}%", font=("Arial", 15), fg="black").pack(expand=False)
            if self.approach == "C":
                if self.is_flag_found():
                    tk.Label(env_window, text=f"Bandeira encontrada.", font=("Arial", 15), fg="black").pack(expand=False)
                else:
                    tk.Label(env_window, text=f"Bandeira não foi encontrada.", font=("Arial", 15), fg="black").pack(expand=False)

        def update_grid():
            for row in range(self.rows):
                for col in range(self.cols):
                    cell = self.grid[row][col]
                    color = cell.display_color()

                    agent_here = None
                    for agent in agents:
                        if agent.alive and agent.position == (row, col):
                            color = "purple"
                            agent_here = agent.name

                    labels[row][col].config(bg=color, text=agent_here if agent_here else cell.type) #type: ignore

        def move_agents(index):
            result = self.verify_success(agents)
            if result == 0:
                env_window.after(130000, env_window.destroy)  # Stop Tkinter loop
                display_success()
                return
            if result == 1:
                env_window.after(130000, env_window.destroy)  # Stop Tkinter loop
                display_failure()
                return

            if index >= len(self.agents):  # Stop if all agents have moved
                env_window.after(20, move_agents, 0)  # Restart loop quickly
                return

            agent = self.agents[index]

            if not agent.alive:
                print(f"{agent.name} is destroyed in {agent.position} and cannot move.")
            else:
                agent.move(self.grid)  # Move only one agent at a time

            update_grid()
            env_window.after(270, move_agents, index + 1)  # Call next agent after 1s

        # GUI setup
        for r in range(self.rows):
            for c in range(self.cols):
                label = tk.Label(
                    env_window, text="", width=6, height=3,
                    bg="white", relief="solid", borderwidth=2
                )
                label.grid(row=r, column=c)
                labels[r][c] = label #type: ignore

        controls_frame = tk.Frame(env_window)
        controls_frame.grid(row=self.rows, column=0, columnspan=self.cols, pady=5)

        # Frame for the start button
        row_frame = tk.Frame(controls_frame)
        row_frame.pack(fill="x", pady=5)
        tk.Button(row_frame, text="Start", bg="green", fg="white",command=lambda index=0 : move_agents(index)).pack(side="left")

        # for i, agent in enumerate(agents):
        #     row_frame = tk.Frame(controls_frame)
        #     row_frame.pack(fill="x", pady=5)
        #     tk.Label(row_frame, text=f"{agent.name}").pack(side="left", padx=5)
        #     tk.Button(row_frame, text="⬆", command=lambda a=agent: move_agent(a, "up")).pack(side="left")
        #     tk.Button(row_frame, text="⬅", command=lambda a=agent: move_agent(a, "left")).pack(side="left")
        #     tk.Button(row_frame, text="⬇", command=lambda a=agent: move_agent(a, "down")).pack(side="left")
        #     tk.Button(row_frame, text="➡", command=lambda a=agent: move_agent(a, "right")).pack(side="left")

        update_grid()