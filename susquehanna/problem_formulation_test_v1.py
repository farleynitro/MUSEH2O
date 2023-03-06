from susquehanna_model import SusquehannaModel
from platypus import NSGAII, Problem, Real
from scipy.spatial.distance import pdist
import math
from math import dist
import numpy as np

class PriorityGiniProblem(Problem):
    '''
    According to the explanation given in the thesis, this is the Priority-based Equity objective formulation. The
    goal is to minimize the distance between the ratio of allocation and demand of the objectives. Moreover, the
    objectives of the case-study are optimized.

    Input:

    Problem: type Platypus.Problem

    Output:

    solution: type dictionary
    '''

    def __init__(self, n_decision_vars, n_objectives,
                n_years, rbf):
        super(PriorityGiniProblem, self).__init__(n_decision_vars, n_objectives)

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
        self.directions[6] = Problem.MINIMIZE  # equity

    @staticmethod
    def gini_coefficient(x_input):
        # x_array = PriorityGiniProblem.array_results(x_input)
        numerator = 0
        for i in range(len(x_input)):
            for j in range(len(x_input)):
                if i != j:
                    numerator += abs(x_input[i] - x_input[j])
                else:
                    pass

        denominator = 2*pow(len(x_input),2)*np.average(x_input) #(sum(x_input)/len(x_input))
        # print("denominator", denominator)
        # print("numerator", numerator)

        gini_coeff = numerator/denominator
        # print("da ginz", gini_coeff)
        return gini_coeff

    def evaluate(self, solution):
        x = solution.variables[:]
        self.function = self.susquehanna_river.evaluate
        # print("printing the function")
        # print(self.function)
        y = self.function(x)
        y = list(y)
        # print("\n", y[-5:])

        objectives_reliability = y[-5:]

        for i in range(len(y)):
            if i != 0: #ignoring hydropower objective for now since the objective is defined differently
                gini_coeff = PriorityGiniProblem.gini_coefficient(objectives_reliability)
            else:
                pass

        y.append(gini_coeff)
        # self.add_objective(euclidean_distance, name = 'equity')

        solution.objectives[:] = y

        #egalitarian_aggregated except hydropower objective
        # apply direction of optimization to each objective

        solution.objectives[:] = [solution.objectives[i] * self.directions[i] for i in range(len(solution.objectives))]
