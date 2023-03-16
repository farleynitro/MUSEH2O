from susquehanna_model import SusquehannaModel
from platypus import NSGAII, Problem, Real
from scipy.spatial.distance import pdist
import math
from math import dist
import numpy as np


########################################## INSIDE OBJECTIVE FORMULATIONS #################################################################

class EquityProblemEuclideanInsideReliabilityAllocation(Problem):
    '''
    According to the explanation given in the thesis, this is the Equity objective formulation. The
    goal is to minimize the distance between the ratio of allocation and demand of the objectives, and the distance
    between the ratio of allocation (without considering the demand of objectives). Moreover, the
    objectives of the case-study are optimized.

    Note that we calculate the distance between objectives inside the model, and subsequently, results are optimized
    once this function is called.

    Input:

    Problem: type Platypus.Problem

    Output:

    solution: type dictionary
    '''

    def __init__(self, n_decision_vars, n_objectives,
                n_years, rbf):
        super(EquityProblemEuclideanInsideReliabilityAllocation, self).__init__(n_decision_vars, n_objectives)

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
        self.directions[6] = Problem.MINIMIZE  # equity reliability
        self.directions[7] = Problem.MINIMIZE  # equity allocation

    def evaluate(self, solution):
        x = solution.variables[:]
        self.function = self.susquehanna_river.evaluate
        # print("printing the function")
        # print(self.function)
        y = self.function(x)
        y = list(y)

        index_nums = [0, 1, 2, 3, 4, 5, 11, 12]
        solution_set = [y[val] for val in index_nums]

        # self.add_objective(euclidean_distance, name = 'equity')

        solution.objectives[:] = solution_set

        #egalitarian_aggregated except hydropower objective
        # apply direction of optimization to each objective

        solution.objectives[:] = [solution.objectives[i] * self.directions[i] for i in range(len(solution.objectives))]

class EquityProblemEuclideanInsideReliability(Problem):
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
        super(EquityProblemEuclideanInsideReliability, self).__init__(n_decision_vars, n_objectives)

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
        self.directions[6] = Problem.MINIMIZE  # equity reliability

    def evaluate(self, solution):
        x = solution.variables[:]
        self.function = self.susquehanna_river.evaluate
        # print("printing the function")
        # print(self.function)
        y = self.function(x)
        y = list(y)


        index_nums = [0,1,2,3,4,5,11]
        solution_set = [y[var] for var in index_nums]
        # print(solution_set)
        # self.add_objective(euclidean_distance, name = 'equity')

        solution.objectives[:] = solution_set

        #egalitarian_aggregated except hydropower objective
        # apply direction of optimization to each objective

        solution.objectives[:] = [solution.objectives[i] * self.directions[i] for i in range(len(solution.objectives))]

