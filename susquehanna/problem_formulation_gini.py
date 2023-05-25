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
        y = list(y)

        # gini mean is index number 7
        index_nums_mean = [0, 1, 2, 3, 4, 5, 7]

        # specify here which formulation you are using
        index_nums = index_nums_mean

        # specify solution set which will be added to objectives
        solution_set = [y[var] for var in index_nums]

        # self.add_objective(euclidean_distance, name = 'equity')
        solution.objectives[:] = solution_set


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

        y = list(y)
        # gini standard deviation is index number 9
        index_nums_std = [0, 1, 2, 3, 4, 5, 9]

        # specify here which formulation you are using
        index_nums = index_nums_std

        # specify solution set which will be added to objectives

        solution_set = [y[var] for var in index_nums]
        # self.add_objective(euclidean_distance, name = 'equity')
        solution.objectives[:] = solution_set

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
        y = list(y)
        # gini ratio is index number 11
        index_nums_std = [0, 1, 2, 3, 4, 5, 11]

        # specify here which formulation you are using

        index_nums = index_nums_std

        # specify solution set which will be added to objectives
        solution_set = [y[var] for var in index_nums]
        solution.objectives[:] = solution_set




