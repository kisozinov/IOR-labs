from src import burn
import numpy as np
import time


def read_file(filename):
    with open('..\\cfp_data\\' + filename + '.txt') as f:
        m, p = list(map(int, f.readline().split()))
        a = np.zeros((m, p))
        for i in range(m):
            details = list(map(int, f.readline().split()[1:]))
            for d in details:
                a[i][d-1] = 1
    return a


def write_to_file(bm_name, answer):
    with open('..\\results\\' + bm_name + '.sol', 'w') as f:
        f.write(str(answer[1]).replace(',', '').replace('[', '').replace(']', '') +
                '\n' + str(answer[0]).replace(',', '').replace('[', '').replace(']', ''))


if __name__ == '__main__':
    data = [
        '20x20',
        '24x40',
        '30x50',
        '30x90',
        '37x53',
    ]

    for bm_name in data:
        total_time = 0
        answers = []
        bm = read_file(bm_name)
        for j in range(5):
            start = time.time()
            labels_p, labels_m = burn.annealing_simulation(bm)
            answers.append((labels_p, labels_m, burn.fitness_function(bm, labels_p, labels_m)))
            total_time += time.time() - start
        print(f'Average time of: {bm_name} - TIME: {total_time / 5}')
        labels_p, labels_m = burn.annealing_simulation(bm)
        answers = sorted(answers,  key=lambda x: x[2], reverse=True)
        print(answers[0])
        write_to_file(bm_name, answers[0])
