[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![DOI:10.1101/2024.05.24.593860](http://img.shields.io/badge/DOI-10.1101/2024.05.24.593860-B31B1B.svg)](https://doi.org/10.1101/2024.05.24.593860)

# SSCx connectome manipulations

Reproduction repository for applying connectome manipulations to a detailed model of the rat somatosensory cortex (SSCx)


## Introduction

Reproduction repository with code and configuration files for applying connectome manipulations using [_Connectome-Manipulator_](https://github.com/BlueBrain/connectome-manipulator) to a detailed anatomical<sup>1</sup> and physiological<sup>2</sup> model of the rat somatosensory cortex (SSCx) in SONATA<sup>3</sup> format (released under [doi: 10.5281/zenodo.8026353](https://doi.org/10.5281/zenodo.8026353)), analyzing results, and reproducing the experiments and figures that can be found in the accompanying article<sup>4</sup>. Specifically, the following two rewiring experiments that are described in the article are included:
- __Interneuron rewiring:__ Increasing the inhibitory targeting specificity of VIP+ (vasoactive intestinal peptide-expressing) interneurons, thereby transplanting connectivity trends present in the MICrONS dataset<sup>5</sup>. Functional quantification through current injection simulations.
- __Simplified connectomes:__ Progressively simplifying<sup>6</sup> connectivity among excitatory neurons. Investigating the changes in spiking synamics through re-calibration to an _in vivo_-like activity state.

### References:

1. Reimann, M. W., Bolaños-Puchet, S., Courcol, J., Egas Santander, D., et al. (2022). Modeling and Simulation of Neocortical Micro- and Mesocircuitry. Part I: Anatomy. _bioRxiv_. [doi: 10.1101/2022.08.11.503144](https://doi.org/10.1101/2022.08.11.503144)
2. Isbister, J. B., Ecker, A., Pokorny, C., Bolaños-Puchet, S., Egas Santander, D., et al. (2023). Modeling and Simulation of Neocortical Micro- and Mesocircuitry. Part II: Physiology and Experimentation. _bioRxiv_. [doi: 10.1101/2023.05.17.541168](https://doi.org/10.1101/2023.05.17.541168)
3. Dai, K., et al. (2020). The SONATA data format for efficient description of large-scale network models. _PLoS Comput Biol_, 16(2), e1007696.[doi: 10.1371/journal.pcbi.1007696](https://doi.org/10.1371/journal.pcbi.1007696)
4. Pokorny, C., et al. (2024). A connectome manipulation framework for the systematic and reproducible study of structure-function relationships through simulations. _bioRxiv_. [doi: 10.1101/2024.05.24.593860](https://doi.org/10.1101/2024.05.24.593860)
5. Schneider-Mizell, C. M., et al. (2024). Cell-type-specific inhibitory circuitry from a connectomic census of mouse visual cortex. _bioRxiv_. [doi: 10.1101/2023.01.23.525290](https://doi.org/10.1101/2023.01.23.525290)
6. Gal E., et al. (2020). Neuron Geometry Underlies Universal Network Features in Cortical Microcircuits. _bioRxiv_. [doi: 10.1101/656058](https://doi.org/10.1101/656058)


## Install

- Download and install the [Connectome-Manipulator](https://github.com/BlueBrain/connectome-manipulator) software
- Download the code and config files from this [sscx-connectome-manipulations](https://github.com/BlueBrain/sscx-connectome-manipulations) repo
- Download the accompanying dataset from [Zenodo](https://zenodo.org/)


## Overview

- [__interneuron_rewiring/__](interneuron_rewiring/) ... Code/configs related to the interneuron rewiring experiment
  - [__code/__](interneuron_rewiring/code/) ... Code/notebooks for setting up model building, rewiring, structural comparison, and analysis
  - [__configs/__](interneuron_rewiring/configs/) ... Config files and run scripts for model building, rewiring, structural comparison, simulations, and analysis
- [__simplified_connectomes/__](simplified_connectomes/) ... Code/configs related to the simplified connectomes experiment
  - [__code/__](simplified_connectomes/code/) ... Code/notebooks for setting up model building, rewiring, structural comparison, and calibration
  - [__configs/__](simplified_connectomes/configs/) ... Config files and run scripts for model building, rewiring, structural comparison, simulations, and calibration
- [__notebooks/__](notebooks/) ... Jupyter notebooks for reproducing the structural/functional figures in the accompanying article


## How to run

### Interneuron rewiring

- __Step 1:__ Follow [interneuron_rewiring_preparation.ipynb](interneuron_rewiring/code/interneuron_rewiring_preparation.ipynb) to configure and run model fitting, rewiring and structural comparison. As an output of this step, a new SONATA circuit with rewired interneuron connectivity will be created.
- __Step 2:__ Functional quantification of the rewired connectome by running network simulations with current injection.
  - (a) Follow the instructions "Simulating the model" from [doi: 10.5281/zenodo.8026353](https://doi.org/10.5281/zenodo.8026353) for setting up the SSCx network model for simulations.
  - (b) In case the rewired circuit from Zenodo is used: Make sure that all path references in the `circuit_config<_tc>.json` of the rewired circuit are pointing to the location of the original circuit (since only the connectome, i.e., `edges.h5`, is different).
  - (c) Adapt paths and use example simulation configs from this repo to run simulations.

<ins>Note</ins>: All (intermediate) results from steps 1 and 2 are also contained in the Zenodo dataset.

### Simplified connectomes

### Replicating figures of the accompanying article

- For replicating the structural figures, configure and run [notebooks/connectome_manipulator_figs_structural.ipynb](notebooks/connectome_manipulator_figs_structural.ipynb)

- For replicating the functional figures, configure and run [notebooks/connectome_manipulator_figs_functional.ipynb](notebooks/connectome_manipulator_figs_functional.ipynb)


## Citation

If you use this software, we kindly ask you to cite the following publication:

C. Pokorny, O. Awile, J.B. Isbister, K. Kurban, M. Wolf, and M.W. Reimann (2024). __A connectome manipulation framework for the systematic and reproducible study of structure-function relationships through simulations.__ bioRxiv 2024.05.24.593860. [doi: 10.1101/2024.05.24.593860](https://doi.org/10.1101/2024.05.24.593860)

```
@article{pokorny2024connectome,
  author = {Pokorny, Christoph and Awile, Omar and Isbister, James B and Kurban, Kerem and Wolf, Matthias and Reimann, Michael W},
  title = {A connectome manipulation framework for the systematic and reproducible study of structure--function relationships through simulations},
  journal = {bioRxiv},
  year = {2024},
  publisher={Cold Spring Harbor Laboratory},
  doi = {10.1101/2024.05.24.593860}
}
```

## Funding & Acknowledgment

The development of this software was supported by funding to the Blue Brain Project, a research center of the École polytechnique fédérale de Lausanne (EPFL), from the Swiss government’s ETH Board of the Swiss Federal Institutes of Technology.

Copyright (c) 2024 Blue Brain Project/EPFL
