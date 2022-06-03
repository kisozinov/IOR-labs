import random

def fitness_function(n, dist, flows, sol):
    ans = 0
    for i in range(n):
        for j in range(n):
            ans += dist[i][j] * flows[sol[i]][sol[j]]
    return ans


def get_start_solution(n, dist, flows):
    sol = [i for i in range(n)]
    random.shuffle(sol)
    return sol


def local_search(n, dist, flows, sol):
    dlb = [0 for i in range(n)]
    current_sol = fitness_function(n, dist, flows, sol)
    for i in range(n-1):
        for j in range(i+1, n):
            if dlb[j] == 1:
                break
            flag = True
            sol[i], sol[j] = sol[j], sol[i]
            temp_sol = fitness_function(n, dist, flows, sol)
            if temp_sol >= current_sol:
                sol[i], sol[j] = sol[j], sol[i]
            else:
                current_sol = temp_sol
                flag = False
                break
        if flag:
            dlb[i] = 1
    return current_sol, sol


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
    while counter < 50:
        counter += 1
        perturbated_sol = stochastic_2_opt(n, current_sol)
        temp_val, temp_sol = local_search(n, dist, flows, perturbated_sol)
        if temp_val < value:
            current_sol = temp_sol
            value = temp_val
            counter = 0
    return value, current_sol
