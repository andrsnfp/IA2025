from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier

from agent import Agent
from ghost_environment import GhostEnvironment
from env_manager import EnvironmentManager
import random
import tkinter as tk
import pandas as pd

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

    # AI Algorithm Selection
    tk.Label(root, text="Select the AI Algorithm:", font=("Arial", 12)).pack(pady=10)
    ai_algorithm_var = tk.StringVar(value="KNN")  # Default value
    ai_algorithm_options = {
        "K-Nearest Neighbors (KNN)": "KNN",
        "Naive Bayes": "Naive_Bayes",
        "Multi-Layer Perceptron": "MLPClassifier",
        "Mixed (10 agents split across types)": "Mixed"
    }
    for label, value in ai_algorithm_options.items():
        tk.Radiobutton(root, text=label, variable=ai_algorithm_var, value=value).pack(anchor="w")

    # Start Button
    def on_start_button():
        start_simulation(
            num_agents_var.get(),
            num_treasures_var.get(),
            bomb_ratio_var.get(),
            approach_var.get(),
            consume_all_treasure_var.get(),
            ai_algorithm_var.get()
        )
        root.destroy()

    tk.Button(root, text="Create Environment", command=on_start_button, bg="blue", fg="white").pack(pady=20)

    # Run the main GUI loop
    root.mainloop()

def establish_ai_data():
    # Loading the dataset
    dataset = pd.read_csv('training_data/dataset.csv', delimiter=',')

    # Encode categorical features ('L', 'B') into numerical values
    label_encoder = LabelEncoder()
    for column in dataset.columns[:-1]:  # Apply encoding to all feature columns
        dataset[column] = label_encoder.fit_transform(dataset[column])

    # split dataset into features (x) and targets (y)
    x = dataset.iloc[:, 0:4]  # First 4 columns as features
    y = dataset.iloc[:, 4]  # Fifth column as the target
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3, random_state = 7)

    ai_data = x_train, y_train, label_encoder

    return ai_data

# Function to initialize agents based on AI model
def initialize_agents(num_agents, ai_models, agent_positions, consume_all_treasure, ghost_env, training_data,
                      action_labels, encoder):
    agents = []

    if ai_models == "KNN":
        ai_model = KNeighborsClassifier()
        agents = [
            Agent(f"A{i + 1}", agent_positions[i], consume_all_treasure, ghost_env, ai_model, training_data,
                  action_labels, encoder)
            for i in range(num_agents)
        ]

    elif ai_models == "Naive_Bayes":
        ai_model = GaussianNB()
        agents = [
            Agent(f"A{i + 1}", agent_positions[i], consume_all_treasure, ghost_env, ai_model, training_data,
                  action_labels, encoder)
            for i in range(num_agents)
        ]

    elif ai_models == "MLPClassifier":
        ai_model = MLPClassifier()
        agents = [
            Agent(f"A{i + 1}", agent_positions[i], consume_all_treasure, ghost_env, ai_model, training_data,
                  action_labels, encoder)
            for i in range(num_agents)
        ]

    elif ai_models == "Mixed":
        models = [KNeighborsClassifier(), GaussianNB(), MLPClassifier()]

        # Round-robin assignment of models to agents
        agent_models = (models * (num_agents // 3)) + [KNeighborsClassifier()] * (num_agents % 3)
        agents = [
            Agent(f"A{i + 1}", agent_positions[i], consume_all_treasure, ghost_env, agent_models[i], training_data,
                  action_labels, encoder)
            for i in range(num_agents)
        ]

    return agents

# Function to start the environment creation after collecting parameters
def start_simulation(num_agents, num_treasures, bomb_ratio, approach, consume_all_treasure, ai_models):
    # Pre-processing for the agents
    training_data, action_labels, encoder = establish_ai_data()

    # Generate the environment
    agent_positions = tuple((random.randint(0,0),random.randint(0,9)) for _ in range(num_agents))
    env = EnvironmentManager(agent_positions, num_treasures, bomb_ratio, approach)
    env.generate_grid()

    # Generate ghost_environment
    ghost_env = GhostEnvironment()
    ghost_env.initialize_ghost_environment(agent_positions)
    ghost_env.print_ghost_environment()

    # Initialize the agents (agent2.py)
    # agents = [Agent(f"A{i+1}", agent_positions[i],consume_all_treasure, ghost_env) for i in range(num_agents)]

    # Initialize the agents (agent.py)
    agents = initialize_agents(num_agents, ai_models, agent_positions, consume_all_treasure, ghost_env,
                               training_data, action_labels, encoder)

    #Displaying the environment
    env.display(agents)

