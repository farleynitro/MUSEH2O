# ===========================================================================
# Name        : main_susquehanna.py
# Author      : MarkW, adapted from JazminZ & MatteoG
# Version     : 0.05
# Copyright   : Your copyright notice
# ===========================================================================
import csv
import logging
import numpy as np
import os
import pandas as pd
import random

from platypus import Problem, EpsNSGAII, Real, ProcessPoolEvaluator

# from problem_formulation_euclidean import  EquityProblemEuclideanInsideReliabilityAllocation, EquityProblemEuclideanInsideReliability, EquityProblemEuclideanInsideAllocation, EquityProblemEuclideanOutsideReliabilityAllocation, EquityProblemEuclideanOutsideReliability, EquityProblemEuclideanOutsideAllocation
# from problem_formulation_gini import EquityProblemGiniInsideReliabilityAllocation, EquityProblemGiniInsideReliability, EquityProblemGiniInsideAllocation, EquityProblemGiniOutsideReliabilityAllocation, EquityProblemGiniOutsideReliability, EquityProblemGiniOutsideAllocation

from problem_formulation_euclidean import  EquityProblemEuclideanInsideReliability, EquityProblemEuclideanOutsideReliability
from problem_formulation_gini import EquityProblemGiniInsideReliability, EquityProblemGiniOutsideReliability
from problem_formulation_original import OriginalProblem
import rbf_functions


# OriginalProblem
# EquityProblemEuclideanInsideReliabilityAllocation
# EquityProblemEuclideanInsideReliability
# EquityProblemEuclideanInsideAllocation
# EquityProblemEuclideanOutsideReliabilityAllocation
# EquityProblemEuclideanOutsideReliability
# EquityProblemEuclideanOutsideAllocation
# EquityProblemGiniInsideReliabilityAllocation
# EquityProblemGiniInsideReliability
# EquityProblemGiniInsideAllocation
# EquityProblemGiniOutsideReliabilityAllocation
# EquityProblemGiniOutsideReliability
# EquityProblemGiniOutsideAllocation

class TrackProgress:
    def __init__(self):
        self.nfe = []
        self.improvements = []
        self.objectives = {}

    def __call__(self, algorithm):
        self.nfe.append(algorithm.nfe)
        self.improvements.append(algorithm.archive.improvements)
        temp = {}
        for i, solution in enumerate(algorithm.archive):
            temp[i] = list(solution.objectives)
        self.objectives[algorithm.nfe] = pd.DataFrame.from_dict(temp, orient="index")

    def to_dataframe(self):
        df_imp = pd.DataFrame.from_dict(
            dict(nfe=self.nfe, improvements=self.improvements)
        )
        df_hv = pd.concat(self.objectives, axis=0)
        return df_imp, df_hv


def store_results(algorithm, track_progress, output_dir, objective_formulation, seed_id):
    path_name = f"{output_dir}/{objective_formulation}"
    if not os.path.exists(path_name):
        try:
            os.makedirs(path_name)
            os.chmod(path_name, 0o777)  # set permissions to read, write, and execute for owner, group, and others

        except OSError:
            print("Creation of the directory failed")

    header = None

    # if objective_formulation in ['EquityProblemEuclideanInsideReliabilityAllocation', 'EquityProblemEuclideanOutsideReliabilityAllocation', 'EquityProblemGiniInsideReliabilityAllocation']:
    #     header = [
    #         "hydropower reliability",
    #         "atomicpowerplant reliability",
    #         "baltimore reliability",
    #         "chester reliability",
    #         "environment reliability",
    #         "recreation reliability",
    #         "allocation based equity",
    #         "reliability based equity"
    #     ]

    if objective_formulation in ['OriginalProblem']:
        header = [
            "hydropower reliability",
            "atomicpowerplant reliability",
            "baltimore reliability",
            "chester reliability",
            "environment reliability",
            "recreation reliability"
        ]

    elif objective_formulation in ['EquityProblemEuclideanInsideReliability', 'EquityProblemEuclideanOutsideReliability', 'EquityProblemGiniInsideReliability', 'EquityProblemGiniOutsideReliability']:
        header = [
            "hydropower reliability",
            "atomicpowerplant reliability",
            "baltimore reliability",
            "chester reliability",
            "environment reliability",
            "recreation reliability",
            "reliability based equity"
        ]

    # elif objective_formulation in ['EquityProblemEuclideanInsideAllocation', 'EquityProblemEuclideanOutsideAllocation', 'EquityProblemGiniInsideAllocation', 'EquityProblemGiniOutsideAllocation']:
    #     header = [
    #         "hydropower reliability",
    #         "atomicpowerplant reliability",
    #         "baltimore reliability",
    #         "chester reliability",
    #         "environment reliability",
    #         "recreation reliability",
    #         "recreation allocation",
    #         # "reliability based equity"
    #     ]

    with open(
            f"{output_dir}/{objective_formulation}/{seed_id}_solution.csv",
            "w",
            encoding="UTF8",
            newline="",
    ) as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for solution in algorithm.result:
            writer.writerow(solution.objectives)

    with open(
            f"{output_dir}/{objective_formulation}/{seed_id}_variables.csv",
            "w",
            encoding="UTF8",
            newline="",
    ) as f:
        writer = csv.writer(f)
        for solution in algorithm.result:
            writer.writerow(solution.variables)

    # save progress info
    df_conv, df_hv = track_progress.to_dataframe()
    df_conv.to_csv(f"{output_dir}/{objective_formulation}/{seed_id}_convergence.csv")
    df_hv.to_csv(f"{output_dir}/{objective_formulation}/{seed_id}_hypervolume.csv")

