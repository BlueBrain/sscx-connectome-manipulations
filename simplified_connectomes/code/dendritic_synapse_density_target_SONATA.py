# Description:   Extracts dendritic E/I synapse densities (#synapses/um) for each neuron within a given circuit target in isolation
#                => To be used with SONATA circuits (requires Blue Brain SNAP)
# Author:        C. Pokorny
# Created:       02/02/2024 (from dendritic_synapse_density_target.py, 27/04/2021)
# Last modified: 05/02/2024


import os
import sys
import time
import warnings

import neurom as nm
import numpy as np
import pandas as pd

from bluepysnap import Circuit
from datetime import datetime
from joblib import Parallel, delayed

from bluepysnap.exceptions import BluepySnapDeprecationWarning


# SONATA section type mapping: 0 = soma, 1 = axon, 2 = basal, 3 = apical
SEC_TYPE_MAP = {nm.AXON: 1, nm.BASAL_DENDRITE: 2, nm.APICAL_DENDRITE: 3}
DD_TYPES = [SEC_TYPE_MAP[_dd] for _dd in [nm.BASAL_DENDRITE, nm.APICAL_DENDRITE]]


# Creates data splits [for parallel processing]
def create_data_splits(circuit_config, nodes_popul, circuit_target, N_split):
    
    # Load circuit
    circuit = Circuit(circuit_config)
    nodes = circuit.nodes[nodes_popul]
    cell_ids = nodes.ids(circuit_target)
    cell_ids_split = np.split(cell_ids, np.cumsum([np.ceil(len(cell_ids) / N_split).astype(int)] * (N_split - 1)))

    print(f'INFO: Created {N_split} data splits for {circuit_config} using nodes population "{nodes_popul}" and target "{circuit_target}" with {len(cell_ids)} cells', flush=True)

    return cell_ids_split


