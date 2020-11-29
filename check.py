import time

import numpy as np

import ex1
import search


def timeout_exec(func, args=(), kwargs={}, timeout_duration=10, default=None):
    """This function will spawn a thread and run the given function
    using the args, kwargs and return the given default value if the
    timeout_duration is exceeded.
    """
    import threading
    class InterruptableThread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.result = default

        def run(self):
            # remove try if you want program to abort at error
            # try:
            self.result = func(*args, **kwargs)
            # except Exception as e:
            #    self.result = (-3, -3, e)

    it = InterruptableThread()
    it.start()
    it.join(timeout_duration)
    if it.is_alive():
        return default
    else:
        return it.result


def check_problem(p, search_method, timeout):
    """ Constructs a problem using ex1.create_wumpus_problem,
    and solves it using the given search_method with the given timeout.
    Returns a tuple of (solution length, solution time, solution)"""

    """ (-2, -2, None) means there was a timeout
    (-3, -3, ERR) means there was some error ERR during search """

    t1 = time.time()
    s = timeout_exec(search_method, args=[p], timeout_duration=timeout)
    t2 = time.time()

    if isinstance(s, search.Node):
        solve = s
        solution = list(map(lambda n: n.action, solve.path()))[1:]
        return (len(solution), t2 - t1, solution)
    elif s is None:
        return (-2, -2, None)
    else:
        return s


def solve_problems(problems, weights):
    solved = 0
    for i, problem in enumerate(problems):
        try:
            # weights = [0.3214811807174396, 0.7931524209752023, 0.10004562939257255, 0.3748156568695349,
            #            0.07650427762183343, 0.1639237155039427, 0.6766203622831798, 0.23211957815601592]
            p = ex1.create_medical_problem(problem, weights=weights)
        except Exception as e:
            print("Error creating problem: ", e)
            return None
        timeout = 60
        result = check_problem(p, (lambda p: search.best_first_graph_search(p, p.h)), timeout)
        print(i + 1, "GBFS ", result)
        if result[2] != None:
            if result[0] != -3:
                solved = solved + 1


def find_optimal_weights(problems, total_runs):
    for i in range(total_runs):
        evaluate_weights(problems, i)


def evaluate_weights(problems, i):
    weights = np.random.random(ex1.NUM_MEASURES)
    # weights = np.insert(np.positive(np.random.normal(size=ex1.NUM_MEASURES-1)), 0, 1)
    # weights[weights < 0] = -weights[weights < 0]

    results = []
    max_time = 0

    for j, problem in enumerate(problems):
        start = time.time()
        try:
            p = ex1.create_medical_problem(problem, weights=weights)
            timeout = 60
            output = check_problem(p, (lambda p: search.best_first_graph_search(p, p.h)), timeout)
        except Exception:
            print(f'run {i + 1:>2}: error in problem {j + 1:>2} weights:', *np.round(weights, 2))
            return

        if output[0] == -2:
            print(f'run {i + 1:>2}: timeout in problem {j + 1:>2} after {round(time.time() - start)} seconds weights:',
                  *np.round(weights, 2))
            with open(f'results/{j + 1}', 'a') as f:
                f.write(','.join([str(val) for val in weights]) + '\n')
            return

        results.append(output[0])
        max_time = max(output[1], max_time)

    print(f'run {i + 1:>2}: finished successfully weights:', *np.round(weights, 2))
    run_result = np.average(results)
    with open('results/done', 'a') as f:
        f.write(', '.join([str(val) for val in weights]) + f' - {run_result} - {max_time}\n')


