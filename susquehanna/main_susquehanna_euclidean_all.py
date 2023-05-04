# ===========================================================================
# Name        : main_susquehanna.py
# Author      : MarkW, adapted from JazminZ & MatteoG
# Version     : 0.05
# Copyright   : Your copyright notice
# ===========================================================================
import csv
import logging
import os
import pandas as pd
import random
from platypus import EpsNSGAII, ProcessPoolEvaluator
    # Other evaluators seem to not yield faster results: Evaluator, PoolEvaluator, MultiprocessingEvaluator
from problem_formulation_euclidean import  CombinedTraditionalEuclideanMean, CombinedTraditionalEuclideanStd, CombinedTraditionalEuclideanRatioStdMean
import rbf_functions

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

    header = [
        "hydropower revenue",
        "atomic plant reliability",
        "baltimore reliability",
        "chester reliability",
        "environment reliability",
        "recreation reliability",
        "equity"
    ]

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
    seeds = [10, 20, 30, 40, 50]
    entry = rbf_functions.original_rbf

    # Model setup with rbf
    n_inputs = 2
    n_outputs = 4
    n_years = 1
    n_objectives_justice = 7

    # rbf setup
    n_rbfs = 4

    rbf = rbf_functions.RBF(n_rbfs, n_inputs, n_outputs, rbf_function=entry)
    n_decision_vars = len(rbf.platypus_types)


    ############## FOR EUCLIDEAN FORMULATIONS ####################
    euclidean_std = CombinedTraditionalEuclideanStd(n_decision_vars, n_objectives_justice,
                                                    n_years, rbf)
    euclidean_mean = CombinedTraditionalEuclideanMean(n_decision_vars, n_objectives_justice,
                                                      n_years, rbf)
    euclidean_ratio_std_mean = CombinedTraditionalEuclideanRatioStdMean(n_decision_vars, n_objectives_justice,
                                                                        n_years, rbf)
    # choose out of the following problems
    # 3 different objective formulations in total. They are meant for test runs where we test both the distance based optimization
    # inside and outside the objective formulation. In the original problem we do not test it.

    problem_choices = [euclidean_mean, euclidean_std, euclidean_ratio_std_mean]

    # choose problem
    for problem_choice in problem_choices:
        for seed in seeds:
            random.seed(seed)

            # leave it as is
            epsilons = [0.5, 0.05, 0.05, 0.05, 0.001, 0.05, 0.1]

            # run all problems
            track_progress = TrackProgress()
            with ProcessPoolEvaluator() as evaluator:
                algorithm = EpsNSGAII(problem_choice, epsilons=epsilons, evaluator=evaluator)
                algorithm.run(500000, track_progress)
            store_results(
                algorithm, track_progress, "output_farley", f"{problem_choice.__class__.__name__}", seed
            )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()


