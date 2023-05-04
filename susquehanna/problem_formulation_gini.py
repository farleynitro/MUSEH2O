from susquehanna_model import SusquehannaModel
from platypus import Problem
import numpy as np
import pandas as pd

class CombinedTraditionalGiniMean(Problem):
    '''
    According to the explanation given in the thesis, this is the Proportionality-based Equity objective formulation. The
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
        super(CombinedTraditionalGiniMean, self).__init__(n_decision_vars, n_objectives)

        # initialize rbf
        self.types[:] = rbf.platypus_types

        # initialize storing results
        # self.list_gini_std = []
        # self.list_gini_mean = []
        # self.list_eucli_std = []
        # self.list_eucli_mean = []
        # self.list_j_hydro_reliability = []
        # self.list_gini_std_monthly = []
        # self.list_eucli_std_monthly = []

        # initialize model
        self.susquehanna_river = SusquehannaModel(108.5, 505.0, 5, n_years, rbf)
        self.susquehanna_river.set_log(False)

        # Set direction of optimization for each objective
        self.directions[0] = Problem.MAXIMIZE  # hydropower
        self.directions[1] = Problem.MAXIMIZE  # atomic power plant
        self.directions[2] = Problem.MAXIMIZE  # baltimore
        self.directions[3] = Problem.MAXIMIZE  # chester
        self.directions[4] = Problem.MINIMIZE  # environment
        self.directions[5] = Problem.MAXIMIZE  # recreation
        self.directions[6] = Problem.MINIMIZE  # equity reliability

    def evaluate(self, solution):
        x = solution.variables[:]
        self.function = self.susquehanna_river.evaluate

        y = self.function(x)

        # other results in the model
        # self.list_gini_std.append(self.susquehanna_river.gini_monthly_std_coeff)
        # self.list_gini_mean.append(self.susquehanna_river.gini_yearly_mean_coeff)
        # self.list_eucli_std.append(self.susquehanna_river.eucli_monthly_std_coeff)
        # self.list_eucli_mean.append(self.susquehanna_river.eucli_yearly_mean_coeff)
        # self.list_j_hydro_reliability.append(self.susquehanna_river.j_hydro_reliability_yearly_mean)
        # self.list_gini_std_monthly.append(self.susquehanna_river.gini_monthly)
        # self.list_eucli_std_monthly.append(self.susquehanna_river.eucli_monthly)


        # df_results = pd.concat([
        #     pd.Series(y[0], dtype='float64'),
        #     pd.Series(y[1], dtype='float64'),
        #     pd.Series(y[2], dtype='float64'),
        #     pd.Series(y[3], dtype='float64'),
        #     pd.Series(y[4], dtype='float64'),
        #     pd.Series(y[5], dtype='float64'),
        #     pd.Series(self.susquehanna_river.gini_monthly_std_coeff),
        #     pd.Series(self.susquehanna_river.gini_yearly_mean_coeff),
        #     pd.Series(self.susquehanna_river.eucli_monthly_std_coeff),
        #     pd.Series(self.susquehanna_river.eucli_yearly_mean_coeff),
        #     pd.Series(self.susquehanna_river.gini_monthly),
        #     pd.Series(self.susquehanna_river.eucli_monthly),
        #     pd.Series(self.susquehanna_river.j_hydro_reliability_yearly_mean)
        # ], axis=1)
        #
        # df_results.to_csv("gini_mean_results.csv", mode='a', index=False, header=False)

        y = list(y)

        # gini mean is index number 7
        index_nums_mean = [0, 1, 2, 3, 4, 5, 7]

        # specify here which formulation you are using

        index_nums = index_nums_mean

        # specify solution set which will be added to objectives

        solution_set = [y[var] for var in index_nums]

        # self.add_objective(euclidean_distance, name = 'equity')
        solution.objectives[:] = solution_set

        # apply direction of optimization to each objective

        solution.objectives[:] = [solution.objectives[i] * self.directions[i] for i in range(len(solution.objectives))]



class CombinedTraditionalGiniStd(Problem):
    '''
    According to the explanation given in the thesis, this is the Proportionality-based Equity objective formulation. The
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
        super(CombinedTraditionalGiniStd, self).__init__(n_decision_vars, n_objectives)

        # initialize rbf
        self.types[:] = rbf.platypus_types

        # initialize storing results
        # self.list_gini_std = []
        # self.list_gini_mean = []
        # self.list_eucli_std = []
        # self.list_eucli_mean = []
        # self.list_j_hydro_reliability = []
        # self.list_gini_std_monthly = []
        # self.list_eucli_std_monthly = []

        # initialize model
        self.susquehanna_river = SusquehannaModel(108.5, 505.0, 5, n_years, rbf)
        self.susquehanna_river.set_log(False)

        # Set direction of optimization for each objective
        self.directions[0] = Problem.MAXIMIZE  # hydropower
        self.directions[1] = Problem.MAXIMIZE  # atomic power plant
        self.directions[2] = Problem.MAXIMIZE  # baltimore
        self.directions[3] = Problem.MAXIMIZE  # chester
        self.directions[4] = Problem.MINIMIZE  # environment
        self.directions[5] = Problem.MAXIMIZE  # recreation
        self.directions[6] = Problem.MINIMIZE  # equity reliability

    def evaluate(self, solution):
        x = solution.variables[:]
        self.function = self.susquehanna_river.evaluate

        y = self.function(x)

        # other results in the model
        # self.list_gini_std.append(self.susquehanna_river.gini_monthly_std_coeff)
        # self.list_gini_mean.append(self.susquehanna_river.gini_yearly_mean_coeff)
        # self.list_eucli_std.append(self.susquehanna_river.eucli_monthly_std_coeff)
        # self.list_eucli_mean.append(self.susquehanna_river.eucli_yearly_mean_coeff)
        # self.list_j_hydro_reliability.append(self.susquehanna_river.j_hydro_reliability_yearly_mean)
        # self.list_gini_std_monthly.append(self.susquehanna_river.gini_monthly)
        # self.list_eucli_std_monthly.append(self.susquehanna_river.eucli_monthly)


        # df_results = pd.concat([
        #     pd.Series(y[0], dtype='float64'),
        #     pd.Series(y[1], dtype='float64'),
        #     pd.Series(y[2], dtype='float64'),
        #     pd.Series(y[3], dtype='float64'),
        #     pd.Series(y[4], dtype='float64'),
        #     pd.Series(y[5], dtype='float64'),
        #     pd.Series(self.susquehanna_river.gini_monthly_std_coeff),
        #     pd.Series(self.susquehanna_river.gini_yearly_mean_coeff),
        #     pd.Series(self.susquehanna_river.eucli_monthly_std_coeff),
        #     pd.Series(self.susquehanna_river.eucli_yearly_mean_coeff),
        #     pd.Series(self.susquehanna_river.gini_monthly),
        #     pd.Series(self.susquehanna_river.eucli_monthly),
        #     pd.Series(self.susquehanna_river.j_hydro_reliability_yearly_mean)
        # ], axis=1)
        #
        # df_results.to_csv("gini_std_results.csv", mode='a', index=False, header=False)

        y = list(y)
        # gini standard deviation is index number 9
        index_nums_std = [0, 1, 2, 3, 4, 5, 9]

        # specify here which formulation you are using

        index_nums = index_nums_std

        # specify solution set which will be added to objectives

        solution_set = [y[var] for var in index_nums]
        # self.add_objective(euclidean_distance, name = 'equity')
        solution.objectives[:] = solution_set

        # apply direction of optimization to each objective

        solution.objectives[:] = [solution.objectives[i] * self.directions[i] for i in range(len(solution.objectives))]