class EquityProblemEuclideanInsideAllocation(Problem):
    '''
    According to the explanation given in the thesis, this is the Priority-based Equity objective formulation. The
    goal is to minimize the distance between the ratio of allocation (we do not consider the demand of objectives).
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
        super(EquityProblemEuclideanInsideAllocation, self).__init__(n_decision_vars, n_objectives)

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
        self.directions[6] = Problem.MINIMIZE  # equity allocation

    def evaluate(self, solution):
        x = solution.variables[:]
        self.function = self.susquehanna_river.evaluate
        # print("printing the function")
        # print(self.function)
        y = self.function(x)
        y = list(y)

        index_nums = [0, 1, 2, 3, 4, 5, 12]
        solution_set = [y[var] for var in index_nums]

        # self.add_objective(euclidean_distance, name = 'equity')

        solution.objectives[:] = solution_set

        #egalitarian_aggregated except hydropower objective
        # apply direction of optimization to each objective

        solution.objectives[:] = [solution.objectives[i] * self.directions[i] for i in range(len(solution.objectives))]






########################################## OUTSIDE OBJECTIVE FORMULATIONS #################################################################
class EquityProblemEuclideanOutsideReliabilityAllocation(Problem):
    '''
    According to the explanation given in the thesis, this is the Priority-based Equity objective formulation. The
    goal is to minimize the distance between the ratio of allocation and demand of the objectives. Moreover, the
    objectives of the case-study are optimized.

    Note that we calculate the distance between the objectives after running the model, and subsequently, results are optimized.

    Input:

    Problem: type Platypus.Problem

    Output:

    solution: type dictionary
    '''

    def __init__(self, n_decision_vars, n_objectives,
                n_years, rbf):
        super(EquityProblemEuclideanOutsideReliabilityAllocation, self).__init__(n_decision_vars, n_objectives)

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
        self.directions[6] = Problem.MINIMIZE  # equity reliability
        self.directions[7] = Problem.MINIMIZE  # equity allocation


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
        x_array = SusquehannaModel.array_results(x_input)
        for i in range(len(x_array)):
            for j in range(len(x_array)):
                if i != j:
                    # print("x_array[i]", x_array[i])
                    total_distance += SusquehannaModel.euclidean_distance_singular(x_array[i], x_array[j])
                # print("total_distance", total_distance)
                else:
                    pass
        return total_distance

    def evaluate(self, solution):
        x = solution.variables[:]
        self.function = self.susquehanna_river.evaluate
        # print("printing the function")
        # print(self.function)
        y = self.function(x)
        y = list(y)

        index_nums_reliability = [1,2,3,4,5,15]
        objectives_reliability = [y[var] for var in index_nums_reliability]

        index_nums_allocation= [6,7,8,9,10]
        objectives_allocation = [y[var] for var in index_nums_allocation]


        # for i in range(len(objectives_reliability)):
            # if i != 0: #ignoring hydropower objective for now since the objective is defined differently
        euclidean_distance_reliability = EquityProblemEuclideanOutsideReliabilityAllocation.euclidean_distance_multiple(objectives_reliability)
        print("eucli", euclidean_distance_reliability)

            # else:
            #     pass

        # for i in range(len(objectives_allocation)):
            # if i != 0: #ignoring hydropower objective for now since the objective is defined differently
        euclidean_distance_allocation = EquityProblemEuclideanOutsideReliabilityAllocation.euclidean_distance_multiple(objectives_allocation)
            # else:
            #     pass

        solution_set = y[0:6]
        solution_set.append(euclidean_distance_reliability)
        solution_set.append(euclidean_distance_allocation)

        # self.add_objective(euclidean_distance, name = 'equity')

        solution.objectives[:] = solution_set

        #egalitarian_aggregated except hydropower objective
        # apply direction of optimization to each objective

        solution.objectives[:] = [solution.objectives[i] * self.directions[i] for i in range(len(solution.objectives))]


class EquityProblemEuclideanOutsideReliability(Problem):
    '''
    According to the explanation given in the thesis, this is the Priority-based Equity objective formulation. The
    goal is to minimize the distance between the ratio of allocation and demand of the objectives. Moreover, the
    objectives of the case-study are optimized.

    Note that we calculate the distance between the objectives after running the model, and subsequently, results are optimized.

    Input:

    Problem: type Platypus.Problem

    Output:

    solution: type dictionary
    '''

    def __init__(self, n_decision_vars, n_objectives,
                n_years, rbf):
        super(EquityProblemEuclideanOutsideReliability, self).__init__(n_decision_vars, n_objectives)

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
        x_array = SusquehannaModel.array_results(x_input)
        for i in range(len(x_array)):
            for j in range(len(x_array)):
                if i != j:
                    # print("x_array[i]", x_array[i])
                    total_distance += SusquehannaModel.euclidean_distance_singular(x_array[i], x_array[j])
                # print("total_distance", total_distance)
                else:
                    pass
        return total_distance

    def evaluate(self, solution):
        x = solution.variables[:]
        self.function = self.susquehanna_river.evaluate
        # print("printing the function")
        # print(self.function)
        y = self.function(x)
        y = list(y)

        # objectives_reliability = y[0:6]

        index_nums = [1, 2, 3, 4, 5, 15]
        objectives_reliability = [y[val] for val in index_nums]
        print("objectives_reliability", objectives_reliability)

        # for i in range(len(objectives_reliability)):
            # if i != 0: # ignoring hydropower objective for now since the objective is defined differently
        euclidean_distance = EquityProblemEuclideanOutsideReliability.euclidean_distance_multiple(objectives_reliability)
        print("eucli", euclidean_distance)

            # else:
            #     pass

        # print("\n", euclidean_distance)

        solution_set = y[0:6]
        solution_set.append(euclidean_distance)
        # self.add_objective(euclidean_distance, name = 'equity')

        solution.objectives[:] = solution_set

        #egalitarian_aggregated except hydropower objective
        # apply direction of optimization to each objective

        solution.objectives[:] = [solution.objectives[i] * self.directions[i] for i in range(len(solution.objectives))]

class EquityProblemEuclideanOutsideAllocation(Problem):
    '''
    According to the explanation given in the thesis, this is the Priority-based Equity objective formulation. The
    goal is to minimize the distance between the ratio of allocation and demand of the objectives. Moreover, the
    objectives of the case-study are optimized.

    Note that we calculate the distance between the objectives after running the model, and subsequently, results are optimized.

    Input:

    Problem: type Platypus.Problem

    Output:

    solution: type dictionary
    '''

    def __init__(self, n_decision_vars, n_objectives,
                n_years, rbf):
        super(EquityProblemEuclideanOutsideAllocation, self).__init__(n_decision_vars, n_objectives)

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
        x_array = SusquehannaModel.array_results(x_input)
        for i in range(len(x_array)):
            for j in range(len(x_array)):
                if i != j:
                    # print("x_array[i]", x_array[i])
                    total_distance += SusquehannaModel.euclidean_distance_singular(x_array[i], x_array[j])
                # print("total_distance", total_distance)
                else:
                    pass
        return total_distance

    def evaluate(self, solution):
        x = solution.variables[:]
        self.function = self.susquehanna_river.evaluate
        # print("printing the function")
        # print(self.function)
        y = self.function(x)
        y = list(y)

        objectives_allocation = y[7:12]
        # print(objectives_allocation)

        # for i in range(len(objectives_allocation)):
        euclidean_distance = EquityProblemEuclideanOutsideAllocation.euclidean_distance_multiple(objectives_allocation)
            # else:
            #     pass

        # print("\n", euclidean_distance)
        solution_set = y[0:6]
        solution_set.append(euclidean_distance)
        # self.add_objective(euclidean_distance, name = 'equity')

        solution.objectives[:] = solution_set

        #egalitarian_aggregated except hydropower objective
        # apply direction of optimization to each objective

        solution.objectives[:] = [solution.objectives[i] * self.directions[i] for i in range(len(solution.objectives))]

