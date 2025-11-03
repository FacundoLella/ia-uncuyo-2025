import math
import random
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
import os


def fitness_par_reinas(tablero):
    reinas_amenazadas = 0
    cols = len(tablero)
    for i in range(0, cols):
        for j in range(i + 1, cols):
            if tablero[i] == tablero[j] or abs(tablero[i] - tablero[j]) == abs(i - j):
                reinas_amenazadas += 1
    return reinas_amenazadas

def hill_climbing(tablero, estados_explorados, H_trace=None):
    if H_trace is None:
        H_trace = []
    current_fitness = fitness_par_reinas(tablero)
    H_trace.append(current_fitness)
    best = []
    cols = len(tablero)
    for i in range(cols):
        for j in range(cols):
            if tablero[j] != tablero[i]:
                estados_explorados += 1
                new_tablero = tablero.copy()
                new_tablero[i] = j
                new_fitness = fitness_par_reinas(new_tablero)
                if new_fitness < current_fitness:
                    best.append((new_tablero, new_fitness))
    if best != []:
        new_tablero = min(best, key=lambda x: x[1])[0]
        return hill_climbing(new_tablero, estados_explorados, H_trace)
    else:
        return tablero, estados_explorados, H_trace

def schedule2(t, estados_explorados):
    return t * 0.95

def simulated_annealing(tablero, estados_explorados, t, H_trace=None):
    if H_trace is None:
        H_trace = []
    current_fitness = fitness_par_reinas(tablero)
    H_trace.append(current_fitness)
    if current_fitness == 0 or estados_explorados > 1000:
        return tablero, estados_explorados, H_trace
    aceptado = True
    estados_rechazados = 0
    while aceptado:
        if estados_rechazados > 30:
            return tablero, estados_explorados, H_trace
        col = random.randint(0, len(tablero) - 1)
        row = random.randint(0, len(tablero) - 1)
        if tablero[col] != row:
            new_tablero = tablero.copy()
            new_tablero[col] = row
            new_fitness = fitness_par_reinas(new_tablero)
            estados_explorados += 1
            if new_fitness < current_fitness:
                tablero = new_tablero
                current_fitness = new_fitness
                aceptado = False
            else:
                probabilidad = math.exp((current_fitness - new_fitness) / t)
                if random.random() < probabilidad:
                    tablero = new_tablero
                    current_fitness = new_fitness
                    aceptado = False
                else:
                    estados_rechazados += 1
    t = schedule2(t, estados_explorados)
    return simulated_annealing(tablero, estados_explorados, t, H_trace)

def algoritmo_genetico(tableros, estados_explorados, generaciones, H_trace=None):
    if H_trace is None:
        H_trace = []
    poblacion = tableros.copy()
    n = len(poblacion[0])
    for _ in range(generaciones):
        fitness = [fitness_par_reinas(tablero) for tablero in poblacion]
        H_trace.append(min(fitness))
        if 0 in fitness:
            idx = fitness.index(0)
            return poblacion[idx], estados_explorados, H_trace
        padres = random.sample(poblacion, 2)
        punto_corte = random.randint(1, n - 1)
        hijo = padres[0][:punto_corte] + padres[1][punto_corte:]
        estados_explorados += 1
        if random.random() < 0.1:
            col = random.randint(0, n - 1)
            hijo[col] = random.randint(0, n - 1)
        peor_idx = fitness.index(max(fitness))
        if fitness_par_reinas(hijo) < fitness[peor_idx]:
            poblacion[peor_idx] = hijo
    fitness = [fitness_par_reinas(tablero) for tablero in poblacion]
    mejor_idx = fitness.index(min(fitness))
    return poblacion[mejor_idx], estados_explorados, H_trace

def aleatorio_tablero(n, H_trace=None):
    if H_trace is None:
        H_trace = []
    best_tablero = None
    estados_explorados = 0
    while True:
        tablero = [random.randint(0, n - 1) for _ in range(n)]
        h = fitness_par_reinas(tablero)
        H_trace.append(h)
        estados_explorados += 1
        if h == 0:
            return tablero, estados_explorados, H_trace
        if best_tablero is None or h < fitness_par_reinas(best_tablero):
            best_tablero = tablero
        if estados_explorados > 100:
            return best_tablero, estados_explorados, H_trace


