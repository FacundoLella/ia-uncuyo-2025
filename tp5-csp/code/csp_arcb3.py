import copy
def eliminar_valores_conflictivos(tablero, domains):
    new_domains = copy.deepcopy(domains)
    fila_actual = len(tablero) - 1
    new_domains[fila_actual] = [domains[fila_actual][0]]
    columna_reina = tablero[-1]
    for i in range(fila_actual + 1, len(new_domains)):
        if columna_reina in new_domains[i]:
            new_domains[i].remove(columna_reina)
        distancia_fila = i - fila_actual
        if columna_reina - distancia_fila in new_domains[i]:
            new_domains[i].remove(columna_reina - distancia_fila)
        if columna_reina + distancia_fila in new_domains[i]:
            new_domains[i].remove(columna_reina + distancia_fila)
    return new_domains
    
def csp_forward_checking_n_reinas(tablero,domains,index,contador):
    if len(tablero)==8:
        return tablero
    domain = domains[index]
    if len(domain)==0:
        return False
    for i in domain:
        contador[0] += 1
        tablero.append(i)
        new_domains = eliminar_valores_conflictivos(tablero,domains)
        if any(len(d) == 0 for d in new_domains[index+1:]):
            tablero.pop()
            continue

        resultado = csp_forward_checking_n_reinas(tablero, new_domains, index+1, contador)
        if resultado:
            return resultado
        tablero.pop()   
    return False