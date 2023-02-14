# ===========================================================================
# Name        : main_susquehanna.py
# Author      : MarkW, adapted from JazminZ & MatteoG
# Version     : 0.05
# Copyright   : Your copyright notice
# ===========================================================================
import csv
import logging
# import os-sys
# import sys
from ema_workbench.em_framework.optimization import EpsilonProgress, HyperVolume


import pandas as pd
from ema_workbench import (Model, ScalarOutcome, RealParameter)
# from platypus import Problem, EpsNSGAII, Real, ProcessPoolEvaluator
from ema_workbench import MultiprocessingEvaluator, ema_logging

from rbf import rbf_functions
from susquehanna_model import SusquehannaModel

# module_path = os.path.abspath(os.path.join(".."))
# if module_path not in sys.path:
#     sys.path.append(module_path)

def main():
    # RBF parameters
    n_inputs = 2  # (time, storage of Conowingo)
    n_outputs = 4
    n_rbfs = 4 #changed from 4, or 1 now?
    rbf = rbf_functions.RBF(n_rbfs, n_inputs, n_outputs, rbf_function=[rbf_functions.original_rbf])
    #model

    # Load the model:
    n_years = 1
    susquehanna_model = SusquehannaModel(108.5, 505.0, 5, n_years, rbf)
    susquehanna_model.set_log(True) #Set to true to keep track

    # workbench model:
    ema_susquehanna_model = Model('susquehanna', function=susquehanna_model)

    levers_types = rbf.platypus_types
    levers_list = list()

    for i in range(len(levers_types)):
        # modulus = (i - n_outputs) % p_per_RBF
        # if (
        #     (i >= n_outputs)
        #     and (modulus < (p_per_RBF - n_outputs))
        #     and (modulus % 2 == 0)
        # ):  # centers:
        levers_list.append(RealParameter(f"v{i}", -1, 1))
        # else:  # linear parameters for each release, radii and weights of RBFs:
        #     lever_list.append(RealParameter(f"v{i}", 0, 1))

    ema_susquehanna_model.levers = levers_list

    #inspired from Yasin's thesis
    # parameter_count = susquehanna_model.overarching_policy.get_total_parameter_count()
    # n_inputs = nile_model.overarching_policy.functions["release"].n_inputs
    # n_outputs = nile_model.overarching_policy.functions["release"].n_outputs
    # RBF_count = nile_model.overarching_policy.functions["release"].RBF_count
    # p_per_RBF = 2 * n_inputs + n_outputs

    # lever_list = list()
    # for i in range(parameter_count):
    #     modulus = (i - n_outputs) % p_per_RBF
    #     if (
    #         (i >= n_outputs)
    #         and (modulus < (p_per_RBF - n_outputs))
    #         and (modulus % 2 == 0)
    #     ):  # centers:
    #         lever_list.append(RealParameter(f"v{i}", -1, 1))
    #     else:  # linear parameters for each release, radii and weights of RBFs:
    #         lever_list.append(RealParameter(f"v{i}", 0, 1))

    # levers
    #     # load uncertainties and levers in dike_model:
    #     susquehanna_river.uncertainties = uncertainties
    #     susquehanna_river.levers = levers
    #
    #     # initialize objective problem formulation
    #
        # status quo, 6 objectives
    variable_names = []
    variable_names_ = []
    variable_names__ = []
    variable_names___ = []
    variable_names____ = []
    variable_names_____ = []

    # for n in ema_susquehanna_model.decision_steps_per_year:
    #     variable_names.extend(['Hydropower Revenue {}'.format(n)])
    #     variable_names_.extend(['Atomic Power Plant water supply reliability {}'.format(n)])
    #     variable_names__.extend(['Baltimore water supply reliability {}'.format(n)])
    #     variable_names___.extend(['Chester water supply reliability {}'.format(n)])
    #     variable_names____.extend(['Storage reliability (Recreation) {}'.format(n)])
    #     variable_names_____.extend(['Environmental shortage {}'.format(n)])

    #specify direction to maximize over
    direction_min = ScalarOutcome.MINIMIZE
    direction_max = ScalarOutcome.MAXIMIZE


    #specify objectives
    ema_susquehanna_model.outcomes = [
        ScalarOutcome('Hydropower Revenue',
                      direction_max),

        ScalarOutcome('Atomic Power Plant water supply reliability',
                      direction_max),

        ScalarOutcome('Baltimore water supply reliability',
                      direction_max),

        ScalarOutcome('Chester water supply reliability',
                      direction_max),

        ScalarOutcome('Storage reliability (Recreation)',
                      direction_max),

        ScalarOutcome('Environmental shortage',
                      direction_min),
        ]

    # #specify objectives
    # ema_susquehanna_model.outcomes = [
    #     ScalarOutcome('Hydropower Revenue',
    #                   variable_name=[var for var in variable_names],
    #                   function=sum_over, kind=direction_max),
    #
    #     ScalarOutcome('Atomic Power Plant water supply reliability',
    #                   variable_name=[var for var in variable_names_],
    #                   function=sum_over, kind=direction_max),
    #
    #     ScalarOutcome('Baltimore water supply reliability',
    #                   variable_name=[var for var in variable_names__],
    #                   function=sum_over, kind=direction_max),
    #
    #     ScalarOutcome('Chester water supply reliability',
    #                   variable_name=[var for var in variable_names___],
    #                   function=sum_over, kind=direction_max),
    #
    #     ScalarOutcome('Storage reliability (Recreation)',
    #                   variable_name=[var for var in variable_names____],
    #                   function=sum_over, kind=direction_max),
    #
    #     ScalarOutcome('Environmental shortage',
    #                   variable_name=[var for var in variable_names_____],
    #                   function=sum_over, kind=direction_min),
    #     ]

        # Lower and Upper Bound for problem.types
    epsilon_list = [0.5, 0.05, 0.05, 0.05, 0.001, 0.05] #old value
        # n_decision_vars = len(rbf.platypus_types)
        #
        # problem = Problem(n_decision_vars, n_objectives)
        # problem.types[:] = rbf.platypus_types
        # problem.function = susquehanna_river.evaluate
        #
        # problem.directions[0] = Problem.MAXIMIZE  # hydropower
        # problem.directions[1] = Problem.MAXIMIZE  # atomic power plant
        # problem.directions[2] = Problem.MAXIMIZE  # baltimore
        # problem.directions[3] = Problem.MAXIMIZE  # chester
        # problem.directions[4] = Problem.MINIMIZE  # environment
        # problem.directions[5] = Problem.MAXIMIZE  # recreation

    # ###################################### run experiments ################################################################
    #
    convergence_metrics = [EpsilonProgress()]

    # seeds = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]  # run later
    # for seed in seeds:
    #     random.seed(seed)
    #     ema_logging.log_to_stderr(ema_logging.INFO)
    #
    #     #using directed policy search
    #
    with MultiprocessingEvaluator(ema_susquehanna_model) as evaluator:
        results = evaluator.optimize(nfe=5, searchover="levers", convergence=convergence_metrics, epsilons=epsilon_list)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
