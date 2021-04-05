import itertools

import search

ids = ["318792827", "321659187"]

NUM_MEASURES = 8
SICK_TOTAL = 0
SICK_1 = 1
SICK_2 = 2
SICK_3 = 3
IMMUNE = 4
QUARANTINED_1 = 5
QUARANTINED_2 = 6
ENDANGERED = 7

Q_action = 'quarantine'
V_action = 'vaccinate'



class MedicalProblem(search.Problem):
    """This class implements a medical problem according to problem description file"""

    def __init__(self, initial):
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
        search.Problem.__init__(self, initial_state)

    def actions(self, state):
        """Returns all the actions that can be executed in the given
        state. The result should be a tuple (or other iterable) of actions
        as defined in the problem description file"""
        sick = []
        healthy = []
        for i, line in enumerate(state):
            for j, (value, _) in enumerate(line):
                if value == 'S':
                    sick.append((Q_action, (i, j)))
                elif value == 'H':
                    healthy.append((V_action, (i, j)))

        sick_permutations = list(itertools.combinations(sick, min(self.police, len(sick))))
        healthy_permutations = list(itertools.combinations(healthy, min(self.medics, len(healthy))))
        actions = [sick_perm + healthy_perm
                   for sick_perm in sick_permutations
                   for healthy_perm in healthy_permutations]
        return actions

    def result(self, state, actions):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        state = state_to_list(state)

        for action, (i, j) in actions:
            if action == Q_action:
                state[i][j] = ('Q', 3)

            elif action == V_action:
                state[i][j] = ('I', 0)

        infect = []
        for i, row in enumerate(state):
            for j, value in enumerate(row):
                if value[0] == 'S':
                    for k, l in self.get_neighbors(i, j):
                        if state[k][l][0] == 'H':
                            infect.append((k, l))

        for i, j in infect:
            state[i][j] = ('S', 4)  # 4 since this is going to be demoted immediately

        for i, row in enumerate(state):
            for j, (value, days) in enumerate(row):
                if value in ['S', 'Q']:
                    if days == 1:
                        state[i][j] = ('H', 0)
                    else:
                        state[i][j] = (value, days - 1)

        return state_to_tuple(state)

    def get_neighbors(self, i, j):
        return [val for val in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)] if self.in_board(*val)]

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

        for i, line in enumerate(state):
            for j, (value, day) in enumerate(line):
                if value == 'S':
                    h_score += day
        return h_score

    def count_measures(self, state):
        counts = [0] * NUM_MEASURES
        for i in range(self.len):
            for j in range(self.width):
                value, day = state[i][j]

                if value == 'H':
                    if self.is_endangered(state, i, j):
                        counts[ENDANGERED] += 1
                elif value == 'U':
                    continue
                elif value == 'S':
                    counts[SICK_TOTAL] += 1
                    if day == 1:
                        counts[SICK_1] += 1
                    elif day == 2:
                        counts[SICK_2] += 1
                    elif day == 3:
                        counts[SICK_3] += 1
                elif value == 'I':
                    counts[IMMUNE] += 1
                elif value == 'Q':
                    if day == 1:
                        counts[QUARANTINED_1] += 1
                    elif day == 2:
                        counts[QUARANTINED_2] += 1
        return counts

    @staticmethod
    def is_healthy(val):
        return val[0] == 'H'

    @staticmethod
    def is_sick(val):
        return val[0] == 'S'

    @staticmethod
    def is_immune(val):
        return val[0] == 'I'

    @staticmethod
    def is_quarantined(val):
        return val[0] == 'Q'

    def is_endangered(self, state, i, j):
        if state[i][j][0] == 'H':
            for k, l in self.get_neighbors(i, j):
                if state[k][l][0] == 'S':
                    return True
        return False


def state_to_list(state):
    return [list(row) for row in state]


def state_to_tuple(state):
    return tuple(tuple(row) for row in state)


def create_medical_problem(game):
    return MedicalProblem(game)
