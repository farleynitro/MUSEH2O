from susquehanna_model import SusquehannaModel
from platypus import NSGAII, Problem, Real
from scipy.spatial.distance import pdist
import math
from math import dist
import numpy as np


# class UtilitarianProblemTest1(Problem):
#     def __init__(self,
#                  n_decision_vars,
#                  n_objectives,
#                  n_years,
#                  rbf):
#         super(UtilitarianProblemTest1, self).__init__(n_decision_vars,
#                                                  n_objectives)
#
#         #initialize rbf
#         self.types[:] = rbf.platypus_types
#
#         #initialize model
#         self.susquehanna_river = SusquehannaModel(108.5, 505.0, 5, n_years, rbf)
#         self.susquehanna_river.set_log(False)
#
#         # Set direction of optimization for each objective
#         self.directions[0] = Problem.MAXIMIZE  # hydropower
#         self.directions[1] = Problem.MAXIMIZE  # atomic power plant
#         self.directions[2] = Problem.MAXIMIZE  # baltimore
#         self.directions[3] = Problem.MAXIMIZE  # chester
#         self.directions[4] = Problem.MINIMIZE  # environment
#         self.directions[5] = Problem.MAXIMIZE  # recreation
#         self.directions[6] = Problem.INFO # equity
#
#     def evaluate(self, solution):
#         # super().evaluate(solution)
#
#         x = solution.variables
#         self.function = self.susquehanna_river.evaluate
#
#         y = self.function(x)
#
#         @staticmethod
#         def array_results(x):
#             arrays = []
#             for i in x:
#                 new_array = [i]
#                 arrays.append(new_array)
#             return arrays
#
#         @staticmethod
#         def euclidean_distance_singular(x1, x2):
#             if len(x1) != len(x2):
#                 raise ValueError("Both points must be of same length")
#
#             squared_distance = 0
#             for i in range(len(x1)):
#                 squared_distance += (x1[i] - x2[i]) ** 2
#             distance = math.sqrt(squared_distance)
#
#             return distance
#
#         def euclidean_distance_multiple(x):
#             total_distance = 0
#             x_array = PriorityEquityProblem.array_results(x)
#             for i in range(len(x_array) - 1):
#                 total_distance += UtilitarianProblemTest1.euclidean_distance_singular(x_array[i], x_array[i + 1])
#             return total_distance
#
#         def evaluate(self, solution):
#             x = solution.variables
#             self.function = self.susquehanna_river.evaluate
#
#             y = self.function(x)
#             y = list(y)
#             solution.objectives[:] = y
#
#             for i in range(len(y)):
#                 if i != 0:  # ignoring hydropower objective for now since the objective is defined differently
#                     euclidean_distance = PriorityEquityProblem.euclidean_distance_multiple(y[:-5])
#                 else:
#                     pass
#
#             self.add_objective(euclidean_distance, name='equity')
#
#             # apply direction of optimization to each objective
#             solution.objectives[:] = [solution.objectives[i] * self.directions[i] for i in
#                                       range(len(solution.objectives))]
#
#         # solution.objectives[:] = y
#         # # utilitarian_aggregated
#         # y_all_except_env = [y[0], y[1], y[2], y[3], y[5]]
#         # y_env = y[4]
#         #
#         # y_maximize_all_except_env = y[0] + y[1] + y[2] + y[3] + y[5]
#         # y_minimize_env = y_env
#         #
#         # # set objective values
#         # solution.objectives[0] = y_maximize_all_except_env/ len(y_all_except_env)
#         # solution.objectives[1] = y_minimize_env
#         #
#         # # apply direction of optimization to each objective
#         # solution.objectives[:] = [solution.objectives[0] * self.directions[0],
#         #                           solution.objectives[1] * self.directions[1]]
#
#
# class UtilitarianProblemTest2(Problem):
#     def __init__(self,
#                  n_decision_vars,
#                  n_objectives,
#                  n_years,
#                  rbf):
#         super(UtilitarianProblemTest2, self).__init__(n_decision_vars,
#                                                  n_objectives)
#
#         #initialize rbf
#         self.types[:] = rbf.platypus_types
#
#         #initialize model
#         self.susquehanna_river = SusquehannaModel(108.5, 505.0, 5, n_years, rbf)
#         self.susquehanna_river.set_log(False)
#
#         # Set direction of optimization for each objective
#         self.directions[0] = Problem.MAXIMIZE  # hydropower
#         self.directions[1] = Problem.MAXIMIZE  # atomic power plant
#         self.directions[2] = Problem.MAXIMIZE  # baltimore
#         self.directions[3] = Problem.MAXIMIZE  # chester
#         self.directions[4] = Problem.MINIMIZE  # environment
#         self.directions[5] = Problem.MAXIMIZE  # recreation
#         self.directions[6] = Problem.INFO # equity
#
#     def evaluate(self, solution):
#         # super().evaluate(solution)
#
#         x = solution.variables
#         self.function = self.susquehanna_river.evaluate
#
#         y = self.function(x)
#
#         @staticmethod
#         def array_results(x):
#             arrays = []
#             for i in x:
#                 new_array = [i]
#                 arrays.append(new_array)
#             return arrays
#
#         @staticmethod
#         def euclidean_distance_singular(x1, x2):
#             if len(x1) != len(x2):
#                 raise ValueError("Both points must be of same length")
#
#             squared_distance = 0
#             for i in range(len(x1)):
#                 squared_distance += (x1[i] - x2[i]) ** 2
#             distance = math.sqrt(squared_distance)
#
#             return distance
#         def euclidean_distance_multiple(x):
#             total_distance = 0
#             x_array = UtilitarianProblemTest2.array_results(x)
#             for i in range(len(x_array) - 1):
#                 total_distance += UtilitarianProblemTest2.euclidean_distance_singular(x_array[i], x_array[i + 1])
#             return total_distance
#
#         def evaluate(self, solution):
#             x = solution.variables
#             self.function = self.susquehanna_river.evaluate
#
#             y = self.function(x)
#             y = list(y)
#
#             for i in range(len(y)):
#                 if i != 0:  # ignoring hydropower objective for now since the objective is defined differently
#                     euclidean_distance = UtilitarianProblemTest2.euclidean_distance_multiple(y[:-5])
#                 else:
#                     pass
#
#             # utilitarian_aggregated
#
#             y.append(euclidean_distance)
#
#             solution.objectives[:] = y
#
#
#             # apply direction of optimization to each objective
#             solution.objectives[:] = [solution.objectives[i] * self.directions[i] for i in
#                                       range(len(solution.objectives))]

# class SufficientarianProblem(Problem):
    # def __init__(self,
    #          n_decision_vars,
    #          n_objectives,
    #          n_years,
    #          rbf):
    #     super(SufficientarianProblem, self).__init__(n_decision_vars,
    #                                              n_objectives)
    #
    #    #initialize rbf
    #     self.types[:] = rbf.platypus_types
    #
    #     #initialize model
    #     self.susquehanna_river = SusquehannaModel(108.5, 505.0, 5, n_years, rbf)
    #     self.susquehanna_river.set_log(False)
    #     self.directions[:] = Problem.MINIMIZE


# class PrioritarianProblem(Problem):
#     def __init__(self,
#              n_decision_vars,
#              n_objectives,
#              n_years,
#              rbf):
#         super(EgalitarianProblem, self).__init__(n_decision_vars,
#                                                  n_objectives)
#
#        #initialize rbf
#         self.types[:] = rbf.platypus_types
#
#         #initialize model
#         self.susquehanna_river = SusquehannaModel(108.5, 505.0, 5, n_years, rbf)
#         self.susquehanna_river.set_log(False)
#         self.directions[:] = Problem.MINIMIZE
