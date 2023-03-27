from susquehanna_model import SusquehannaModel
from platypus import Problem
import numpy as np

class SufficientarianPrinciple(Problem):
    '''
    According to the explanation given in the thesis, this is the Priority-based Equity objective formulation. The
    goal is to minimize the distance between the ratio of allocation and demand of the objectives, also known as the reliability.
    Moreover, the objectives of the case-study are optimized.

    Note that we calculate the distance between objectives inside the model, and subsequently, results are optimized
    once this function is called.

    Input:

    Problem: type Platypus.Problem

    Output:

    solution: type dictionary
    '''

    def __init__(self, n_decision_vars, n_objectives,
                n_years, rbf):
        super(SufficientarianPrinciple, self).__init__(n_decision_vars, n_objectives)

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
        self.directions[6] = Problem.MAXIMIZE  # sufficientarian principle

    def threshold_distance(x_input):
        # As defined by Jafino et al. (2022)

        # 1 = j_hyd, 2 = j_atom, 3 = j_balt, 4 = j_ches, 5 = j_env, 6 = j_rec
        # x_distances = np.array(x_input.size)
        threshold_minimum_flow = [39.23, 0.632, 1, 1, 0.1068, 0]
        threshold_baseline_policy = [39.30, 0.633, 1, 1, 0.1058, 0]
        thresholds_SBRC = [60, 0.9, 0.85, 0.9, 0.1]

        # make a choice out of the thresholds to calculate the distance
        thresholds = threshold_minimum_flow

        x_distances = x_input - thresholds
        x_distances_aggregated = x_distances.sum()

        return x_distances_aggregated

    def evaluate(self, solution):
        x = solution.variables[:]
        self.function = self.susquehanna_river.evaluate
        # print("printing the function")
        # print(self.function)
        y = self.function(x)
        y = list(y)


        index_nums = [0, 1, 2, 3, 4, 5]
        solution_set = [y[var] for var in index_nums]

        sufficientarian_obj = SufficientarianPrinciple.minimize_threshold_distance(solution_set)
        # print(solution_set)
        # self.add_objective(euclidean_distance, name = 'equity')
        solution_set.append(sufficientarian_obj)
        solution.objectives[:] = solution_set

        #egalitarian_aggregated except hydropower objective
        # apply direction of optimization to each objective

        solution.objectives[:] = [solution.objectives[i] * self.directions[i] for i in range(len(solution.objectives))]

class RawlsianDifferencePrinciple(Problem):
    '''
    According to the explanation given in the thesis, this is the Priority-based Equity objective formulation. The
    goal is to minimize the distance between the ratio of allocation and demand of the objectives, also known as the reliability.
    Moreover, the objectives of the case-study are optimized.

    Note that we calculate the distance between objectives inside the model, and subsequently, results are optimized
    once this function is called.

    Input:

    Problem: type Platypus.Problem

    Output:

    solution: type dictionary
    '''

    def __init__(self, n_decision_vars, n_objectives,
                n_years, rbf):
        super(RawlsianDifferencePrinciple, self).__init__(n_decision_vars, n_objectives)

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
        self.directions[6] = Problem.MAXIMIZE  # sufficientarian principle

    def marginalized_objective(x_input):
        # 1 = j_hyd, 2 = j_atom, 3 = j_balt, 4 = j_ches, 5 = j_env, 6 = j_rec
        # x_distances = np.array(x_input.size)
        array_input = np.array(x_input)
        j_min = np.argmin(array_input)
        return j_min

    def evaluate(self, solution):
        x = solution.variables[:]
        self.function = self.susquehanna_river.evaluate
        # print("printing the function")
        # print(self.function)
        y = self.function(x)
        y = list(y)


        index_nums = [1, 2, 3, 4, 5, 8]
        solution_set = [y[var] for var in index_nums]

        rawlsian_obj = RawlsianDifferencePrinciple.minimize_threshold_distance(solution_set)

        # print(solution_set)
        # self.add_objective(euclidean_distance, name = 'equity')

        solution_set.append(rawlsian_obj)
        solution.objectives[:] = solution_set

        #egalitarian_aggregated except hydropower objective
        # apply direction of optimization to each objective

        solution.objectives[:] = [solution.objectives[i] * self.directions[i] for i in range(len(solution.objectives))]
