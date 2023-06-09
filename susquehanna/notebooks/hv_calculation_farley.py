import pandas as pd
import datetime as DT
from platypus import Solution, Problem, Hypervolume
import pickle

#change according to your own library
# folder_destination_data = '/Users/farleyrimon/Documents/GitHub/MUSEH2O/susquehanna/refsets'

# open a file, where you stored the pickled data
# file_ref = open(f'{folder_destination_data}/ref_sets_hv.pkl', 'rb')
# file_arch = open(f'{folder_destination_data}/archives_hv.pkl', 'rb')

file_ref = open(f'ref_sets_hv.pkl', 'rb')
file_arch = open(f'archives_hv.pkl', 'rb')

# dump information to that file
ref_sets = pickle.load(file_ref)
archives = pickle.load(file_arch)


# close the file
file_ref.close()
file_arch.close()


ethical_formulations = [#'TraditionalPrinciple',
                        # 'CombinedTraditionalGiniMean',
                        'CombinedTraditionalGiniStd',
                        'CombinedTraditionalGiniRatioStdMean',
                        # 'CombinedTraditionalEuclideanMean',
                        # 'CombinedTraditionalEuclideanStd',
                        # 'CombinedTraditionalEuclideanRatioStdMean',
]



for ethical_formulation in ethical_formulations:
    tempnfe = {}
    temphv = {}
    nfe_sets = {}
    hv_sets = {}
    # for rbf in archives:
    nfe_sets[ethical_formulation] = {}
    hv_sets[ethical_formulation] = {}
    hv = Hypervolume(reference_set=ref_sets[ethical_formulation])
    print(f"started {ethical_formulation} at {DT.datetime.now().strftime('%H:%M:%S')}")
    for seed in archives[ethical_formulation]:
        nfe_sets[ethical_formulation][seed] = {}
        hv_sets[ethical_formulation][seed] = {}
        s_archives = archives[ethical_formulation][seed]
        nfes = []
        hvs = []
        for nfe, archive in s_archives.items():
            nfes.append(nfe)
            hvs.append(hv.calculate(archive))

        nfe_sets[ethical_formulation][seed] = nfes
        hv_sets[ethical_formulation][seed] = hvs
        tempnfe[seed] = nfes
        temphv[seed] = hvs
        dfhv = pd.DataFrame.from_dict(temphv, orient='index')
        dfnfe = pd.DataFrame.from_dict(tempnfe, orient='index')
        dfhv = dfhv.T
        dfnfe = dfnfe.T
        dfhv.to_csv(f"{ethical_formulation}_hv.csv", index=False)
        dfnfe.to_csv(f"{ethical_formulation}_nfe.csv", index=False)
        print(f"finished seed: {seed} at {DT.datetime.now().strftime('%H:%M:%S')}")

    #     dfhv.to_csv(f"hv_global/{rbf}_hv_all.csv", index=False) #global
    #     dfnfe.to_csv(f"hv_global/{rbf}_nfe_all.csv", index=False) #global
