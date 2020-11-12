import itertools

import search

ids = ["318792827", "321659187"]


class MedicalProblem(search.Problem):
    """This class implements a medical problem according to problem description file"""

    def __init__(self, initial, weights): # TODO delete weights
        """Don't forget to implement the goal test
        You should change the initial to your own representation.
        search.Problem.__init__(self, initial) creates the root node"""
        self.medics = initial['medics']
        self.police = initial['police']
        state_durations = {'U': 0, 'H': 0, 'S': 3, 'Q': 2, 'I': 0}
        initial_state = tuple([tuple([(value, state_durations[value]) for value in line])
                               for line in initial['map']])
        self.len = len(initial_state)
        self.width = len(initial_state[0])
        self.weights = weights
        search.Problem.__init__(self, initial_state)

    def actions(self, state):
        """Returns all the actions that can be executed in the given
        state. The result should be a tuple (or other iterable) of actions
        as defined in the problem description file"""
        sick = []
        healthy = []
        for i, line in enumerate(state):
            for j, val in enumerate(line):
                if val[0] == 'S':
                    sick.append(('quarantine', (i, j)))
                if val[0] == 'H':
                    healthy.append(('vaccinate', (i, j)))

        actions = [sick_perm + healthy_perm for sick_perm in itertools.combinations(sick, self.police)
                   for healthy_perm in itertools.combinations(healthy, self.medics)]
        return actions

    def result(self, state, actions):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        state = state_to_list(state)

        for action, (i, j) in actions:
            if action == 'quarantine':
                assert state[i][j][0] == 'S'
                state[i][j] = ('Q', 2)

            elif action == 'vaccinate':
                assert state[i][j][0] == 'H'
                state[i][j] = ('I', 0)

        for i, row in enumerate(state):
            for j, value in enumerate(row):
                if value[0] == 'S':
                    for k, l in self.neighbors(i, j):
                        if state[k][l][0] == 'H':
                            state[k][l] = ('S', 3)

        for i, row in enumerate(state):
            for j, (value, days) in enumerate(row):
                if value in ['S', 'Q']:
                    if days == 1:
                        state[i][j] = ('H', 0)
                    else:
                        state[i][j] = (value, days - 1)

        return state_to_tuple(state)

    def neighbors(self, i, j):
        return [val for val in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)] if self.in_board(*val)]

    def in_board(self, i, j):
        return 0 <= i < self.len and 0 <= j < self.width

    def goal_test(self, state):
        """ Given a state, checks if this is the goal state.
         Returns True if it is, False otherwise."""
        for row in state:
            for value, _ in row:
                if value == 'S':
                    return False
        return True

    def h(self, node: search.Node):
        """ This is the heuristic. It gets a node (not a state,
        state can be accessed via node.state)
        and returns a goal distance estimate"""
        h_score = 0
        state = node.state
        scores = [self.count_sick(state),
                     self.count_recovery(state, 1),
                     self.count_recovery(state, 2),
                     self.count_immune(state)
                     self.count_quarantined(state, 1),
                     self.count_quarantined(state, 2),
                     self.count_endangered(state)]
        for score, weight in zip(scores, self.weights):
            h_score += scores * weight
        return h_score

    def generic_count(self, state, counter_func):
        score = 0
        for i in self.len:
            for j in self.width:
                score += counter_func(i, j, state)
        return score

    def count_sick(self, state):
        return self.generic_count(state, lambda i, j, state: state[i][j][0] == 'S')

    def count_recovery(self, state, days):
        return self.generic_count(state, lambda i, j, state: state[i][j] == ('S', days))

    def count_immune(self, state):
        return self.generic_count(state, lambda i, j, state: state[i][j][0] == 'I')

    def count_quarantined(self, state, days):
        return self.generic_count(state, lambda i, j, state: state[i][j] == ('Q', days))

    def count_endangered(self, state):

        def is_endangered(i, j, state):
            if state[i][j][0] == 'H':
                for k, l in self.neighbors(i, j):
                    if state[k][l][0] == 'S':
                        return 1
            return 0

        return self.generic_count(state, is_endangered)

    """Feel free to add your own functions
    (-2, -2, None) means there was a timeout"""


def state_to_list(state):
    return [list(row) for row in state]


def state_to_tuple(state):
    return tuple(tuple(row) for row in state)


def create_medical_problem(game):
    return MedicalProblem(game)