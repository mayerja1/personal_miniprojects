from copy import deepcopy
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

    def satisfied(self, variables):
        return any([v.value is None for v in self.bound_variables]) or self.predicate(variables)

class Problem:

    def __init__(self, variables, constraints):
        self.variables = variables
        self.constraints = constraints

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
        for var in problem.unassigned_variables():
            for val in var.domain:
                var.value = val
                if all([c.satisfied(problem.variables) for c in problem.constraints]):
                    # TODO: forward checking
                    self._solve()
            var.value = None
