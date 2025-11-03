import random

def es_valido(tablero):
    if len(tablero)==1:
        return True
    for i in range(len(tablero)):
        for j in range(i + 1, len(tablero)):
            if tablero[i] == tablero[j] or abs(tablero[i] - tablero[j]) == abs(i - j):
                print("Conflicto entre reinas en filas", i, "y", j)
                return False
    return True
    
def csp_backtracking_n_reinas(tablero, domain, contador, n):
    contador[0] += 1
    if len(tablero) == n:
        return tablero

 
    if len(tablero) == 0:
        start_idx = random.randint(0, n - 1)
        domain_ordered = domain[start_idx:] + domain[:start_idx]
    else:
        domain_ordered = domain

    for i in domain_ordered:
        tablero.append(i)
        if es_valido(tablero):
            result = csp_backtracking_n_reinas(tablero, domain, contador, n)
            if result:
                return result
        tablero.pop()

    return False