class CombinedTraditionalGiniRatioStdMean(Problem):
    '''
    According to the explanation given in the thesis, this is the Proportionality-based Equity objective formulation. The
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
        super(CombinedTraditionalGiniRatioStdMean, self).__init__(n_decision_vars, n_objectives)

        # initialize rbf
        self.types[:] = rbf.platypus_types

        # initialize storing results
        # self.list_gini_std = []
        # self.list_gini_mean = []
        # self.list_eucli_std = []
        # self.list_eucli_mean = []
        # self.list_j_hydro_reliability = []
        # self.list_gini_std_monthly = []
        # self.list_eucli_std_monthly = []

        # initialize model
        self.susquehanna_river = SusquehannaModel(108.5, 505.0, 5, n_years, rbf)
        self.susquehanna_river.set_log(False)

        # Set direction of optimization for each objective
        self.directions[0] = Problem.MAXIMIZE  # hydropower
        self.directions[1] = Problem.MAXIMIZE  # atomic power plant
        self.directions[2] = Problem.MAXIMIZE  # baltimore
        self.directions[3] = Problem.MAXIMIZE  # chester
        self.directions[4] = Problem.MINIMIZE  # environment
        self.directions[5] = Problem.MAXIMIZE  # recreation
        self.directions[6] = Problem.MINIMIZE  # equity reliability

    def evaluate(self, solution):
        x = solution.variables[:]
        self.function = self.susquehanna_river.evaluate

        y = self.function(x)

        # other results in the model
        # self.list_gini_std.append(self.susquehanna_river.gini_monthly_std_coeff)
        # self.list_gini_mean.append(self.susquehanna_river.gini_yearly_mean_coeff)
        # self.list_eucli_std.append(self.susquehanna_river.eucli_monthly_std_coeff)
        # self.list_eucli_mean.append(self.susquehanna_river.eucli_yearly_mean_coeff)
        # self.list_j_hydro_reliability.append(self.susquehanna_river.j_hydro_reliability_yearly_mean)
        # self.list_gini_std_monthly.append(self.susquehanna_river.gini_monthly)
        # self.list_eucli_std_monthly.append(self.susquehanna_river.eucli_monthly)

        # df_results = pd.concat([
        #     pd.Series(y[0], dtype='float64'),
        #     pd.Series(y[1], dtype='float64'),
        #     pd.Series(y[2], dtype='float64'),
        #     pd.Series(y[3], dtype='float64'),
        #     pd.Series(y[4], dtype='float64'),
        #     pd.Series(y[5], dtype='float64'),
        #     pd.Series(self.susquehanna_river.gini_monthly_std_coeff),
        #     pd.Series(self.susquehanna_river.gini_yearly_mean_coeff),
        #     pd.Series(self.susquehanna_river.eucli_monthly_std_coeff),
        #     pd.Series(self.susquehanna_river.eucli_yearly_mean_coeff),
        #     pd.Series(self.susquehanna_river.gini_monthly),
        #     pd.Series(self.susquehanna_river.eucli_monthly),
        #     pd.Series(self.susquehanna_river.j_hydro_reliability_yearly_mean)
        # ], axis=1)
        #
        # df_results.to_csv("gini_std_results.csv", mode='a', index=False, header=False)

        y = list(y)
        # gini ratio is index number 11
        index_nums_std = [0, 1, 2, 3, 4, 5, 11]

        # specify here which formulation you are using

        index_nums = index_nums_std

        # specify solution set which will be added to objectives

        solution_set = [y[var] for var in index_nums]
        # self.add_objective(euclidean_distance, name = 'equity')
        solution.objectives[:] = solution_set

        # apply direction of optimization to each objective

        solution.objectives[:] = [solution.objectives[i] * self.directions[i] for i in range(len(solution.objectives))]























# class CombinedPrincipleGiniPostOptimization(Problem):
#     '''
#     According to the explanation given in the thesis, this is the Priority-based Equity objective formulation. The
#     goal is to minimize the distance between the ratio of allocation and demand of the objectives. Moreover, the
#     objectives of the case-study are optimized.
#
#     Note that we calculate the distance between the objectives after running the model, and subsequently, results are optimized.
#
#     Input:
#
#     Problem: type Platypus.Problem
#
#     Output:
#
#     solution: type dictionary
#     '''
#
#     def __init__(self, n_decision_vars, n_objectives,
#                 n_years, rbf):
#         super(CombinedPrincipleGiniPostOptimization, self).__init__(n_decision_vars, n_objectives)
#
#        #initialize rbf
#         self.types[:] = rbf.platypus_types
#
#         #initialize model
#         self.susquehanna_river = SusquehannaModel(108.5, 505.0, 5, n_years, rbf)
#         self.susquehanna_river.set_log(False)
#         # Set direction of optimization for each objective
#         self.directions[0] = Problem.MAXIMIZE  # hydropower
#         self.directions[1] = Problem.MAXIMIZE  # atomic power plant
#         self.directions[2] = Problem.MAXIMIZE  # baltimore
#         self.directions[3] = Problem.MAXIMIZE  # chester
#         self.directions[4] = Problem.MINIMIZE  # environment
#         self.directions[5] = Problem.MAXIMIZE  # recreation
#         self.directions[6] = Problem.MINIMIZE  # equity
#
#     @staticmethod
#     def gini_coefficient(x_input):
#         # x_array = PriorityGiniProblem.array_results(x_input)
#         numerator = 0
#         for i in range(len(x_input)):
#             for j in range(len(x_input)):
#                 if i != j:
#                     # divide by 2 to remove double counting
#                     numerator += abs(x_input[i] - x_input[j]) / 2
#                 else:
#                     pass
#
#         denominator = 2 * pow(len(x_input), 2) * np.average(x_input)  # (sum(x_input)/len(x_input))
#         # print("denominator", denominator)
#         # print("numerator", numerator)
#
#         gini_coeff = numerator / denominator
#         # print("da ginz", gini_coeff)
#         return gini_coeff
#     def evaluate(self, solution):
#         x = solution.variables[:]
#         self.function = self.susquehanna_river.evaluate
#         # print("printing the function")
#         # print(self.function)
#         y = self.function(x)
#         y = list(y)
#
#         # objectives_reliability = y[0:6]
#
#         index_nums = [1, 2, 3, 4, 5, 8]
#         objectives_reliability = [y[val] for val in index_nums]
#
#
#         # for i in range(len(objectives_reliability)):
#             # if i != 0: #ignoring hydropower objective for now since the objective is defined differently
#         gini_distance = EquityProblemGiniOutsideReliability.gini_coefficient(objectives_reliability)
#         # print("gini", gini_distance)
#             # else:
#             #     pass
#
#         # print("\n", euclidean_distance)
#
#         solution_set = y[0:6]
#         solution_set.append(gini_distance)
#         # self.add_objective(euclidean_distance, name = 'equity')
#
#         solution.objectives[:] = solution_set
#
#         #egalitarian_aggregated except hydropower objective
#         # apply direction of optimization to each objective
#
#         solution.objectives[:] = [solution.objectives[i] * self.directions[i] for i in range(len(solution.objectives))]


