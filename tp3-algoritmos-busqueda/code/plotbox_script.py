import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# === Leer CSV ===
df = pd.read_csv("results.csv", header=None, names=[
    "algorithm_name", "env_n", "states_n", 
    "actions_count", "actions_cost", "time", "solution_found"
])

# === Excluir DFS para estos gráficos ===
df_no_dfs = df[df['algorithm_name'] == 'DFS']

# === Crear carpeta de salida ===
output_dir = "plots"
os.makedirs(output_dir, exist_ok=True)

# === Métricas a graficar ===
metricas = ["states_n", "actions_count", "actions_cost", "time"]

# === Gráfico por métrica (sin DFS) ===
for metrica in metricas:
    plt.figure(figsize=(10,6))
    sns.boxplot(x="algorithm_name", y=metrica, data=df_no_dfs)
    plt.title(f"Distribución de {metrica} por algoritmo", fontsize=14)
    plt.xlabel("Algoritmo")
    plt.ylabel(metrica.replace("_", " ").title())
    plt.grid(True, axis="y", linestyle="--", alpha=0.7)

    # Guardar cada gráfico
    filename = os.path.join(output_dir, f"{metrica}_boxplot_onlyDFS.png")
    plt.savefig(filename, dpi=300, bbox_inches="tight")
    plt.close()

print(f"✅ Gráficos sin DFS guardados en: {output_dir}/")
