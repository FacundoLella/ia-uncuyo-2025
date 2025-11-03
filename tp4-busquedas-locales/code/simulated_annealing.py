import math
import random
from math import log

def schedule(t,estados_explorados):
    t = t/(log(estados_explorados + 0.5))
    return t

def schedule2(t,estados_explorados):
    t = t*0.95
    return t

def fitness_par_reinas(tablero):
    reinas_amenazadas = 0
    cols = len(tablero)

    for i in range(0,cols):
        lugar_reina = tablero[i]
        for j in range(i+1,cols):
            if tablero[i]==tablero[j] or abs(tablero[i]-tablero[j]) == abs(i-j):
                reinas_amenazadas += 1

    return reinas_amenazadas

#CRITERIOS DE DETENCION:
# - Si encuentra una solucion (fitness = 0)
# - Si exploro mas de 1000 estados
# - Si rechazo 30 estados consecutivos

def simulated_annealing(tablero,estados_explorados,t):

    current_fitness = fitness_par_reinas(tablero)

    if current_fitness == 0 or estados_explorados > 1000:
        return (tablero,estados_explorados)
    
    aceptado = True
    estados_rechazados = 0

    while aceptado:

        if estados_rechazados>30:
            
            return (tablero,estados_explorados)
        
        col = random.randint(0,len(tablero)-1)
        row = random.randint(0,len(tablero)-1)
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
                probababilidad = math.exp((current_fitness - new_fitness)/t)
                if random.random() < probababilidad:
                    tablero = new_tablero
                    current_fitness = new_fitness
                    aceptado = False
                else:
                    estados_rechazados += 1

    t = schedule2(t,estados_explorados)
    return simulated_annealing(tablero,estados_explorados,t)
