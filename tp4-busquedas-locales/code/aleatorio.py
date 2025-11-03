
import random


def fitness_par_reinas(tablero):
    reinas_amenazadas = 0
    cols = len(tablero)

    for i in range(0,cols):
        lugar_reina = tablero[i]
        for j in range(i+1,cols):
            if tablero[i]==tablero[j] or abs(tablero[i]-tablero[j]) == abs(i-j):
                reinas_amenazadas += 1

    return reinas_amenazadas

def aleatorio_tablero(n):
    estados_explorados = 0
    best_tablero = None
    tablero = []
    while True:
        estados_explorados += 1
        for _ in range(n):
            tablero.append(random.randint(0,n-1))
        if fitness_par_reinas(tablero) == 0:
            return tablero,estados_explorados
        if best_tablero is None or fitness_par_reinas(tablero) < fitness_par_reinas(best_tablero):
            best_tablero = tablero
        if estados_explorados>100:
            return best_tablero,estados_explorados