def run_experimento():
    os.makedirs("resultados", exist_ok=True)
    algoritmos = ["aleatorio", "HC", "SA", "GA"]
    tamanios = [4, 8, 10]
    semillas = range(30)
    max_estados = 1000
    resultados_globales = {}

    for alg in algoritmos:
        print(f"\n=== Ejecutando {alg} ===")
        registros = []
        for n in tamanios:
            for seed in tqdm(semillas, desc=f"{alg} N={n}", leave=False):
                random.seed(seed)
                start_time = time.time()
                estados = 0

                if alg == "aleatorio":
                    tablero, estados, H_trace = aleatorio_tablero(n)
                elif alg == "HC":
                    tablero_inicial = [random.randint(0, n - 1) for _ in range(n)]
                    tablero, estados, H_trace = hill_climbing(tablero_inicial, estados)
                elif alg == "SA":
                    tablero_inicial = [random.randint(0, n - 1) for _ in range(n)]
                    tablero, estados, H_trace = simulated_annealing(tablero_inicial, estados, t=1.0)
                elif alg == "GA":
                    poblacion = [[random.randint(0, n - 1) for _ in range(n)] for _ in range(10)]
                    tablero, estados, H_trace = algoritmo_genetico(poblacion, estados, generaciones=100)

                tiempo = time.time() - start_time
                h = fitness_par_reinas(tablero)

                registros.append({
                    "algorithm_name": alg,
                    "env_n": seed,
                    "size": n,
                    "best_solution": tablero,
                    "H": h,
                    "states": estados,
                    "time": tiempo
                })

                if seed == 0:
                    np.save(f"resultados/Htrace_{alg}_N{n}.npy", np.array(H_trace))

        df = pd.DataFrame(registros)
        df.to_csv(f"resultados/{alg}.csv", index=False)
        resultados_globales[alg] = df

    return resultados_globales



def analizar_y_graficar(resultados):
    # Combinar todos los DataFrames
    df_total = pd.concat(resultados.values(), ignore_index=True)

    for n in sorted(df_total["size"].unique()):
        sub = df_total[df_total["size"] == n]
        print(f"\n===== Tamaño {n} =====")
        for alg in sorted(sub["algorithm_name"].unique()):
            sub_alg = sub[sub["algorithm_name"] == alg]
            total = len(sub_alg)
            optimo = (sub_alg["H"] == 0).sum()
            print(f"{alg:>10} → óptimo={optimo}/{total} ({100*optimo/total:.1f}%)")
            print(f"  H promedio={sub_alg['H'].mean():.2f} ± {sub_alg['H'].std():.2f}")
            print(f"  tiempo medio={sub_alg['time'].mean():.4f}s ± {sub_alg['time'].std():.4f}")
            print(f"  estados medios={sub_alg['states'].mean():.1f} ± {sub_alg['states'].std():.1f}")

        # --- GRAFICOS BOXPLOT combinados ---
        fig, axs = plt.subplots(1, 3, figsize=(15, 5))
        metricas = ["H", "time", "states"]
        titulos = ["Valor de H", "Tiempo (s)", "Estados explorados"]

        for i, metrica in enumerate(metricas):
            datos = [sub[sub["algorithm_name"] == alg][metrica] for alg in sorted(sub["algorithm_name"].unique())]
            axs[i].boxplot(datos, labels=sorted(sub["algorithm_name"].unique()))
            axs[i].set_title(titulos[i])
            axs[i].grid(True, linestyle="--", alpha=0.5)

        plt.suptitle(f"Comparación de algoritmos - {n} reinas", fontsize=14)
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.savefig(f"resultados/boxplots_combinados_N{n}.png")
        plt.close()

        # --- GRAFICO DE H-trace (solo una corrida por algoritmo) ---
        plt.figure(figsize=(8, 5))
        for alg in sorted(sub["algorithm_name"].unique()):
            trace_path = f"resultados/Htrace_{alg}_N{n}.npy"
            if os.path.exists(trace_path):
                trace = np.load(trace_path)
                plt.plot(trace, label=alg)
        plt.title(f"Evolución de H por iteración - N={n}")
        plt.xlabel("Iteración")
        plt.ylabel("H")
        plt.legend()
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.savefig(f"resultados/Htrace_combinado_N{n}.png")
        plt.close()


# ============================
#  MAIN
# ============================

if __name__ == "__main__":
    resultados = run_experimento()
    analizar_y_graficar(resultados)
    print("\nTodos los resultados guardados en /resultados")