def main():
    seeds = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    entry = rbf_functions.original_rbf

    for seed in seeds:
        random.seed(seed)
        n_inputs = 2
        n_outputs = 4
        n_years = 1

        #objectives, based on the distance based objective we can change the number of objectives.
        n_objectives_original = 6
        # n_objectives_reliability_and_allocation = 8
        n_objectives_reliability = 7
        n_objectives_allocation = 7
        n_rbfs = 4

        rbf = rbf_functions.RBF(n_rbfs, n_inputs, n_outputs, rbf_function=entry)
        n_decision_vars = len(rbf.platypus_types)

        # choose out of the following problems
        # 7 different objective formulations in total. They are meant for test runs where we test both the distance based optimization
        # inside and outside the objective formulation. In the original problem we do not test it.

        original = OriginalProblem(n_decision_vars, n_objectives_original, n_years, rbf)

        ############## FOR EUCLIDEAN ####################
        euclidean_equity_inside_reliability = EquityProblemEuclideanInsideReliability(n_decision_vars, n_objectives_reliability,
                                                                            n_years, rbf)
        euclidean_equity_outside_reliability = EquityProblemEuclideanOutsideReliability(n_decision_vars, n_objectives_reliability,
                                                                            n_years, rbf)
        # euclidean_equity_inside_allocation = EquityProblemEuclideanInsideAllocation(n_decision_vars, n_objectives_allocation,
        #                                                                     n_years, rbf)
        # euclidean_equity_outside_allocation = EquityProblemEuclideanOutsideAllocation(n_decision_vars, n_objectives_allocation,
        #                                                                   n_years, rbf)
        # euclidean_equity_inside_reliability_and_allocation = EquityProblemEuclideanInsideReliabilityAllocation(n_decision_vars, n_objectives_reliability_and_allocation,
        #                                                                   n_years, rbf)
        # euclidean_equity_outside_reliability_and_allocation = EquityProblemEuclideanOutsideReliabilityAllocation(n_decision_vars, n_objectives_reliability_and_allocation,
        #                                                                   n_years, rbf)

        ################ FOR GINI ######################

        gini_equity_inside_reliability = EquityProblemGiniInsideReliability(n_decision_vars, n_objectives_reliability,
                                                                            n_years, rbf)
        gini_equity_outside_reliability = EquityProblemGiniOutsideReliability(n_decision_vars, n_objectives_reliability,
                                                                            n_years, rbf)
        # gini_equity_inside_allocation = EquityProblemGiniInsideAllocation(n_decision_vars, n_objectives_allocation,
        #                                                                   n_years, rbf)
        # gini_equity_outside_allocation = EquityProblemGiniOutsideAllocation(n_decision_vars, n_objectives_allocation,
        #                                                                   n_years, rbf)
        # gini_equity_inside_reliability_and_allocation = EquityProblemGiniInsideReliabilityAllocation(n_decision_vars, n_objectives_reliability_and_allocation,
        #                                                                   n_years, rbf)
        # gini_equity_outside_reliability_and_allocation = EquityProblemGiniOutsideReliabilityAllocation(n_decision_vars, n_objectives_reliability_and_allocation,
        #                                                                   n_years, rbf)

        #choose problem
        problem_choice = original

        epsilons = [0.5, 0.05, 0.05, 0.05, 0.001, 0.05]

        # algorithm = EpsNSGAII(problem, epsilons=epsilons)
        # algorithm.run(1000)

        track_progress = TrackProgress()
        with ProcessPoolEvaluator() as evaluator:
            algorithm = EpsNSGAII(problem_choice, epsilons=epsilons, evaluator=evaluator)
            algorithm.run(10000, track_progress)

        store_results(
            algorithm, track_progress, "output_farley", f"{problem_choice.__class__.__name__}", seed
        )



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
