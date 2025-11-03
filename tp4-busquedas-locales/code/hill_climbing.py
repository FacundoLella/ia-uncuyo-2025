


def fitness_par_reinas(tablero):
    reinas_amenazadas = 0
    cols = len(tablero)

    for i in range(0,cols):
        lugar_reina = tablero[i]
        for j in range(i+1,cols):
            if tablero[i]==tablero[j] or abs(tablero[i]-tablero[j]) == abs(i-j):
                reinas_amenazadas += 1

    return reinas_amenazadas


def hill_climbing(tablero,estados_explorados):
    current_fitness = fitness_par_reinas(tablero)
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
        return(hill_climbing(new_tablero,estados_explorados))
    else:
        return (tablero,estados_explorados)