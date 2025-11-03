import random
import time
import csv
import statistics
import matplotlib.pyplot as plt

def es_valido(tablero):
   
    for i in range(len(tablero)):
        for j in range(i + 1, len(tablero)):
            if tablero[i] == tablero[j] or abs(tablero[i] - tablero[j]) == abs(i - j):
                return False
    return True


def csp_backtracking_n_reinas(tablero, domain, contador, n):

    if len(tablero) == n:
        return tablero
    if len(tablero) == 0:
        start_idx = random.randint(0, n - 1)
        domain_ordered = domain[start_idx:] + domain[:start_idx]
    else:
        domain_ordered = domain

    for i in domain_ordered:
        contador[0] += 1 
        tablero.append(i)
        if es_valido(tablero):
            result = csp_backtracking_n_reinas(tablero, domain, contador, n)
            if result:
                return result
        tablero.pop()

    return False


def consistent(xi, xj, vi, vj):
    return vi != vj and abs(xi - xj) != abs(vi - vj)

def forward_checking(csp, assignment, domains, var, value):
    n = len(csp)
    new_domains = {v: set(domains[v]) for v in domains}
    new_domains[var] = {value}  

    for other_var in csp:
        if other_var not in assignment and other_var != var:
            diff = abs(other_var - var)
            
            if value in new_domains[other_var]:
                new_domains[other_var].remove(value)
            
            if (value - diff) in new_domains[other_var]:
                new_domains[other_var].remove(value - diff)
            if (value + diff) in new_domains[other_var]:
                new_domains[other_var].remove(value + diff)
            if not new_domains[other_var]:
                return None
    return new_domains


def select_unassigned_variable(assignment, domains):
    unassigned = [v for v in domains if v not in assignment and len(domains[v]) > 0]

    if not unassigned:
        return None

    min_size = min(len(domains[v]) for v in unassigned)
    candidates = [v for v in unassigned if len(domains[v]) == min_size]
    return random.choice(candidates)


def backtrack_fc(csp, domains, assignment, contador):
    if len(assignment) == len(csp):
        return assignment

    var = select_unassigned_variable(assignment, domains)
    if var is None:
        return None


    for value in sorted(domains[var]):
        contador[0] += 1  
        if not all(consistent(var, other_var, value, assignment[other_var]) 
                for other_var in assignment):
            continue
        new_domains = {v: set(domains[v]) for v in domains}
        new_domains[var] = {value}
        for i in csp:
            if i != var and i not in assignment:
                diff = abs(i - var)
                if value in new_domains[i]:
                    new_domains[i].discard(value)
                if (value - diff) in new_domains[i]:
                    new_domains[i].discard(value - diff)
                if (value + diff) in new_domains[i]:
                    new_domains[i].discard(value + diff)
                if not new_domains[i]:
                    new_domains = None
                    break
        if new_domains is None:
            continue
        new_assignment = assignment.copy()
        new_assignment[var] = value
        result = backtrack_fc(csp, new_domains, new_assignment, contador)
        if result is not None:
            return result



def n_queens_forward_checking(n, contador):
    csp = list(range(n))
    domains = {v: set(range(n)) for v in csp}
    assignment = {}
    return backtrack_fc(csp, domains, assignment, contador)


# ---------------------------------
#   PARTE 3 - EXPERIMENTOS
# ---------------------------------
def ejecutar_experimentos(n, algoritmo, nombre_algoritmo):
    resultados = []
    for seed in range(30): 
        random.seed(seed)
        contador = [0]
        start = time.time()
        if nombre_algoritmo == "backtracking":
            tablero = []
            domain = list(range(n))
            result = csp_backtracking_n_reinas(tablero, domain, contador, n)
        else:
            result = n_queens_forward_checking(n, contador)
        end = time.time()

        exito = 1 if result else 0
        tiempo = end - start
        resultados.append((seed, exito, tiempo, contador[0]))
        print(f"Seed {seed}: exito={exito}, tiempo={tiempo:.6f}s, nodos={contador[0]}")


    with open(f"resultados_{nombre_algoritmo}_{n}reinas.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["seed", "exito", "tiempo", "nodos_explorados"])
        writer.writerows(resultados)

    exitos = [r[1] for r in resultados]
    tiempos = [r[2] for r in resultados]
    nodos = [r[3] for r in resultados]

    print(f"\n--- {nombre_algoritmo.upper()} - {n} reinas ---")
    print(f"Éxito: {sum(exitos)}/{len(exitos)} ({sum(exitos)/len(exitos)*100:.2f}%)")
    print(f"Tiempo promedio: {statistics.mean(tiempos):.5f}s")
    print(f"Nodos promedio: {statistics.mean(nodos):.2f}\n")

    return tiempos, nodos


def graficar_boxplots(datos_back, datos_fc, nombre, ylabel):
    plt.figure(figsize=(8, 5))
    plt.boxplot([datos_back, datos_fc], labels=["Backtracking", "Forward Checking"])
    plt.ylabel(ylabel)
    plt.title(f"Comparación de {ylabel} - {nombre} reinas")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.savefig(f"boxplot_{ylabel}_{nombre}reinas.png")
    plt.close()


# ---------------------------------
#   MAIN
# ---------------------------------
if __name__ == "__main__":
    for n in [4, 8,10,12,15]:
        tiempos_back, nodos_back = ejecutar_experimentos(n, csp_backtracking_n_reinas, "backtracking")
        tiempos_fc, nodos_fc = ejecutar_experimentos(n, n_queens_forward_checking, "forward_checking")

        graficar_boxplots(tiempos_back, tiempos_fc, n, "Tiempos (s)")
        graficar_boxplots(nodos_back, nodos_fc, n, "Nodos explorados")
