from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier

from sklearn.metrics import confusion_matrix, f1_score, accuracy_score

from agent import Agent
from ghost_environment import GhostEnvironment
from env_manager import EnvironmentManager
import random
import copy
import tkinter as tk
import pandas as pd

# Function to handle entry parameters
def setup_entry_parameters():
    root = tk.Tk()
    root.title("Escolher Parâmetros")

    # Number of Agents Selection
    tk.Label(root, text="Seleccionar o número de agentes:", font=("Arial", 12)).pack(pady=10)
    num_agents_var = tk.IntVar(value=10)  # Default value
    tk.Scale(root, from_=1, to=10, orient=tk.HORIZONTAL, variable=num_agents_var).pack()

    # Number of Treasures Selection
    tk.Label(root, text="Seleccionar o número de tesouros:", font=("Arial", 12)).pack(pady=10)
    num_treasures_var = tk.IntVar(value=14)  # Default value
    tk.Scale(root, from_=8, to=14, orient=tk.HORIZONTAL, variable=num_treasures_var).pack()

    # Bomb Ratio Selection
    tk.Label(root, text="Seleccionar a percentagem de bombas no ambiente:", font=("Arial", 12)).pack(pady=10)
    bomb_ratio_var = tk.DoubleVar(value=0.5)  # Default value
    bomb_options = {
        "50% Bombas": 0.5,
        "60% Bombas": 0.6,
        "70% Bombas": 0.7,
        "80% Bombas": 0.8
    }
    for label, value in bomb_options.items():
        tk.Radiobutton(root, text=label, variable=bomb_ratio_var, value=value).pack(anchor="w")

    # Approach Selection
    tk.Label(root, text="Seleccionar a abordagem a ser usada:", font=("Arial", 12)).pack(pady=10)
    approach_var = tk.StringVar(value="A")  # Default value
    approach_options = {
        "Abordagem A": "A",
        "Abordagem B": "B",
        "Abordagem C": "C"
    }
    for label, value in approach_options.items():
        tk.Radiobutton(root, text=label, variable=approach_var, value=value).pack(anchor="w")

    # Consume All Treasure Selection
    tk.Label(root, text="Um agente consome todo o tesouro?", font=("Arial", 12)).pack(pady=10)
    consume_all_treasure_var = tk.BooleanVar(value=False)  # Default is True
    tk.Radiobutton(root, text="Yes", variable=consume_all_treasure_var, value=True).pack(anchor="w")
    tk.Radiobutton(root, text="No", variable=consume_all_treasure_var, value=False).pack(anchor="w")

    # Start Button
    def on_start_button():
        start_simulation(
            num_agents_var.get(),
            num_treasures_var.get(),
            bomb_ratio_var.get(),
            approach_var.get(),
            consume_all_treasure_var.get(),
        )
        #root.destroy()

    tk.Button(root, text="Criar Ambiente", command=on_start_button, bg="blue", fg="white").pack(pady=20)

    # Run the main GUI loop
    root.mainloop()

def establish_ai_data():
    # Loading the dataset
    dataset = pd.read_csv('training_data/dataset.csv', delimiter = ',')

    # Encode categorical features ('L', 'B') into numerical values
    label_encoder = LabelEncoder()
    for column in dataset.columns[:-1]:  # Apply encoding to all feature columns
        dataset[column] = label_encoder.fit_transform(dataset[column])

    # split dataset into features (x) and targets (y)
    x = dataset[['left','right','up','down']].values  # First 4 columns as features
    y = dataset['Move']  # Fifth column as the target
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 42)

    ai_data = x_train, y_train, label_encoder

    # classifier = KNeighborsClassifier(n_neighbors=7, p=2, metric='euclidean')
    # #classifier = GaussianNB(var_smoothing=1e-5)
    # #classifier = MLPClassifier()
    # classifier.fit(x_train, y_train)
    # y_pred = classifier.predict(x_test)
    #
    # # Evaluate the model
    # cm = confusion_matrix(y_test, y_pred)
    # print("Confusion Matrix:\n", cm)
    #
    # f1 = f1_score(y_test, y_pred, average='macro')
    # print("F1 Score:", f1)
    #
    # accuracy = accuracy_score(y_test, y_pred)
    # print("Accuracy:", accuracy)

    return ai_data

