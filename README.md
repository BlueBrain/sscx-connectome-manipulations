[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![DOI:10.1101/2024.05.24.593860](http://img.shields.io/badge/DOI-10.1162/netn__a__00429-B31B1B.svg)](https://doi.org/10.1162/netn_a_00429)

# SSCx connectome manipulations

Reproduction repository for applying connectome manipulations to a detailed model of the rat somatosensory cortex (SSCx)


## Introduction

Reproduction repository with code and configuration files for applying connectome manipulations using [_Connectome-Manipulator_](https://github.com/BlueBrain/connectome-manipulator) to a detailed anatomical<sup>1</sup> and physiological<sup>2</sup> model of the rat somatosensory cortex (SSCx) in SONATA<sup>3</sup> format (released under DOI: [10.5281/zenodo.8026353](https://doi.org/10.5281/zenodo.8026353)), analyzing results, and reproducing the experiments and figures that can be found in the accompanying article<sup>4</sup>. Specifically, the following rewiring experiments and benchmarks that are described in the article are part of this repository, together with the accompanying dataset on Zenodo (DOI: [10.5281/zenodo.11402578](https://doi.org/10.5281/zenodo.11402578)).
- __Interneuron rewiring:__ Increasing the inhibitory targeting specificity of VIP+ (vasoactive intestinal peptide-expressing) interneurons, thereby transplanting connectivity trends present in the MICrONS dataset<sup>5</sup>. Functional quantification through current injection simulations.
- __Simplified connectomes:__ Progressively simplifying<sup>6</sup> connectivity among excitatory neurons. Investigating the changes in spiking synamics through re-calibration to an _in vivo_-like activity state<sup>2</sup>.
- __Performance benchmarks:__ Benchmarks tests to assess the strong and weak scaling behavior of connectome rewiring.

### References:

1. Reimann, M. W., Bolaños-Puchet, S., Courcol, J., Egas Santander, D., et al. (2024). Modeling and Simulation of Neocortical Micro- and Mesocircuitry. Part I: Anatomy. _eLife_, 13:RP99688. DOI: [10.7554/eLife.99688.1](https://doi.org/10.7554/eLife.99688.1)
2. Isbister, J. B., Ecker, A., Pokorny, C., Bolaños-Puchet, S., Egas Santander, D., et al. (2024). Modeling and Simulation of Neocortical Micro- and Mesocircuitry. Part II: Physiology and Experimentation. _eLife_, 13:RP99693. DOI: [10.7554/eLife.99693.1](https://doi.org/10.7554/eLife.99693.1)
3. Dai, K., et al. (2020). The SONATA data format for efficient description of large-scale network models. _PLOS Computational Biology_, 16(2), e1007696. DOI: [10.1371/journal.pcbi.1007696](https://doi.org/10.1371/journal.pcbi.1007696)
4. Pokorny, C., et al. (2024). A connectome manipulation framework for the systematic and reproducible study of structure-function relationships through simulations. _Network Neuroscience_. DOI: [10.1162/netn_a_00429](https://doi.org/10.1162/netn_a_00429)
5. Schneider-Mizell, C. M., et al. (2024). Cell-type-specific inhibitory circuitry from a connectomic census of mouse visual cortex. _bioRxiv_. DOI: [10.1101/2023.01.23.525290](https://doi.org/10.1101/2023.01.23.525290)
6. Gal E., et al. (2020). Neuron Geometry Underlies Universal Network Features in Cortical Microcircuits. _bioRxiv_. DOI: [10.1101/656058](https://doi.org/10.1101/656058)


## Overview

- [__interneuron_rewiring/__](interneuron_rewiring/) ... Code/configs related to the interneuron rewiring experiment
  - [__code/__](interneuron_rewiring/code/) ... Code/notebooks for setting up and running model building, rewiring, structural comparison, and analysis
  - [__configs/__](interneuron_rewiring/configs/) ... Config files and run scripts for model building, rewiring, structural comparison, simulations, and analysis
  - [__sim_configs/__](interneuron_rewiring/sim_configs/) ... Simulation config example files for running spontaneous simulations with current injection
- [__simplified_connectomes/__](simplified_connectomes/) ... Code/configs related to the simplified connectomes experiment
  - [__code/__](simplified_connectomes/code/) ... Code/notebooks for setting up and running model building, rewiring, structural comparison, validation, missing synapse estimation, and calibration
  - [__configs/__](simplified_connectomes/configs/) ... Config files and run scripts for model building, rewiring, structural comparison, simulations, and calibration
  - [__validation_configs/__](simplified_connectomes/validation_configs/) ... Config files to run model order validation
  - [__sim_configs/__](simplified_connectomes/sim_configs/) ... Simulation config template and example files for running re-calibration simulations
- [__notebooks/__](notebooks/) ... Jupyter notebooks for reproducing the structural/functional/benchmark figures in the accompanying article


## Requirements

- Python (recommended v3.10.8) and Jupyter environment
- Computation system with [Slurm Workload Manager](https://slurm.schedmd.com)


## Install

- Download and install the [Connectome-Manipulator](https://github.com/BlueBrain/connectome-manipulator) software in a Python venv
- Download the code and config files from this [sscx-connectome-manipulations](https://github.com/BlueBrain/sscx-connectome-manipulations) repo
- Download and uncompress the accompanying dataset from Zenodo (DOI: [10.5281/zenodo.11402578](https://doi.org/10.5281/zenodo.11402578))
- Download the code from the [CortexETL](https://github.com/BlueBrain/cortexetl) repo
- Download and uncompress the released SSCx network model in SONATA format from Zenodo (DOI: [10.5281/zenodo.8026353](https://doi.org/10.5281/zenodo.8026353))
- Download and uncompress the corresponding SSCx flat map from Zenodo (DOI: [10.5281/zenodo.10686776](https://doi.org/10.5281/zenodo.10686776))
- Optionally: Install additional dependencies as listed in the individual Jupyter notebooks, if needed


## How to run

### Interneuron rewiring

- __Step 1 - Structure:__
  - Follow [interneuron_rewiring_preparation.ipynb](interneuron_rewiring/code/interneuron_rewiring_preparation.ipynb) to configure and run model fitting, rewiring and structural comparison. As an output of this step, a new SONATA circuit with rewired interneuron connectivity will be created.
- __Step 2 - Function:__ Functional quantification of the rewired connectome by running network simulations with current injection.
  - __(a)__ Follow the instructions "Simulating the model" from DOI: [10.5281/zenodo.8026353](https://doi.org/10.5281/zenodo.8026353) for setting up the SSCx network model for simulations.
  - __(b)__ IMPORTANT, in case the rewired circuit from Zenodo is used: Make sure that all path references in the `circuit_config<_tc>.json` of the rewired circuit are pointing to the location of the original circuit (since only a new connectome file, i.e., `edges.h5`, is provided).
  - __(c)__ Use example simulation configs `simulation_config.json` from this repo to run simulations with different current injection strengths, as indicated by the folder name. Adapt the path under "network" pointing to the circuit config of either the original or the rewired circuit.
  - __(d)__ Follow [current_injection_analysis.ipynb](interneuron_rewiring/code/current_injection_analysis.ipynb) for simulation data analysis.

<ins>Note</ins>: All (intermediate) results from steps 1 and 2 are also contained in the Zenodo dataset.

### Simplified connectomes

- __Step 1 - Structure:__
  - __(a)__ Follow [SSCx_model_fitting.ipynb](simplified_connectomes/code/SSCx_model_fitting.ipynb) to configure and run model fitting, which will produce (simplified) stochastic model descriptions required in the subsequent rewiring step.
  - __(b)__ Follow [SSCx_rewiring.ipynb](simplified_connectomes/code/SSCx_rewiring.ipynb) to configure and run rewiring based on the stochastic model descriptions from the previous step (incl. matching the overall numbers of connections). As an output of this step, new SONATA circuits with rewired (simplified) E-to-E connectivity will be created.
  - __(c)__ Follow [SSCx_struct_comparison.ipynb](simplified_connectomes/code/SSCx_struct_comparison.ipynb) to configure and run a structural comparison of the rewired connectomes.
  - __(d)__ Follow [SSCx_model_order_validation.ipynb](simplified_connectomes/code/SSCx_model_order_validation.ipynb) to configure and run a validation of the rewired model orders.
  - __(e)__ Follow [SSCx_missing_synapses.ipynb](simplified_connectomes/code/SSCx_missing_synapses.ipynb) to compute missing afferent synapse counts.
- __Step 2 - Function:__
  - __(a)__ Follow the instructions "Simulating the model" from DOI: [10.5281/zenodo.8026353](https://doi.org/10.5281/zenodo.8026353) for setting up the SSCx network model for simulations.
  - __(b)__ Follow [SSCx_calibration.ipynb](simplified_connectomes/code/SSCx_calibration.ipynb) for iterative re-calibration and analysis of the original and rewired circuits.

<ins>Note</ins>: All (intermediate) results from steps 1 and 2 are also contained in the Zenodo dataset.

### Benchmarks

Repeatedly run rewiring as in "Simplified connectomes - Step 1b" based on the fitted 1st order stochastic connectivity model, and measure the resulting runtimes, under the following conditions:

- __Strong scaling:__
  Using 12,345 data splits*) and different numbers of processing units (CPUs) from 4 to 512 in 8 logarithmic steps.
- __Weak scaling:__
  Using 1,234 data splits*) and different network sizes by selecting the different source/target node sets "NS1.0", "NS0.5", "NS0.25", and "NS0.125" as provided in the enclosed `nodesets_weak_scaling.json` (Zenodo). Importantly, this node sets file must be set in the original SONATA circuit config under "node_sets_file".

*) Aritrary (large) numbers of data splits

<ins>Note</ins>: All benchmark results (runtimes) are also contained in the Zenodo dataset.

### Replicating figures of the accompanying article

- For replicating the structural figures (both experiments), configure and follow [notebooks/connectome_manipulator_figs_structural.ipynb](notebooks/connectome_manipulator_figs_structural.ipynb).
- For replicating the functional figures (both experiments), configure and follow [notebooks/connectome_manipulator_figs_functional.ipynb](notebooks/connectome_manipulator_figs_functional.ipynb).
- For replicating the benchmark figures, configure and follow [notebooks/connectome_manipulator_figs_benchmark.ipynb](notebooks/connectome_manipulator_figs_benchmark.ipynb).

## Citation

If you use this software, we kindly ask you to cite the following publication:

C. Pokorny, O. Awile, J.B. Isbister, K. Kurban, M. Wolf, and M.W. Reimann (2024). __A connectome manipulation framework for the systematic and reproducible study of structure–function relationships through simulations.__ Network Neuroscience. DOI: [10.1162/netn_a_00429](https://doi.org/10.1162/netn_a_00429)

```
@article{pokorny2024connectome,
  author = {Pokorny, Christoph and Awile, Omar and Isbister, James B and Kurban, Kerem and Wolf, Matthias and Reimann, Michael W},
  title = {A connectome manipulation framework for the systematic and reproducible study of structure--function relationships through simulations},
  journal = {Network Neuroscience},
  year = {2024},
  publisher={MIT Press},
  doi = {10.1162/netn_a_00429}
}
```

## Funding & Acknowledgment

The development of this software was supported by funding to the Blue Brain Project, a research center of the École polytechnique fédérale de Lausanne (EPFL), from the Swiss government’s ETH Board of the Swiss Federal Institutes of Technology.

Copyright (c) 2024 Blue Brain Project/EPFL