########################################## INSIDE OBJECTIVE FORMULATIONS #################################################################

# class EquityProblemGiniInsideReliabilityAllocation(Problem):
#     '''
#     According to the explanation given in the thesis, this is the Equity objective formulation. The
#     goal is to minimize the distance between the ratio of allocation and demand of the objectives, and the distance
#     between the ratio of allocation (without considering the demand of objectives). Moreover, the
#     objectives of the case-study are optimized.
#
#     Note that we calculate the distance between objectives inside the model, and subsequently, results are optimized
#     once this function is called.
#
#     Input:
#
#     Problem: type Platypus.Problem
#
#     Output:
#
#     solution: type dictionary
#     '''
#
#     def __init__(self, n_decision_vars, n_objectives,
#                 n_years, rbf):
#         super(EquityProblemGiniInsideReliabilityAllocation, self).__init__(n_decision_vars, n_objectives)
#
#        #initialize rbf
#         self.types[:] = rbf.platypus_types
#
#         #initialize model
#         self.susquehanna_river = SusquehannaModel(108.5, 505.0, 5, n_years, rbf)
#         self.susquehanna_river.set_log(False)
#         # Set direction of optimization for each objective
#         self.directions[0] = Problem.MAXIMIZE  # hydropower
#         self.directions[1] = Problem.MAXIMIZE  # atomic power plant
#         self.directions[2] = Problem.MAXIMIZE  # baltimore
#         self.directions[3] = Problem.MAXIMIZE  # chester
#         self.directions[4] = Problem.MINIMIZE  # environment
#         self.directions[5] = Problem.MAXIMIZE  # recreation
#         self.directions[6] = Problem.MINIMIZE  # equity reliability
#         self.directions[7] = Problem.MINIMIZE  # equity allocation
#
#     def evaluate(self, solution):
#         x = solution.variables[:]
#         self.function = self.susquehanna_river.evaluate
#         # print("printing the function")
#         # print(self.function)
#         y = self.function(x)
#         y = list(y)
#
#         index_nums = [0, 1, 2, 3, 4, 5, 13, 14]
#         solution_set = [y[val] for val in index_nums]
#
#         # self.add_objective(euclidean_distance, name = 'equity')
#
#         solution.objectives[:] = solution_set
#
#         #egalitarian_aggregated except hydropower objective
#         # apply direction of optimization to each objective
#
#         solution.objectives[:] = [solution.objectives[i] * self.directions[i] for i in range(len(solution.objectives))]

