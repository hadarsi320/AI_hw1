import numpy as np
from random import shuffle
import pickle
from ex1 import *
from check import *
from search import *
from pprint import pprint  # TODO: delete unnecessary imports


class Tournament:

    def __init__(self, players, problems, n_rounds, timeout):
        self.tournament_id = 1
        self.players = players
        self.problems = problems
        self.timeout = timeout
        self.round = 0
        self.n_rounds = n_rounds
        self.n_problems = len(problems)

    def run(self):
        for i in range(self.n_rounds):
            print(f"Starting Round {i+1}")
            problems = [self.generate_problem(*problem) for problem in self.problems]
            results = [self.solve_round_problems(problems, player, player_num) for
                       player_num, player in enumerate(self.players)]
            for i, problem in enumerate(problems):
                pprint(problem)
                for result in results:
                    pprint(result[i])
            # self.players = self.generate_next_round_players(results)
            self.round += 1

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
            # print("GBFS ", result, '\n')
            # if result[2] != None:
            #     if result[0] != -3:
            #         solved = solved + 1
        print(results)
        return results

    def generate_next_round_players(self, results):

        return self.players

    def pickle_players(self):
        with open(f"players_round_{self.tournament_id}_{self.round}.pickle", 'wb') as f:
            pickle.dump(self.players, f)

    def load_players(self, tournament_id, round):
        with open(f"players_round_{self.tournament_id}_{round}.pickle", 'rb') as f:
            self.players = pickle.load(f)

    # @staticmethod
    # def generate_problem(size_param, police_param, medic_param, probabilities):
    #     problem = {}
    #     board_len, board_width = geometric(size_param, 2)
    #     problem['police'] = geometric(police_param, 1)[0]
    #     problem['medics'] = geometric(medic_param, 1)[0]
    #     map = choice(['U', 'H', 'S', 'Q', 'I'],
    #                  size=(board_len, board_width),
    #                  p=probabilities)
    #     problem['map'] = ex1.state_to_tuple(map.tolist())
    #     return problem

    @staticmethod
    def generate_problem(len, width, police, medics, sick, unpopulated, quarantined):
        problem = {
            'police': police,
            'medics': medics
        }
        map = ['S'] * sick + \
              ['U'] * unpopulated + \
              ['Q'] * quarantined + \
              ['H'] * (len * width - sick - unpopulated - quarantined)
        shuffle(map)
        map = np.array(map).reshape(len, width).tolist()
        problem['map'] = state_to_tuple(map)
        return problem


if __name__ == '__main__':
    # weights = [SICK_TOTAL, SICK_1, SICK_2, IMMUNE, QUARANTINED_1, QUARANTINED_2, ENDANGERED]
    players = [[1, 1, 1.5, -1, -0.5, -0.75, 1],
               [1, 0, 0, 0, 0, 0, 0]]
    # problem = [len, width, police, medics, sick, unpopulated, quarantined]
    problems = [[6, 6, 2, 2, 4, 8, 0],
                [6, 6, 3, 2, 6, 10, 0],
                [6, 6, 3, 3, 7, 20, 0],
                # [6, 6, 3, 3, 4, 8, 0]
                ]
    t = Tournament(players, problems, 5, 60)
    t.run()
    # pprint(problem)
    # solve_round_problems([problem], player, 1)