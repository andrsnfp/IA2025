import random
import tkinter as tk
from cell import Cell

class EnvironmentManager:
    def __init__(self, agents, num_treasures, bombs_ratio, approach):
        self.rows = 10
        self.cols = 10
        self.num_treasures = num_treasures
        self.total_cells = (self.rows * self.cols) - self.num_treasures
        self.num_bombs = int(bombs_ratio * self.total_cells)
        self.num_free_cells = self.total_cells - self.num_bombs
        self.approach = approach
        self.agents = agents
        self.grid = self.generate_grid()

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
        for x, y in self.agents:
            grid[x][y] = Cell('L', (x, y))

        return grid

    def count_consumed_treasures(self):
        return sum(1 for row in self.grid for cell in row if cell.type == 'T' and cell.is_consumed)

    def is_flag_found(self):
        return any (cell.type == 'F' and cell.is_flag_found for row in self.grid for cell in row)

    def verify_success(self, agents):
        if self.approach == 'A' and self.count_consumed_treasures() > self.num_treasures // 2:
            # Count discovered and consumed treasures
            return 0

        if self.approach == 'C' and self.is_flag_found():
            return 0

        if all(not agent.alive for agent in agents):
            return 1

        return

    def display(self, agents):
        # Tkinter window setup
        env_window = tk.Tk()
        env_window.title("Ambiente com Agente")
        labels = [[None for _ in range(self.cols)] for _ in range(self.rows)]

        def display_success():
            for widget in env_window.winfo_children():
                widget.destroy()
            tk.Label(env_window, text="SUCCESS", font=("Arial", 24), fg="green").pack(expand=True)

        def display_failure():
            for widget in env_window.winfo_children():
                widget.destroy()
            tk.Label(env_window, text="FAILURE", font=("Arial", 24), fg="red").pack(expand=True)

        def update_grid():
            for r in range(self.rows):
                for c in range(self.cols):
                    cell = self.grid[r][c]
                    color = cell.display_color()

                    agent_here = None
                    for agent in agents:
                        if agent.alive and agent.position == (r, c):
                            color = "pink"
                            agent_here = agent.name

                    labels[r][c].config(bg=color, text=agent_here if agent_here else cell.type) #type: ignore

            # Check success or failure
            result = self.verify_success(agents)
            if result == 0:
                display_success()
            if result == 1:
                display_failure()

        def move_agent(agent, direction):
            if not agent.alive:
                print(f"{agent.name} is destroyed in {agent.position} and cannot move.")
                return
            agent.move(direction, self.grid)
            update_grid()

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
