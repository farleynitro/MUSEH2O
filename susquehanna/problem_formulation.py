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
        x = solution.variables

        self.function = self.susquehanna_river.evaluate

        y = self.function(x)

        # set objective values
        solution.objectives[:] = y

        # apply direction of optimization to each objective
        solution.objectives[:] = [solution.objectives[i] * self.directions[i] for i in range(len(self.directions))]

class UtilitarianProblem(Problem):
    def __init__(self,
                 n_decision_vars,
                 n_objectives,
                 n_years,
                 rbf):
        super(UtilitarianProblem, self).__init__(n_decision_vars,
                                                 n_objectives)

        #initialize rbf
        self.types[:] = rbf.platypus_types

        #initialize model
        self.susquehanna_river = SusquehannaModel(108.5, 505.0, 5, n_years, rbf)
        self.susquehanna_river.set_log(False)

        self.directions[0] = Problem.MAXIMIZE
        self.directions[1] = Problem.MINIMIZE

    def evaluate(self, solution):
        # super().evaluate(solution)

        x = solution.variables
        self.function = self.susquehanna_river.evaluate

        y = self.function(x)

        solution.objectives[:] = y
        # utilitarian_aggregated
        y_all_except_env = [y[0], y[1], y[2], y[3], y[5]]
        y_env = y[4]

        y_maximize_all_except_env = y[0] + y[1] + y[2] + y[3] + y[5]
        y_minimize_env = y_env

        # set objective values
        solution.objectives[0] = y_maximize_all_except_env/ len(y_all_except_env)
        solution.objectives[1] = y_minimize_env

        # apply direction of optimization to each objective
        solution.objectives[:] = [solution.objectives[0] * self.directions[0],
                                  solution.objectives[1] * self.directions[1]]

class EgalitarianProblem(Problem):
    def __init__(self,
             n_decision_vars,
             n_objectives,
             n_years,
             rbf):
        super(EgalitarianProblem, self).__init__(n_decision_vars,
                                                 n_objectives)

       #initialize rbf
        self.types[:] = rbf.platypus_types

        #initialize model
        self.susquehanna_river = SusquehannaModel(108.5, 505.0, 5, n_years, rbf)
        self.susquehanna_river.set_log(False)
        self.directions[:] = Problem.MINIMIZE

    def evaluate(self, solution):
        x = solution.variables
        self.function = self.susquehanna_river.evaluate

        y = self.function(x)
        j_hyd, j_atom, j_balt, j_ches, j_env, j_rec = y


        y_result = euclidean_distance(y)
        print(y_result)
        # y_egalitarian = math.dist(j_hyd, j_atom, j_balt, j_ches, j_env, j_rec)

        # utilitarian_aggregated

        y_minimize = [y_egalitarian]

        # set objective values
        solution.objectives[:] = [y_minimize]

        # apply direction of optimization to each objective
        solution.objectives[:] = [solution.objectives[:] * self.directions[:]]


@staticmethod
def euclidean_distance(x):
    x_array = np.asarray(x, axis=0)
    euclidean_distance_value = 0

    for i in range(x_array):
        if i != 0:
            euclidean_distance_value += math.sqrt((x_array[i]**2) - (x_array[i-1]**2))
        else:
            pass
    return euclidean_distance_value


# def formulation_possible(var):
#     possible = False
#     if type(var) != int:
#         print("Invalid input for problem formulation")
#     else:
#         print("Test is working")
#         possible = True
#     return possible


# def ObjectiveFormulation(formulation, problem, objective_formulation = None):
#     valid = formulation_possible(formulation)
#     problem = problem
#     if valid == True:
#         if formulation == 0:
#             objective_formulation = OriginalProblem()
#             print(objective_formulation)
#         elif formulation == 1:
#             objective_formulation = UtilitarianProblem()
#         elif formulation == 2:
#             objective_formulation = EgalitarianProblem()
#         else:
#             pass
#     return objective_formulation

