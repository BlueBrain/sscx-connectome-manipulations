#!/bin/bash -l
#SBATCH --job-name=syndensity
#SBATCH --time=1:00:00
#SBATCH --account=proj83
#SBATCH --partition=prod
#SBATCH --mem=0
#SBATCH --exclusive
#SBATCH --constraint=cpu

source /gpfs/bbp.cscs.ch/home/pokorny/ReWiringKernel/bin/activate
python -u dendritic_synapse_density_target_SONATA.py $1 $2 $3 $4 $5 $6

# EXAMPLE HOW TO RUN: sbatch run_dendritic_synapse_density_SONATA.sh CIRCUIT_CONFIG_PATH NODES_POPUL_NAME <CIRCUIT_TARGET> <#PARALLEL_JOBS, e.g. 72> <#DATA_SPLITS, e.g. 288> <PATH/SAVE_FILE.h5 OR .pkl>
