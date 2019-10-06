from copy import deepcopy, copy
from numpy import all, any

class Variable:

    def __init__(self, domain):
        self.domain = domain
        self.value = None

    def __str__(self):
        return str(self.value)

class Constraint:

    def __init__(self, predicate, bound_variables):
        self.predicate = predicate
        self.bound_variables = bound_variables

    def satisfied(self):
        return any([v.value is None for v in self.bound_variables]) or self.predicate(self.bound_variables)

class Problem:

    def __init__(self, variables, constraints):
        self.variables = variables
        self.constraints = constraints

    def get_variables_values(self):
        return list(map(lambda x: x.value, self.variables))

    def unassigned_variables(self):
        # TODO: heuristic
        for var in self.variables:
            if var.value is None:
                yield var


class Solver:

    def __init__(self, problem):
        self.problem = problem
        self.solutions = []

    def solve(self):
        if not self.solutions:
            # TODO: ac3 or some different preprocessing
            self._solve()

    def _solve(self):
        problem = self.problem
        unassigned_variables = list(problem.unassigned_variables())
        if len(unassigned_variables) == 0:
            self.solutions.append(deepcopy(problem.variables))
        else:
            var = unassigned_variables[0]
            for val in var.domain:
                var.value = val
                if all([c.satisfied() for c in problem.constraints]):
                    # TODO: forward checking
                    self._solve()
            var.value = None

    def get_solution_values(self):
        return list(map(lambda y: list(map(lambda x: x.value, y)), self.solutions))

def N_queen_problem_example():
        N = 8
        # find a way to place 8 queens on a chessboard
        def same_diagonal(i, j, v1, v2):
            if j < i:
                i, j == j, i
            if v1 == v2 + (j - i) or v1 == v2 - (j - i):
                pass
            return v1 == v2 + (j - i) or v1 == v2 - (j - i)

        def get_diagonal_call(i, j):
            return lambda vars: not same_diagonal(i, j, vars[0].value, vars[1].value)

        def visualise_queens(queens):
            for q in queens:
                print(q * 'X' + 'Q' + (N - q - 1) * 'X')
            print()

        variables = [Variable(list(range(N))) for _ in range(N)]
        constraints = []
        for i, v1 in enumerate(variables):
            for j, v2 in enumerate(variables):
                if i == j: continue
                # same row
                constraints.append(Constraint(lambda vars: vars[0].value != vars[1].value, [v1, v2]))
                # diagonal
                constraints.append(Constraint(get_diagonal_call(i, j), [v1, v2]))

        s = Solver(Problem(variables, constraints))
        s.solve()
        print(f'found {len(s.solutions)} solutions:')
        for v in s.get_solution_values():
            visualise_queens(v)

def main():
    N_queen_problem_example()


if __name__ == '__main__':
    main()
