#!/bin/bash -l
#SBATCH --job-name=conn_rewire
#SBATCH --partition=prod
#SBATCH --nodes=5
#SBATCH --tasks-per-node=18
#SBATCH --cpus-per-task=4
#SBATCH --mem=0
#SBATCH --exclusive
#SBATCH --time=0:15:00
#SBATCH --account=proj83
#SBATCH --out=logs/%j.txt
#SBATCH --err=logs/%j.txt

. /etc/profile.d/modules.sh
unset MODULEPATH
. /gpfs/bbp.cscs.ch/ssd/apps/bsd/config/modules.sh
module purge
module load archive/2023-07 python-dev parquet-converters/0.8.0 py-mpi4py
# module load py-connectome-manipulator/0.0.6  # "tables" dependency missing
source /gpfs/bbp.cscs.ch/home/pokorny/ReWiringKernel/bin/activate

set -x

srun dplace parallel-manipulator -v manipulate-connectome $1 --output-dir=$2 --parallel --profile --splits=$3

# EXAMPLE HOW TO RUN: sbatch run_rewiring_parallel.sh <model_config.json> <output_dir> <num_splits>
# e.g. sbatch run_rewiring.sh manip_config.json /gpfs/.../O1v5-SONATA__Rewired 100
#
# IMPORTANT: Don't launch from within another SLURM allocation!!
