import numpy as np
from sklearn.cluster import KMeans
import functools as ft
import random
import math


def calc_labels_m(a, labels_p):
    p = np.shape(a)[1]
    cells = set(labels_p)
    errs = []
    for i in range(len(a)):
        for cell in cells:
            v = 0
            e = 0
            for j in range(p):
                if labels_p[j] == cell:
                    if a[i][j] == 0:
                        e += 1
                else:
                    if a[i][j] == 1:
                        v += 1
            errs.append(e + v)
    errs_size = len(a), len(cells)
    errs = list(ft.reduce(lambda x, y: map(list, zip(*y * (x,))), (iter(errs), *errs_size[:0:-1])))
    labels_m = []
    for e in errs:
        labels_m.append(e.index(min(e)))
    return labels_m


def fitness_function(a, labels_p, labels_m):
    p = np.shape(a)[1]
    n_1 = 0
    n_0_in = 0
    n_1_out = 0
    n1_in = 0
    for machine in a:
        for detail in machine:
            n_1 += detail
    for i in range(len(a)):
        for j in range(p):
            if labels_m[i] == labels_p[j]:
                if a[i][j] == 0:
                    n_0_in += 1
                else:
                    n1_in += 1
    n_1_out = n_1 - n1_in
    #print('n1 ', n_1)
    #print('n1_out ', n_1_out)
    #print('n0_in', n_0_in)
    S = (n_1 - n_1_out) / (n_1 + n_0_in)
    # print(S)
    return S


def initial_solution(a, C):
    # similarity matrix b
    p = np.shape(a)[1]
    b = np.zeros((p, p))
    for i in range(p):
        for j in range(0, p):
            both = 0
            only_i = 0
            only_j = 0
            for x in range(len(a)):
                if a[x][i] == 1 and a[x][j] == 1:
                    both += 1
                elif a[x][i] == 1:
                    only_i += 1
                elif a[x][j] == 1:
                    only_j += 1
            b[i][j] = both / (both + only_j + only_i)

    # clustering P
    kmeans = KMeans(n_clusters=C, random_state=0).fit(b)
    labels_p = kmeans.labels_
    # clustering M
    labels_m = calc_labels_m(a, labels_p)
    # calc fitness_function
    f0 = fitness_function(a, labels_p, labels_m)
    return b, labels_p, labels_m, f0


def single_move(a, labels_p, labels_m, counter_cells, S):
    # развить в цикл
    #move_idx = random.randint(0, len(labels_p) - 1)
    cells = [x for x in range(counter_cells)]
    original_m = labels_m.copy()
    best_p = labels_p.copy()
    for move_idx in range(len(labels_p)):
        original_cell = labels_p[move_idx]
        for cell in cells:
            if cell != labels_p[move_idx]:
                labels_p[move_idx] = cell
                labels_m = calc_labels_m(a, labels_p)
                S_c = fitness_function(a, labels_p, labels_m)
                if S_c > S:
                    S = S_c
                    best_p = labels_p.copy()
                    # print('############ YA PEREZAPISAL #############')
                labels_p[move_idx] = original_cell
                labels_m = original_m
    labels_p = best_p
    labels_m = calc_labels_m(a, labels_p)
    return labels_p, labels_m


def exchange_move(a, labels_p, labels_m, counter_cells, S):
    # развить в цикл
    #move_idx = random.randint(0, len(labels_p) - 1)
    cells = [x for x in range(counter_cells)]
    original_m = labels_m.copy()
    best_p = labels_p.copy()
    for move_idx in range(len(labels_p)-1):
        for move_jdx in range(move_idx, len(labels_p)):
            original_cell = labels_p[move_idx]
            #original_cell2 = labels_p[move_jdx]
            for cell in cells:
                if cell != labels_p[move_idx] and labels_p[move_idx] != labels_p[move_jdx]:
                    labels_p[move_idx] = cell
                    labels_p[move_jdx] = original_cell
                    labels_m = calc_labels_m(a, labels_p)
                    S_c = fitness_function(a, labels_p, labels_m)
                    if S_c > S:
                        S = S_c
                        best_p = labels_p.copy()
                        # print('############ YA PEREZAPISAL EXCHANGE #############')
                    labels_p[move_idx], labels_p[move_jdx] = labels_p[move_jdx], labels_p[move_idx]
                    labels_m = original_m
    labels_p = best_p
    labels_m = calc_labels_m(a, labels_p)
    return labels_p, labels_m


def annealing_simulation(a): # Main function
    # print('Generating initial solution:')
    C = 2
    goto2 = True
    b, labels_p, labels_m, f = initial_solution(a, C)
    labels_pbest, labels_mbest = labels_p, labels_m
    f_i = f
    while True:
        if goto2:
            b, labels_p, labels_m, f = initial_solution(a, C)
            labels_pi, labels_mi = labels_p, labels_m
            # C = 2
            L = 11
            D = 10
            alpha = 0.5
            counter_mc = 0
            counter_trapped = 0
            counter_stagnant = 0
            counter = 0
            T_0 = 1
            T_f = 0.2
            T = T_0

        goto2 = False
        while counter_mc < L and counter_trapped < L / 2:
            # print('\nNEW ITERATION')
            if counter_mc % D == 0 and counter_mc != 0:
                labels_pc, labels_mc = exchange_move(a, labels_p, labels_m, C, f_i)
            else:
                labels_pc, labels_mc = single_move(a, labels_p, labels_m, C, f_i)
            f_c = fitness_function(a, labels_pc, labels_mc)

            if f_c > f_i:
                labels_pi, labels_mi = labels_pc, labels_mc
                labels_p, labels_m = labels_pc, labels_mc
                counter_stagnant = 0
                counter_mc += 1
                f_i = f_c
                continue

            elif f_c == f_i:
                labels_p, labels_m = labels_pc, labels_mc
                counter_stagnant += 1
                counter_mc += 1
                continue

            delta = f_c - fitness_function(a, labels_p, labels_m)
            if math.e ** (delta / T) > random.uniform(0, 1):
                labels_p, labels_m = labels_pc, labels_mc
                counter_trapped = 0
            else:
                counter_trapped += 1
            counter_mc += 1
            # continue
        if T <= T_f or counter_stagnant > 100:
            if f_i > fitness_function(a, labels_pbest, labels_mbest):
                labels_pbest, labels_mbest = labels_pi, labels_mi
                C += 1
                goto2 = True
            else:
                break
        else:
            T = T * alpha
            counter_mc = 0
            counter += 1
            continue
    return labels_pbest, labels_mbest
        # print('DELTA: ', delta)
    #print(f"Final ff on {C} cells: {fitness_function(a, labels_pi, labels_mi)}")
    #return 0
