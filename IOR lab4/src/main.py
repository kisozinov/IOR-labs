import time
import src.qap_search as qap


def read_file(filename):
    with open('..\\' + filename) as f:
        n = int(f.readline())
        distances, flows = [], []
        for i in range(n):
            distances.append([int(item) for item in f.readline().split()])
        f.readline()
        for i in range(n):
            flows.append([int(item) for item in f.readline().split()])
    return n, distances, flows


if __name__ == '__main__':
    data = {
            'tai20a': read_file('benchmarks\\tai20a'),
            'tai40a': read_file('benchmarks\\tai40a'),
            'tai60a': read_file('benchmarks\\tai60a'),
            'tai80a': read_file('benchmarks\\tai80a'),
            'tai100a': read_file('benchmarks\\tai100a'),
        }
    for filename in data:
        print(filename)
        results_two_opt = []
        time_executed = 0
        for i in range(10):
            start_time = time.time()
            results_two_opt.append(qap.local_search(*data[filename], qap.get_start_solution(*data[filename])))
            time_executed += time.time() - start_time
        print('Local search')
        print(f'Average time: {time_executed/10}')
        best_result = sorted(results_two_opt, key=lambda x: x[1])[0]
        print(f'Best result: {best_result[1]}')
        print(f'Best value: {best_result[0]}')

        with open(f'..\\results\\local_search\\{filename}.sol', 'w') as f:
            f.write(' '.join(list(map(str, best_result[1]))))


        print()

        results_iterated_local = []
        time_executed = 0
        for i in range(10):
            start_time = time.time()
            results_iterated_local.append(qap.iterated_local_search(*data[filename]))
            time_executed += time.time() - start_time
        print('Iterated local search')
        print(f'Average time: {time_executed / 10}')
        best_result = sorted(results_iterated_local, key=lambda x: x[0])[0]
        print(f'Best value: {best_result[0]}')
        print(f'Best result: {best_result[1]}')

        file = open(f'..\\results\\iterated_local_search\\{filename}.sol', 'w')
        file.write(' '.join(list(map(str, best_result[1]))))

        print('-----------------------------------------------')