# Create table with cell positions and dentritic synapse density for given set of GIDs [for easy parallelization]
def create_cell_table(circuit_config, nodes_popul, circuit_target, nids, morph_ext='asc'):

    # Disable deprecation/user warnings
    warnings.filterwarnings('ignore', category=BluepySnapDeprecationWarning)
    warnings.filterwarnings('ignore', category=UserWarning)

    # Load circuit
    circuit = Circuit(circuit_config)
    nodes = circuit.nodes[nodes_popul]
    pre_cell_ids = nodes.ids(circuit_target)
    num_cells = len(nids)

    # Load edges populations (only the ones projecting to nodes_popul)
    edges_populs_all = circuit.edges.population_names
    edges_populs = []
    is_local_popul = []
    for pop in edges_populs_all:
        edges = circuit.edges[pop]
        if edges.target.name == nodes_popul:
            edges_populs.append(pop)
            if edges.source.name == nodes_popul:
                is_local_popul.append(True)
            else:
                is_local_popul.append(False)

    print(f'INFO: Creating cell table for {num_cells} cells: {nids[:3]}..{nids[-3:]}', flush=True)
    print(f'INFO: {len(edges_populs)} edges populations:')
    for pop, is_loc in zip(edges_populs, is_local_popul):
        print(f'      * "{pop}" ({"local" if is_loc else "projection"})')

    # Extract cell positions
    cell_table = nodes.get(nids, properties=['x', 'y', 'z'])

    # Get dendrite length & number of afferent (dendritic) synapses
    cell_table.insert(column='total_dendrite_length', value=np.nan, loc=cell_table.shape[1])

    for pop, is_loc in zip(edges_populs, is_local_popul):
        if is_loc:  # Distinguish E/I synapses
            cell_table.insert(column=pop + '__E_count', value=-1, loc=cell_table.shape[1])
            cell_table.insert(column=pop + '__I_count', value=-1, loc=cell_table.shape[1])
        else:  # Only one type of synapses
            cell_table.insert(column=pop + '__count', value=-1, loc=cell_table.shape[1])

    for idx, nid in enumerate(nids):
        # Query morphology
        morph_file = nodes.morph.get_filepath(nid, extension=morph_ext)
        nrn = nm.load_morphology(morph_file)
        cell_table.at[nid, 'total_dendrite_length'] = nm.get('total_length', nrn, neurite_type=nm.BASAL_DENDRITE) + nm.get('total_length', nrn, neurite_type=nm.APICAL_DENDRITE)

        # Query connectivity (for local connectivity: only within given circuit target in isolation!)
        for pop, is_loc in zip(edges_populs, is_local_popul):
            edges = circuit.edges[pop]
            if is_loc:  # Local connectivity (distinguish between E/I synapses)
                syn = edges.afferent_edges(nid, properties=['@source_node', 'syn_type_id', 'afferent_section_type'])
                syn = syn[np.isin(syn['@source_node'], pre_cell_ids)]
                dd_sel = np.isin(syn['afferent_section_type'], DD_TYPES)
                cell_table.at[nid, pop + '__E_count'] = np.sum(np.logical_and(dd_sel, syn['syn_type_id'] >= 100))
                cell_table.at[nid, pop + '__I_count'] = np.sum(np.logical_and(dd_sel, syn['syn_type_id'] < 100))
            else:  # 'afferent_section_type' not available; assume only one type of synapses, targeting dendrites
                cell_table.at[nid, pop + '__count'] = len(edges.afferent_edges(nid))

        # Progress
        if idx == 0 or np.mod(idx + 1, np.floor(len(nids) / 5).astype(int)) == 0:
            print(f'PROGRESS [GIDs {nids[0]}..{nids[-1]}]: {np.round(100 * (idx + 1) / len(nids)).astype(int)}%', flush=True)
    
    # Compute dendritic synapse density
    for pop, is_loc in zip(edges_populs, is_local_popul):
        if is_loc:  # Local connectivity (distinguish between E/I synapses)
            cell_table.insert(column=pop + '__E_density', value=cell_table[pop + '__E_count'] / cell_table['total_dendrite_length'], loc=cell_table.shape[1])
            cell_table.insert(column=pop + '__I_density', value=cell_table[pop + '__I_count'] / cell_table['total_dendrite_length'], loc=cell_table.shape[1])
        else:
            cell_table.insert(column=pop + '__density', value=cell_table[pop + '__count'] / cell_table['total_dendrite_length'], loc=cell_table.shape[1])

    return cell_table


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        circuit_config = sys.argv[1]
        nodes_popul = sys.argv[2]

        if len(sys.argv) >= 4:
            circuit_target = sys.argv[3]
        else:
            circuit_target = 'All'

        if len(sys.argv) >= 5:
            N_jobs = int(sys.argv[4])
        else:
            N_jobs = 1 # No parallelization

        if len(sys.argv) >= 6:
            N_split = int(sys.argv[5])
        else:
            N_split = N_jobs
        assert N_split >= N_jobs, 'ERROR: Number of data splits too low for given number of parallel jobs!'

        if len(sys.argv) >= 7:
            save_file = sys.argv[6]
        else:
            save_file = "./cell_table.h5"
        file_ext = os.path.splitext(save_file)[-1]
        assert file_ext.lower() in ['.pkl', '.h5'], 'ERROR: Only save file formats .pkl or .h5 supported!'

        # Process
        t_start = time.time()
        cell_ids_split = create_data_splits(circuit_config, nodes_popul, circuit_target, N_split)
        cell_table = pd.concat(Parallel(n_jobs=N_jobs, verbose=100)(delayed(create_cell_table)(circuit_config, nodes_popul, circuit_target, cell_ids_split[idx]) for idx in range(N_split)))
        print(f'INFO: Total time elapsed ({cell_table.shape[0]} cells): {time.time() - t_start:.0f}s')

        # Save table
        save_date = datetime.today().strftime('%Y%m%d_%H%M%S')
        save_file = f'{os.path.splitext(save_file)[0]}__{save_date}{file_ext}'
        if file_ext.lower() == '.pkl':
            cell_table.to_pickle(save_file)
        elif file_ext.lower() == '.h5':
            cell_table.to_hdf(save_file, 'cell_table')
        print(f'INFO: Cell table saved to "{save_file}"', flush=True)

    else:
        print('Extracts dendritic synapse density (#synapses/um) for each neuron within given nodes population (optionally, within given circuit target) from a SONATA circuit')
        print('Usage: dendritic_synapse_density_target_SONATA PATH_TO_CONFIG NODES_POPUL_NAME <CIRCUIT_TARGET> <#PARALLEL_JOBS> <#DATA_SPLITS> <PATH/SAVE_FILE.h5 OR .pkl>')
