
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

#ESTRATEGIA DE SELECCION: RANDOM
#ESTRATEGIA DE REEMPLAZO: SI EL HIJO ES MEJOR QUE EL PEOR DE LA POBLACION, LO REEMPLAZA
#OPERADORES: CRUZAMIENTO SIMPLE, MUTACION SIMPLE
#CRITERIOS DE PARADA: SI ALGUN HIJO TIENE FITNESS 0, 100 GENERACIONES

def algoritmo_genetico(tableros,estados_explorados,generaciones):
    poblacion = tableros.copy()
    n = len(poblacion[0])
    for _ in range(generaciones):
        # Evaluar fitness
        fitness = [fitness_par_reinas(tablero) for tablero in poblacion]
        if 0 in fitness:
            idx = fitness.index(0)
            return poblacion[idx], estados_explorados

        # Selección aleatoria de padres
        padres = random.sample(poblacion, 2)
        punto_corte = random.randint(1, n-1)
        # Cruzamiento simple
        hijo = padres[0][:punto_corte] + padres[1][punto_corte:]
        estados_explorados += 1

        # Mutación simple (opcional)
        if random.random() < 0.1:
            col = random.randint(0, n-1)
            hijo[col] = random.randint(0, n-1)

        # Reemplazo: si el hijo es mejor que el peor, lo reemplaza
        peor_idx = fitness.index(max(fitness))
        if fitness_par_reinas(hijo) < fitness[peor_idx]:
            poblacion[peor_idx] = hijo

    # Devuelve el mejor tablero encontrado
    fitness = [fitness_par_reinas(tablero) for tablero in poblacion]
    mejor_idx = fitness.index(min(fitness))
    return poblacion[mejor_idx], estados_explorados