from susquehanna_model import SusquehannaModel
from platypus import NSGAII, Problem, Real
from scipy.spatial.distance import pdist
import math
from math import dist
import numpy as np

class PriorityProblem(Problem):
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
        super(PriorityProblem, self).__init__(n_decision_vars, n_objectives)

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

        #HELP, I NEED TO INCLUDE EQUITY WITHOUT OPTIMIZING OVER IT

        # self.directions[6] = Problem.INFO  # equity

    @staticmethod
    def array_results(x_input):
        arrays = []
        for i in x_input:
            new_array = [i]
            arrays.append(new_array)
        # print("printing the arrays", arrays)
        # print("this is x_input", x_input)
        return arrays

    @staticmethod
    def euclidean_distance_singular(x1, x2):
        if len(x1) != len(x2):
            raise ValueError("Both points must be of same length")

        squared_distance = 0
        for i in range(len(x1)):
            squared_distance += (x1[i] - x2[i]) ** 2
        distance = math.sqrt(squared_distance)

        return distance

    def euclidean_distance_multiple(x_input):
        total_distance = 0
        x_array = PriorityProblem.array_results(x_input)
        for i in range(len(x_array)):
            for j in range(len(x_array)):
                # print("x_array[i]", x_array[i])
                total_distance += PriorityProblem.euclidean_distance_singular(x_array[i], x_array[j])
                # print("total_distance", total_distance)
        return total_distance

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
                euclidean_distance = PriorityProblem.euclidean_distance_multiple(objectives_reliability)
            else:
                pass

        #HELP

        print("\n", euclidean_distance)
        y.append(euclidean_distance)
        # self.add_objective(euclidean_distance, name = 'equity')

        solution.objectives[:] = y

        #egalitarian_aggregated except hydropower objective
        # apply direction of optimization to each objective

        solution.objectives[:] = [solution.objectives[i] * self.directions[i] for i in range(len(solution.objectives))]