# class EquityProblemGiniInsideAllocation(Problem):
#     '''
#     According to the explanation given in the thesis, this is the Priority-based Equity objective formulation. The
#     goal is to minimize the distance between the ratio of allocation (we do not consider the demand of objectives).
#     Moreover, the objectives of the case-study are optimized.
#
#     Note that we calculate the distance between objectives inside the model, and subsequently, results are optimized
#     once this function is called.
#
#     Input:
#
#     Problem: type Platypus.Problem
#
#     Output:
#
#     solution: type dictionary
#     '''
#
#     def __init__(self, n_decision_vars, n_objectives,
#                 n_years, rbf):
#         super(EquityProblemGiniInsideAllocation, self).__init__(n_decision_vars, n_objectives)
#
#        #initialize rbf
#         self.types[:] = rbf.platypus_types
#
#         #initialize model
#         self.susquehanna_river = SusquehannaModel(108.5, 505.0, 5, n_years, rbf)
#         self.susquehanna_river.set_log(False)
#         # Set direction of optimization for each objective
#         self.directions[0] = Problem.MAXIMIZE  # hydropower
#         self.directions[1] = Problem.MAXIMIZE  # atomic power plant
#         self.directions[2] = Problem.MAXIMIZE  # baltimore
#         self.directions[3] = Problem.MAXIMIZE  # chester
#         self.directions[4] = Problem.MINIMIZE  # environment
#         self.directions[5] = Problem.MAXIMIZE  # recreation
#         self.directions[6] = Problem.MINIMIZE  # equity allocation
#
#     def evaluate(self, solution):
#         x = solution.variables[:]
#         self.function = self.susquehanna_river.evaluate
#         # print("printing the function")
#         # print(self.function)
#         y = self.function(x)
#         y = list(y)
#
#         index_nums = [0, 1, 2, 3, 4, 5, 14]
#         solution_set = [y[var] for var in index_nums]
#
#         # self.add_objective(euclidean_distance, name = 'equity')
#
#         solution.objectives[:] = solution_set
#
#         #egalitarian_aggregated except hydropower objective
#         # apply direction of optimization to each objective
#
#         solution.objectives[:] = [solution.objectives[i] * self.directions[i] for i in range(len(solution.objectives))]