# Function to initialize agents based on AI model
def initialize_agents(num_agents, ai_models, agent_positions, consume_all_treasure, ghost_env, training_data,
                      action_labels, encoder):
    agents = []

    if ai_models == "KNN":
        ai_model = KNeighborsClassifier(n_neighbors = 21, p = 2, metric = 'euclidean')
        ai_model.fit(training_data, action_labels)
        agents = [
            Agent(f"A{i + 1}", agent_positions[i], consume_all_treasure, ghost_env, ai_model,encoder)
            for i in range(num_agents)
        ]

    elif ai_models == "Naive_Bayes":
        ai_model = GaussianNB(var_smoothing=1e-5)
        ai_model.fit(training_data, action_labels)
        print("Agents Trained")
        agents = [
            Agent(f"A{i + 1}", agent_positions[i], consume_all_treasure, ghost_env, ai_model,encoder)
            for i in range(num_agents)
        ]

    elif ai_models == "MLPClassifier":
        ai_model = MLPClassifier()
        ai_model.fit(training_data, action_labels)
        agents = [
            Agent(f"A{i + 1}", agent_positions[i], consume_all_treasure, ghost_env, ai_model,encoder)
            for i in range(num_agents)
        ]

    elif ai_models == "Mixed":
        models = [KNeighborsClassifier(n_neighbors = 21, p = 2, metric = 'euclidean'), GaussianNB(var_smoothing=1e-5), MLPClassifier()]

        for model in models:
            model.fit(training_data, action_labels)

        # Round-robin assignment of models to agents
        agents = [
            Agent(f"A{i + 1}", agent_positions[i], consume_all_treasure, ghost_env, models[i % 3], encoder)
            for i in range(num_agents)
        ]

    return agents

# Function to start the environment creation after collecting parameters
def start_simulation(num_agents, num_treasures, bomb_ratio, approach, consume_all_treasure):
    # Pre-processing for the agents
    training_data, action_labels, encoder = establish_ai_data()

    # Generate ghost_environment
    agent_positions = tuple((random.randint(0,9),random.randint(0,9)) for _ in range(num_agents))
    ghost_env = GhostEnvironment()
    ghost_env.initialize_ghost_environment(agent_positions)
    ghost_env.print_ghost_environment()

    # Initialize the agentss (agent.py)
    agents_knn = initialize_agents(num_agents, "KNN", agent_positions, consume_all_treasure, ghost_env,
                               training_data, action_labels, encoder)
    agents_naive_bayes = initialize_agents(num_agents, "Naive_Bayes", agent_positions, consume_all_treasure, ghost_env,
                                   training_data, action_labels, encoder)
    agents_mlpclassifier = initialize_agents(num_agents, "MLPClassifier", agent_positions, consume_all_treasure, ghost_env,
                                           training_data, action_labels, encoder)
    agents_mixed = initialize_agents(num_agents, "Mixed", agent_positions, consume_all_treasure, ghost_env,
                                           training_data, action_labels, encoder)

    # Generate the environments
    env = EnvironmentManager(agent_positions, num_treasures, bomb_ratio, approach)
    env.generate_grid()

    # Creating copies of env
    env_knn = copy.deepcopy(env)
    env_naive_bayes = copy.deepcopy(env)
    env_mlpclassifier = copy.deepcopy(env)
    env_mixed = copy.deepcopy(env)

    # Giving the copies its agents
    env_knn.receive_agents(agents_knn, 'KNN')
    env_naive_bayes.receive_agents(agents_naive_bayes, 'Naive_Bayes')
    env_mlpclassifier.receive_agents(agents_mlpclassifier, 'MLPClassifier')
    env_mixed.receive_agents(agents_mixed, 'Mixed')

    # Create a single Tkinter root window
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Function to create multiple environment windows
    def create_env_window(env, agents, title):
        window = tk.Toplevel(root)  # Create a new Tkinter window
        window.title(title)
        env.display(agents, window)  # Pass the window to the display function

    # Create all environments as separate windows
    create_env_window(env_knn, agents_knn, "Ambiente KNN")
    create_env_window(env_naive_bayes, agents_naive_bayes, "Ambiente Naive Bayes")
    create_env_window(env_mlpclassifier, agents_mlpclassifier, "Ambiente MLPClassifier")
    create_env_window(env_mixed, agents_mixed, "Ambiente Misto")

    #Displaying the environment
    #env.display(agents_knn)

    root.mainloop()