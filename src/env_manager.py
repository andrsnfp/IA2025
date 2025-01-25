import random
import tkinter as tk
from cell import Cell
import json

class EnvironmentManager:
    def __init__(self, agents_positions, num_treasures, bombs_ratio, approach, time):
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
        self.total_movements = 0  # Contador de movimentos

        self.countdown_timer = True
        self.time_remaining = time


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

        # Timer label (added to GUI)
        self.timer_label = tk.Label(env_window, text="", font=("Arial", 14), fg="red")
        self.timer_label.grid(row=self.rows + 1, column=0, columnspan=self.cols, pady=5)

        def display_success():
            for widget in env_window.winfo_children():
                widget.destroy()
            tk.Label(env_window, text="SUCCESSO", font=("Arial", 24), fg="green").pack(expand=True)
            display_stats()

        def display_failure():
            for widget in env_window.winfo_children():
                widget.destroy()
            tk.Label(env_window, text="FRACASSO", font=("Arial", 24), fg="red").pack(expand=True)
            display_stats()

        def display_stats():
            discovered_percentage = ( self.count_discovered_cells() / self.num_free_cells) * 100 if self.num_free_cells else 0
            treasures_percentage = (self.count_consumed_treasures() / self.num_treasures) * 100 if self.num_treasures else 0

            tk.Label(env_window, text=f"Abordagem: {self.approach}", font=("Arial", 15), fg="black").pack(expand=False)
            tk.Label(env_window, text=f"Número de Agentes: {len(self.agents)}", font=("Arial", 15), fg="black").pack(expand=False)
            tk.Label(env_window, text=f"Algoritmo IA: {self.model}", font=("Arial", 15), fg="black").pack(expand=False)
            tk.Label(env_window, text=f"Células descobertas: {discovered_percentage:.2f}%", font=("Arial", 15), fg="black").pack(expand=False)
            tk.Label(env_window, text=f"Tesouros descobertos: {treasures_percentage:.2f}%", font=("Arial", 15), fg="black").pack(expand=False)
            tk.Label(env_window, text=f"Total de Movimentos: {self.total_movements}", font=("Arial", 15),fg="black").pack(expand=False)
            if self.approach == "C":
                if self.is_flag_found():
                    tk.Label(env_window, text=f"Bandeira encontrada.", font=("Arial", 15), fg="black").pack(expand=False)
                else:
                    tk.Label(env_window, text=f"Bandeira não foi encontrada.", font=("Arial", 15), fg="black").pack(expand=False)
            if self.countdown_timer == False:
                tk.Label(env_window, text="O tempo acabou.", font=("Arial", 15), fg="black").pack(expand=False)

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

            # Check if time is up
            if self.countdown_timer == False:
                print("O tempo acabou! Terminando a simulação.")
                display_failure()
                return  # Stop movement

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
                print(f"{agent.name} foi destruído em {agent.position}.")
            else:
                previous_position = agent.position
                agent.move(self.grid)  # Move only one agent at a time

                if agent.position != previous_position:
                    self.total_movements += 1

            update_grid()
            env_window.after(500, move_agents, index + 1)  # VELOCIDADE DA SIMULACAO

            def move_agent(agent, direction):
                if not agent.alive:
                    print(f"{agent.name} is destroyed in {agent.position} and cannot move.")
                    return
                agent.manual_move(direction, self.grid)
                update_grid()

        def start_countdown():
            """Start a countdown timer and trigger failure if time runs out."""

            def update_timer():
                minutes = self.time_remaining // 60
                seconds = self.time_remaining % 60
                self.timer_label.config(text=f"Tempo restante: {minutes}:{seconds:02d}")  # Format MM:SS

                if self.time_remaining > 0:
                    self.time_remaining -= 1
                    env_window.after(1000, update_timer)  # Update every second
                else:
                    self.countdown_timer = False  # Timer is up
                    return
            
            update_timer()

        def stop_countdown():
            self.time_remaining = 0

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
        tk.Button(row_frame, text="Start", bg="green", fg="white",command=lambda: [move_agents(0), start_countdown()]).pack(side="left")
        tk.Button(row_frame, text="Stop", bg="red", fg="white",command=stop_countdown).pack(side="left")

        # for i, agent in enumerate(agents):
        #     row_frame = tk.Frame(controls_frame)
        #     row_frame.pack(fill="x", pady=5)
        #     tk.Label(row_frame, text=f"{agent.name}").pack(side="left", padx=5)
        #     tk.Button(row_frame, text="⬆", command=lambda a=agent: move_agent(a, "up")).pack(side="left")
        #     tk.Button(row_frame, text="⬅", command=lambda a=agent: move_agent(a, "left")).pack(side="left")
        #     tk.Button(row_frame, text="⬇", command=lambda a=agent: move_agent(a, "down")).pack(side="left")
        #     tk.Button(row_frame, text="➡", command=lambda a=agent: move_agent(a, "right")).pack(side="left")

        update_grid()