import random
import numpy as np

def fitness_function(n, dist, flows, sol):
    ans = 0
    for i in range(n):
        for j in range(n):
            ans += dist[i][j] * flows[sol[i]][sol[j]]
    return ans


def get_start_solution(n, dist, flows):
    return list(np.random.permutation(n))


def recalc_fitness_function(n, dist, flows, sol, i, j, ff):
    for k in range(n):
        ff -= dist[i][k] * flows[sol[i]][sol[k]]
        ff -= dist[j][k] * flows[sol[j]][sol[k]]
    sol[i], sol[j] = sol[j], sol[i]
    for k in range(n):
        ff += dist[i][k] * flows[sol[i]][sol[k]]
        ff += dist[j][k] * flows[sol[j]][sol[k]]
    return sol, ff

def local_search(n, dist, flows, sol):
    dlb = [0 for i in range(n)]
    current_value = fitness_function(n, dist, flows, sol)
    best_sol = []
    best_value = 9999999
    i = 0
    while i < n - 1:
        flag = True
        if dlb[i] == 1:
            i += 1
            continue
        for j in range(i+1, n):
            if dlb[j] == 1:
                continue
            #sol[i], sol[j] = sol[j], sol[i]
            sol, temp_value = recalc_fitness_function(n, dist, flows, sol, i, j, current_value)
            if temp_value < current_value:
                best_sol = sol.copy()
                best_value = temp_value
                flag = False
                i = 0
                break
            else:
                sol[i], sol[j] = sol[j], sol[i]
        if flag:
            dlb[i] = 1
        i += 1
    return best_value, best_sol


def stochastic_2_opt(n, sol):
    #k = random.randint(1, n-2)
    #l = random.randint(k, n-1)
    kl = sorted(random.sample(sol, 2))
    k, l = kl[0], kl[1]
    rev = sol[k:l+1][::-1]
    return sol[:k] + rev + sol[l+1:]


def iterated_local_search(n, dist, flows):
    start_sol = get_start_solution(n, dist, flows)
    value, current_sol = local_search(n, dist, flows, start_sol)
    counter = 0
    #total_counter = 0
    while counter < 50:
        #total_counter += 1
        counter += 1
        perturbated_sol = stochastic_2_opt(n, current_sol)
        temp_val, temp_sol = local_search(n, dist, flows, perturbated_sol)
        if temp_val < value:
            current_sol = temp_sol
            value = temp_val
            counter = 0
    return value, current_sol