########################################## OUTSIDE OBJECTIVE FORMULATIONS #################################################################

# class EquityProblemGiniOutsideReliabilityAllocation(Problem):
#     '''
#     According to the explanation given in the thesis, this is the Priority-based Equity objective formulation. The
#     goal is to minimize the distance between the ratio of allocation and demand of the objectives. Moreover, the
#     objectives of the case-study are optimized.
#
#     Note that we calculate the distance between the objectives after running the model, and subsequently, results are optimized.
#
#     Input:
#
#     Problem: type Platypus.Problem
#
#     Output:
#
#     solution: type dictionary
#     '''
#
#     def __init__(self, n_decision_vars, n_objectives,
#                 n_years, rbf):
#         super(EquityProblemGiniOutsideReliabilityAllocation, self).__init__(n_decision_vars, n_objectives)
#
#        #initialize rbf
#         self.types[:] = rbf.platypus_types
#
#         #initialize model
#         self.susquehanna_river = SusquehannaModel(108.5, 505.0, 5, n_years, rbf)
#         self.susquehanna_river.set_log(False)
#         # Set direction of optimization for each objective
#         self.directions[0] = Problem.MAXIMIZE  # hydropower
#         self.directions[1] = Problem.MAXIMIZE  # atomic power plant
#         self.directions[2] = Problem.MAXIMIZE  # baltimore
#         self.directions[3] = Problem.MAXIMIZE  # chester
#         self.directions[4] = Problem.MINIMIZE  # environment
#         self.directions[5] = Problem.MAXIMIZE  # recreation
#         self.directions[6] = Problem.MINIMIZE  # equity reliability
#         self.directions[7] = Problem.MINIMIZE  # equity allocation
#
#     @staticmethod
#     def gini_coefficient(x_input):
#         # x_array = PriorityGiniProblem.array_results(x_input)
#         numerator = 0
#         for i in range(len(x_input)):
#             for j in range(len(x_input)):
#                 if i != j:
#                 # divide by 2 to remove double counting
#                     numerator += abs(x_input[i] - x_input[j])/2
#                 else:
#                     pass
#
#         denominator = 2 * pow(len(x_input), 2) * np.average(x_input)  # (sum(x_input)/len(x_input))
#         # print("denominator", denominator)
#         # print("numerator", numerator)
#
#         gini_coeff = numerator / denominator
#         # print("da ginz", gini_coeff)
#         return gini_coeff
#
#     def evaluate(self, solution):
#         x = solution.variables[:]
#         self.function = self.susquehanna_river.evaluate
#         # print("printing the function")
#         # print(self.function)
#         y = self.function(x)
#         y = list(y)
#
#         index_nums_reliability = [1,2,3,4,5,15]
#         objectives_reliability = [y[var] for var in index_nums_reliability]
#
#         index_nums_allocation= [6,7,8,9,10]
#         objectives_allocation = [y[var] for var in index_nums_allocation]
#
#
#         # for i in range(len(objectives_reliability)):
#         gini_distance_reliability = EquityProblemGiniOutsideReliabilityAllocation.gini_coefficient(objectives_reliability)
#         print("gini", gini_distance_reliability)
#
#         # for i in range(len(objectives_allocation)):
#         gini_distance_allocation = EquityProblemGiniOutsideReliabilityAllocation.gini_coefficient(objectives_allocation)
#
#         solution_set = y[0:6]
#         solution_set.append(gini_distance_reliability)
#         solution_set.append(gini_distance_allocation)
#
#         # self.add_objective(euclidean_distance, name = 'equity')
#
#         solution.objectives[:] = solution_set
#
#         #egalitarian_aggregated except hydropower objective
#         # apply direction of optimization to each objective
#
#         solution.objectives[:] = [solution.objectives[i] * self.directions[i] for i in range(len(solution.objectives))]

