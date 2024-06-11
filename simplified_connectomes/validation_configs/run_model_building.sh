#!/bin/bash -l
#SBATCH --job-name=model_build
#SBATCH --time=16:00:00
#SBATCH --account=proj83
#SBATCH --partition=prod
#SBATCH --mem=0
#SBATCH --exclusive
#SBATCH --constraint=cpu

module purge
module load unstable
# module load py-connectome-manipulator/0.0.6  # "tables" dependency missing!!
source /gpfs/bbp.cscs.ch/home/pokorny/ReWiringKernel/bin/activate
connectome-manipulator build-model $1 $2 $3

# EXAMPLE HOW TO RUN: sbatch run_model_building.sh <model_config.json> [--force-reextract] [--force-rebuild]
# e.g. sbatch run_model_building.sh model_config.json --force-reextract --force-rebuild
