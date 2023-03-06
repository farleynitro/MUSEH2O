from susquehanna_model import SusquehannaModel
from platypus import NSGAII, Problem, Real
from scipy.spatial.distance import pdist
import math
from math import dist
import numpy as np


class OriginalProblem(Problem):
    def __init__(self,
                 n_decision_vars,
                 n_objectives,
                 n_years,
                 rbf):
        super(OriginalProblem, self).__init__(n_decision_vars,
                                              n_objectives)

        #initialize rbf
        self.types[:] = rbf.platypus_types

        #initialize model
        self.susquehanna_river = SusquehannaModel(108.5, 505.0, 5, n_years, rbf)
        self.susquehanna_river.set_log(False)

        # Set direction of optimization for each objective
        self.directions[0] = Problem.MAXIMIZE  # hydropower
        self.directions[1] = Problem.MAXIMIZE  # atomic power plant
        self.directions[2] = Problem.MAXIMIZE  # baltimore
        self.directions[3] = Problem.MAXIMIZE  # chester
        self.directions[4] = Problem.MINIMIZE  # environment
        self.directions[5] = Problem.MAXIMIZE  # recreation

    # Lower and Upper Bound for problem.types

    def evaluate(self, solution):
        x = solution.variables[:]

        self.function = self.susquehanna_river.evaluate

        y = self.function(x)

        # set objective values
        solution.objectives[:] = y

        # apply direction of optimization to each objective
        solution.objectives[:] = [solution.objectives[i] * self.directions[i] for i in range(len(self.directions))]