# class EquityProblemGiniOutsideAllocation(Problem):
#     '''
#     According to the explanation given in the thesis, this is the Priority-based Equity objective formulation. The
#     goal is to minimize the distance between the ratio of allocation and demand of the objectives. Moreover, the
#     objectives of the case-study are optimized.
#
#     Note that we calculate the distance between the objectives after running the model, and subsequently, results are optimized.
#
#     Input:
#
#     Problem: type Platypus.Problem
#
#     Output:
#
#     solution: type dictionary
#     '''
#
#     def __init__(self, n_decision_vars, n_objectives,
#                 n_years, rbf):
#         super(EquityProblemGiniOutsideAllocation, self).__init__(n_decision_vars, n_objectives)
#
#        #initialize rbf
#         self.types[:] = rbf.platypus_types
#
#         #initialize model
#         self.susquehanna_river = SusquehannaModel(108.5, 505.0, 5, n_years, rbf)
#         self.susquehanna_river.set_log(False)
#         # Set direction of optimization for each objective
#         self.directions[0] = Problem.MAXIMIZE  # hydropower
#         self.directions[1] = Problem.MAXIMIZE  # atomic power plant
#         self.directions[2] = Problem.MAXIMIZE  # baltimore
#         self.directions[3] = Problem.MAXIMIZE  # chester
#         self.directions[4] = Problem.MINIMIZE  # environment
#         self.directions[5] = Problem.MAXIMIZE  # recreation
#         self.directions[6] = Problem.MINIMIZE  # equity
#
#     @staticmethod
#     def gini_coefficient(x_input):
#         # x_array = PriorityGiniProblem.array_results(x_input)
#         numerator = 0
#         for i in range(len(x_input)):
#             for j in range(len(x_input)):
#                 if i != j:
                # divide by 2 to remove double counting
#                     numerator += abs(x_input[i] - x_input[j])/2
#                 else:
#                     pass
#
#         denominator = 2 * pow(len(x_input), 2) * np.average(x_input)  # (sum(x_input)/len(x_input))
#         # print("denominator", denominator)
#         # print("numerator", numerator)
#
#         gini_coeff = numerator / denominator
#         # print("da ginz", gini_coeff)
#         return gini_coeff
#
#     def evaluate(self, solution):
#         x = solution.variables[:]
#         self.function = self.susquehanna_river.evaluate
#         # print("printing the function")
#         # print(self.function)
#         y = self.function(x)
#         y = list(y)
#
#         objectives_allocation = y[7:12]
#         print(objectives_allocation)
#
#         # for i in range(len(y)):
#         gini_distance = EquityProblemGiniOutsideAllocation.gini_coefficient(objectives_allocation)
#             # else:
#             #     pass
#
#         # print("\n", euclidean_distance)
#         solution_set = y[0:6]
#         solution_set.append(gini_distance)
#         # self.add_objective(euclidean_distance, name = 'equity')
#
#         solution.objectives[:] = solution_set
#
#         #egalitarian_aggregated except hydropower objective
#         # apply direction of optimization to each objective
#
#         solution.objectives[:] = [solution.objectives[i] * self.directions[i] for i in range(len(solution.objectives))]

