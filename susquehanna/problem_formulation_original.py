import numpy as np

from susquehanna_model import SusquehannaModel
from platypus import Problem
import pandas as pd

########################################## INSIDE OBJECTIVE FORMULATIONS #################################################################

class OriginalProblem(Problem):
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
        super(OriginalProblem, self).__init__(n_decision_vars,
                                              n_objectives)

        # initialize empty dataframe to store results
        self.df = pd.DataFrame(columns=['euclidean distance', 'gini distance', 'hydro reliability'])

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

    # def store_results(output_dir, objective_formulation):
    #     path_name = f"{output_dir}/{objective_formulation}"
    #     if not os.path.exists(path_name):
    #         try:
    #             os.makedirs(path_name)
    #             os.chmod(path_name,
    #                      0o777)  # set permissions to read, write, and execute for owner, group, and others
    #
    #         except OSError:
    #             print("Creation of the directory failed")

    def evaluate(self, solution):

        x = solution.variables[:]

        self.function = self.susquehanna_river.evaluate

        y = self.function(x)

        # storing non optimized results
        non_optimized_solution = np.array((y[6:]))
        non_optimized_solution_array = np.reshape(non_optimized_solution, (1,3))

        # convert the NumPy array to a pandas DataFrame object
        arr_df = pd.DataFrame(non_optimized_solution_array, columns=self.df.columns)

        # concatenate the DataFrame and the array DataFrame
        self.df = pd.concat([self.df, arr_df], axis=0)
        self.df.to_csv("output_farley/non_optimized_objectives.csv")

        # set objective values for only original problem posed [0:5]
        solution.objectives[:] = y[0:6]

        # apply direction of optimization to each objective
        solution.objectives[:] = [solution.objectives[i] * self.directions[i] for i in range(len(self.directions))]




