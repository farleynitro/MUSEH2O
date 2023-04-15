import numpy as np

import csv
from susquehanna_model import SusquehannaModel
from platypus import Problem
import pandas as pd

########################################## INSIDE OBJECTIVE FORMULATIONS #################################################################


class UtilitarianProblem(Problem):
    '''
    According to the explanation given in the thesis, this is the Original objective formulation. The
    goal is to maximize the direction of all objectives in a consequentialist manner. Therefore we maximize
    reliability of hydropower, environmental, baltimore, chester, atomic, and recreation. We do not consider equity
    here.
    Input:
    Problem: type Platypus.Problem
    Output:
    solution: type dictionary
    '''
    def __init__(self,
                 n_decision_vars,
                 n_objectives,
                 n_years,
                 rbf):
        super(UtilitarianProblem, self).__init__(n_decision_vars,
                                              n_objectives)

        # # initialize empty dataframe to store results
        # self.df = pd.DataFrame(columns=['euclidean distance', 'gini distance', 'hydro reliability'])

        #initialize rbf
        self.types[:] = rbf.platypus_types

        #initialize model
        self.susquehanna_river = SusquehannaModel(108.5, 505.0, 5, n_years, rbf)
        self.susquehanna_river.set_log(True)

        # self.list_gini_std = []
        # self.list_gini_mean = []
        # self.list_eucli_std = []
        # self.list_eucli_mean = []
        # self.list_j_hydro_reliability = []
        # self.list_gini_std_monthly = []
        # self.list_eucli_std_monthly = []

        # Set direction of optimization for each objective
        self.directions[0] = Problem.MAXIMIZE  # hydropower
        self.directions[1] = Problem.MAXIMIZE  # atomic power plant
        self.directions[2] = Problem.MAXIMIZE  # baltimore
        self.directions[3] = Problem.MAXIMIZE  # chester
        self.directions[4] = Problem.MINIMIZE  # environment
        self.directions[5] = Problem.MAXIMIZE  # recreation

    # def extract_variables(self,):
    #     print(self.empty_list_gini_coefficients)
    #     return self.empty_list_gini_coefficients

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

        df_results = pd.concat([
            pd.Series(y[0], dtype='float64'),
            pd.Series(y[1], dtype='float64'),
            pd.Series(y[2], dtype='float64'),
            pd.Series(y[3], dtype='float64'),
            pd.Series(y[4], dtype='float64'),
            pd.Series(y[5], dtype='float64'),
            pd.Series(self.susquehanna_river.gini_monthly_std_coeff),
            pd.Series(self.susquehanna_river.gini_yearly_mean_coeff),
            pd.Series(self.susquehanna_river.eucli_monthly_std_coeff),
            pd.Series(self.susquehanna_river.eucli_yearly_mean_coeff),
            pd.Series(self.susquehanna_river.gini_monthly),
            pd.Series(self.susquehanna_river.eucli_monthly),
            pd.Series(self.susquehanna_river.j_hydro_reliability_yearly_mean)
        ], axis=1)

        df_results.to_csv("utilitarian_problem_results.csv", mode='a', index = False, header = False)

        # set objective values for only original problem posed [0:5]
        solution.objectives[:] = y[0:6]

        # apply direction of optimization to each objective
        solution.objectives[:] = [solution.objectives[i] * self.directions[i] for i in range(len(self.directions))]

        # with open('test_1', 'a', encoding="UTF8", newline="",) as f:
        #     # using csv.writer method from CSV package
        #     write = csv.writer(f)
        #     write.writerow(self.susquehanna_river.gini_yearly_mean_coeff)
        #
        # with open('test_2', 'a', encoding="UTF8", newline="", ) as f:
        #     # using csv.writer method from CSV package
        #     write = csv.writer(f)
        #     write.writerows(self.empty_list_gini_coefficients)
        #     # write.writerows(rows)




