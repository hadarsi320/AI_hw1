from numpy.random import geometric, choice
import ex1
import pickle
from check import *
from search import *


class Tournament:

    def __init__(self, players, timeout, n_rounds):
        self.players = players
        self.timeout = timeout
        self.n_rounds = n_rounds

    def run(self):
        for i in range(self.n_rounds):
            print(f"Starting Round {i}")
            problems = [self.generate_problem(params*) for i in range(n_problems)]
            results = [self.solve_round_problems(problems, player) for player in self.players]
            self.players = self.generate_next_round_players(results)

    def solve_round_problems(self, problems, player, player_num):
        print(f"Solving for player {player_num}:")
        print(f"\t{player}")
        results = []
        for problem in problems:
            try:
                p = ex1.create_medical_problem(problem, player)
            except Exception as e:
                print("Error creating problem: ", e)
                return None
            timeout = 60
            result = check_problem(p, (lambda p: search.best_first_graph_search(p, p.h)), self.timeout)
            results.append(result)
            # (len(solution), t2 - t1, solution)
            print("GBFS ", result, '\n')
            # if result[2] != None:
            #     if result[0] != -3:
            #         solved = solved + 1
        return results

    def generate_next_round_players(self, results):
        return self.players

    @staticmethod
    def generate_problem(size_param, police_param, medic_param, probabilities):
        problem = {}
        board_len, board_width = geometric(size_param, 2)
        problem['police'] = geometric(police_param, 1)[0]
        problem['medics'] = geometric(medic_param, 1)[0]
        map = choice(['U', 'H', 'S', 'Q', 'I'],
                     size=(board_len, board_width),
                     p=probabilities)
        problem['map'] = ex1.state_to_tuple(map.tolist())
        return problem
