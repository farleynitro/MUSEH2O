#!/bin/sh
#
#SBATCH --job-name="Conowingo_trial_euclidean_mean"
#SBATCH --partition=compute
#SBATCH --time=24:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=48
#SBATCH --mem-per-cpu=1G
#SBATCH --account=education-tpm-msc-epa

module load 2022r2

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

srun python3 main_susquehanna.py > result_pi.log