import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json

# Simulação de dados das métricas para visualização
dados_simulacao = {
    "Algoritmo IA": ["KNN", "Naive Bayes", "MLP", "Mixed"],
    "Células Descobertas (%)": [85, 77, 90, 82],
    "Tesouros Descobertos (%)": [80, 70, 88, 75],
    "Agentes Sobreviventes": [7, 4, 9, 6],
    "Movimentos Totais": [250, 230, 270, 245],
    "Tempo Restante (s)": [45, 30, 50, 35],
    "Bombas no Ambiente": [12, 10, 15, 11],
}

env_files = ["simulation_results_KNN.json", "simulation_results_Naive_Bayes.json",
             "simulation_results_MLPClassifier.json", "simulation_results_Mixed.json"]

# Load data from all environments
all_data = []
for file in env_files:
    try:
        with open(file, "r") as f:
            data = json.load(f)
            all_data.append(data)
    except FileNotFoundError:
        print(f"❌ Warning: {file} not found. Skipping...")

# Merge data into a single file
with open("merged_simulation_results.json", "w") as f:
    json.dump(all_data, f, indent=4)

print("✅ Todos os dados foram mesclados em 'merged_simulation_results.json'")

# Convert to DataFrame for visualization
df_simulacao = pd.DataFrame(all_data)

# # Generate graphs
# df_simulacao.set_index("Algoritmo IA")[["Células Descobertas (%)", "Tesouros Descobertos (%)"]].plot(kind="bar")
# plt.title("Desempenho dos Algoritmos de IA")
# plt.ylabel("Porcentagem (%)")
# plt.show()

# # Criar DataFrame com os dados da simulação
# df_simulacao = pd.DataFrame(dados_simulacao)

# Criar gráfico de barras para células descobertas e tesouros descobertos
fig, ax = plt.subplots(figsize=(10, 5))
bar_width = 0.35
index = np.arange(len(df_simulacao["Algoritmo IA"]))

# Barras de células descobertas
bars1 = ax.bar(index, df_simulacao["Células Descobertas (%)"], bar_width, label="Células Descobertas", color="blue")

# Barras de tesouros descobertos
bars2 = ax.bar(index + bar_width, df_simulacao["Tesouros Descobertos (%)"], bar_width, label="Tesouros Descobertos", color="gold")

# Configuração do gráfico
ax.set_xlabel("Algoritmo de IA")
ax.set_ylabel("Porcentagem (%)")
ax.set_title("Comparação de Células e Tesouros Descobertos por Algoritmo")
ax.set_xticks(index + bar_width / 2)
ax.set_xticklabels(df_simulacao["Algoritmo IA"])
ax.legend()

# Exibir gráfico de barras
plt.show()

# Criar gráfico de pizza para agentes sobreviventes
fig, ax = plt.subplots(figsize=(7, 7))
ax.pie(df_simulacao["Agentes Sobreviventes"], labels=df_simulacao["Algoritmo IA"], autopct="%1.1f%%", startangle=90, colors=["blue", "red", "green", "orange"])
ax.set_title("Proporção de Agentes Sobreviventes por Algoritmo")

# Exibir gráfico de pizza
plt.show()

# Criar gráfico de linhas para tempo restante na simulação
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(df_simulacao["Algoritmo IA"], df_simulacao["Tempo Restante (s)"], marker="o", linestyle="-", color="purple", label="Tempo Restante")
ax.set_xlabel("Algoritmo de IA")
ax.set_ylabel("Tempo Restante (s)")
ax.set_title("Tempo Restante por Algoritmo")
ax.legend()

# Exibir gráfico de linhas
plt.show()

# Criar gráfico de barras para bombas no ambiente
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(df_simulacao["Algoritmo IA"], df_simulacao["Bombas no Ambiente"], color="brown")
ax.set_xlabel("Algoritmo de IA")
ax.set_ylabel("Número de Bombas")
ax.set_title("Número de Bombas no Ambiente por Algoritmo")

# Exibir gráfico de bombas
plt.show()