def consistent(xi, xj, vi, vj):
    """Chequea que dos reinas no se ataquen."""
    return vi != vj and abs(vi - vj) != abs(xi - xj)


def forward_checking(csp, assignment, domains, var, value):
    """Aplica forward checking después de asignar var = value."""
    new_domains = {v: set(domains[v]) for v in domains}
    for other_var in csp:
        if other_var not in assignment and other_var != var:
            for val in list(new_domains[other_var]):
                if not consistent(var, other_var, value, val):
                    new_domains[other_var].remove(val)
            # Si algún dominio queda vacío → fallo
            if not new_domains[other_var]:
                return None
    return new_domains


def select_unassigned_variable(assignment, domains):
    """Heurística MRV: variable con menos valores posibles."""
    unassigned = [v for v in domains if v not in assignment]
    return min(unassigned, key=lambda var: len(domains[var]))


def backtrack(csp, domains, assignment):
    if len(assignment) == len(csp):
        return assignment

    var = select_unassigned_variable(assignment, domains)

    for value in sorted(domains[var]):
        # Asignar provisionalmente
        new_assignment = assignment.copy()
        new_assignment[var] = value

        new_domains = forward_checking(csp, new_assignment, domains, var, value)
        if new_domains is not None:
            result = backtrack(csp, new_domains, new_assignment)
            if result is not None:
                return result

    return None


def n_queens_csp(n):
    csp = list(range(n))  # variables 0..n-1 (filas)
    domains = {v: set(range(n)) for v in csp}
    assignment = {}
    return backtrack(csp, domains, assignment)