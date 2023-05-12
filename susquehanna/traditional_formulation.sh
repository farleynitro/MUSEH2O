#!/bin/sh
#
#SBATCH --job-name="traditional_formulation"
#SBATCH --partition=compute
#SBATCH --time=16:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=48
#SBATCH --mem-per-cpu=1G
#SBATCH --account=research-tpm-mas

module load 2022r2

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

srun python3 main_susquehanna.py