def main():
    print(ex1.ids)
    """Here goes the input you want to check"""
    problems = [
        {
            "police": 1,
            "medics": 1,
            "map": (
                ('U', 'H', 'S', 'H',),
                ('H', 'U', 'H', 'S',),
                ('U', 'H', 'H', 'U',),
            )
        },

        {
            "police": 1,
            "medics": 1,
            "map": (
                ('U', 'H', 'S', 'H', 'S'),
                ('H', 'U', 'H', 'S', 'H'),
                ('U', 'H', 'H', 'U', 'H'),
                ('H', 'H', 'H', 'H', 'H'),
            )
        },

        {
            "police": 2,
            "medics": 2,
            "map": (
                ('U', 'H', 'S', 'H', 'S'),
                ('H', 'U', 'H', 'S', 'H'),
                ('U', 'H', 'H', 'U', 'H'),
                ('H', 'H', 'H', 'H', 'H'),
            )
        },

        {
            "police": 2,
            "medics": 1,
            "map": (
                ('U', 'H', 'S', 'H', 'S', 'H'),
                ('H', 'U', 'H', 'S', 'H', 'U'),
                ('U', 'H', 'H', 'U', 'H', 'I'),
                ('H', 'H', 'U', 'H', 'H', 'H'),
                ('H', 'U', 'S', 'H', 'Q', 'H'),
            )
        },

        {
            "police": 1,
            "medics": 1,
            "map": (
                ('U', 'H', 'H', 'S', 'H'),
                ('U', 'U', 'U', 'H', 'U'),
                ('H', 'S', 'Q', 'H', 'S'),
                ('H', 'U', 'H', 'S', 'U'),
            )
        },

        {
            "police": 1,
            "medics": 1,
            "map": (
                ('H', 'S', 'S', 'H'),
                ('S', 'H', 'H', 'S'),
                ('U', 'U', 'H', 'U'),
                ('H', 'H', 'H', 'H'),
                ('H', 'H', 'H', 'H'),
            ),
        },

        {
            "police": 1,
            "medics": 1,
            "map": (
                ('H', 'H', 'U', 'H', 'H'),
                ('S', 'H', 'U', 'H', 'H'),
                ('H', 'H', 'U', 'H', 'H'),
                ('U', 'U', 'U', 'H', 'Q'),
                ('H', 'H', 'H', 'H', 'H'),
                ('H', 'H', 'H', 'H', 'H'),
                ('H', 'I', 'H', 'H', 'H'),
                ('H', 'H', 'H', 'Q', 'H'),
                ('H', 'H', 'H', 'H', 'H'),
            )
        },

        {
            "police": 1,
            "medics": 1,
            "map": (
                ('H', 'H', 'U', 'H', 'H'),
                ('S', 'H', 'H', 'H', 'H'),
                ('H', 'H', 'U', 'H', 'H'),
                ('U', 'U', 'U', 'H', 'Q'),
                ('H', 'H', 'H', 'H', 'H'),
                ('H', 'H', 'H', 'H', 'H'),
                ('H', 'I', 'H', 'H', 'H'),
                ('H', 'H', 'H', 'Q', 'H'),
                ('H', 'H', 'H', 'H', 'H'),
            )
        },

        {
            "police": 1,
            "medics": 1,
            "map": (
                ('H', 'S', 'H', 'H'),
                ('S', 'H', 'H', 'S'),
                ('U', 'I', 'H', 'U'),
                ('H', 'H', 'H', 'H'),
            )
        },

        {
            "police": 2,
            "medics": 1,
            "map": (
                ('S', 'H', 'H', 'S'),
                ('U', 'H', 'H', 'S'),
                ('U', 'U', 'H', 'U'),
                ('H', 'H', 'H', 'H'),
                ('I', 'H', 'H', 'S'),
            )
        },

        {
            "police": 1,
            "medics": 2,
            "map": (
                ('H', 'S', 'S', 'H'),
                ('S', 'H', 'H', 'S'),
                ('U', 'U', 'H', 'U'),
                ('H', 'H', 'H', 'H'),
                ('H', 'H', 'H', 'H'),
            )
        },

        {
            "police": 1,
            "medics": 1,
            "map": (
                ('H', 'S', 'S', 'H', 'H'),
                ('S', 'H', 'H', 'S', 'I'),
                ('U', 'U', 'H', 'U', 'Q'),
                ('H', 'H', 'H', 'H', 'H'),
                ('H', 'H', 'H', 'H', 'H'),
                ('H', 'Q', 'H', 'S', 'H'),
            )
        },

        {
            "police": 3,
            "medics": 1,
            "map": (
                ('H', 'S', 'S', 'H', 'H'),
                ('S', 'H', 'H', 'S', 'I'),
                ('U', 'U', 'H', 'U', 'Q'),
                ('H', 'H', 'H', 'H', 'H'),
                ('H', 'H', 'H', 'H', 'H'),
                ('H', 'Q', 'H', 'S', 'H'),
            )
        },

        {
            "police": 1,
            "medics": 2,
            "map": (
                ('H', 'S', 'S', 'H', 'H', 'H'),
                ('S', 'H', 'H', 'S', 'I', 'U'),
                ('U', 'U', 'H', 'U', 'Q', 'U'),
                ('H', 'H', 'H', 'H', 'H', 'S'),
                ('H', 'H', 'H', 'H', 'H', 'H'),
                ('H', 'Q', 'H', 'S', 'H', 'I'),
            )
        },

        {
            "police": 2,
            "medics": 2,
            "map": (
                ('H', 'S', 'I', 'H', 'H', 'H'),
                ('S', 'H', 'H', 'S', 'I', 'U'),
                ('U', 'H', 'H', 'U', 'S', 'U'),
                ('H', 'S', 'H', 'H', 'H', 'S'),
                ('H', 'H', 'H', 'H', 'H', 'H'),
                ('H', 'Q', 'H', 'S', 'H', 'I'),
            )
        },

    ]

    # problems = problems[-1:]
    # solve_problems(problems)
    # find_optimal_weights(problems, 100)
    weights_list = []
    with open('results/done') as f:
        for i, line in enumerate(f):
            weights_list.append([float(val) for val in line.split('-')[0].split(',')])

    for i, weights in enumerate(weights_list):
        print(i, weights)
        # final_weights = np.round(weights, 5)
        # print(*final_weights, sep=', ')
        # print(np.linalg.norm(final_weights - weights))
        solve_problems(problems, weights)
        print('\n\n')


if __name__ == '__main__':
    main()
