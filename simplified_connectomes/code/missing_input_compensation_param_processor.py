# This file is part of sscx-connectome-manipulations.
# 
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2024 Blue Brain Project/EPFL

# Description:   BBP-WORKFLOW parameter processor functions used to generate SSCx simulation campaigns
# Author:        J. Isbister
# Last modified: 2022-2023

import numpy as np
import pandas as pd
from scipy.interpolate import griddata
from scipy.optimize import curve_fit
from scipy.stats import linregress
import math

scaling_and_data_neuron_class_keys = {
    "L1I":"L1_INH", "L1_5HT3aR":"L1_5HT3aR",
    "L23E":"L23_EXC",
    "L23I":"L23_INH", "L23_PV":"L23_PV", "L23_SST":"L23_SST", "L23_5HT3aR":"L23_5HT3aR",
    "L4E":"L4_EXC",
    "L4I":"L4_INH", "L4_PV":"L4_PV", "L4_SST":"L4_SST", "L4_5HT3aR":"L4_5HT3aR",
    "L5E":"L5_EXC",
    "L5I":"L5_INH", "L5_PV":"L5_PV", "L5_SST":"L5_SST", "L5_5HT3aR":"L5_5HT3aR",
    "L6E":"L6_EXC",
    "L6I":"L6_INH", "L6_PV":"L6_PV", "L6_SST":"L6_SST", "L6_5HT3aR":"L6_5HT3aR"
}


# Used for fitting exponential
# between unconn and conn FRs
# i.e. phi: U_FR -> C_FR
def fit_exponential(x, y):

    popt, pcov = curve_fit(
        lambda t, a, b, c: a * np.exp(b * t) + c,
        x, y, p0=(1.0, 0.5, y.min() - 1), 
        maxfev=20000)
    return popt


# Used for applying 
# phi inverse: C_FR -> U_FR
def calculate_suggested_unconnected_firing_rate(target_connected_fr, 
                                                            a, b, c):
    log_domain = max((target_connected_fr - c) / a, 1.0)
    return math.log(log_domain) / b



def ou_parameters_for_target_unconn_frs(desired_unconnected_fr, unconn_df, neuron_class, depol_stdev_mean_ratio):

    nc_unconn_df = unconn_df[unconn_df["neuron_class"] == neuron_class]
    gradient_line_x = np.linspace(0,100,1000)
    gradient_line_y = gradient_line_x * depol_stdev_mean_ratio
    predicted_frs_for_line = griddata(nc_unconn_df[['mean', 'stdev']].to_numpy(), nc_unconn_df["data"], (gradient_line_x, gradient_line_y), method='cubic')
    index_of_closest_point = np.nanargmin(abs(predicted_frs_for_line - desired_unconnected_fr))
    closest_ou_mean = round(gradient_line_x[index_of_closest_point], 3)
    closest_ou_std = round(gradient_line_y[index_of_closest_point], 3)

    return closest_ou_mean, closest_ou_std



def set_input_compensation_for_desired_frs(*, 
                                        path, 
                                        ca, 
                                        depol_stdev_mean_ratio, 
                                        desired_connected_proportion_of_invivo_frs, 
                                        data_for_unconnected_fit_name, 
                                        data_for_connected_adjustment_fit_name, 
                                        in_vivo_reference_frs,
                                        unconnected_connected_fr_adjustment_fit_method='exponential', 
                                        **kwargs):

    final_params = {}

    # Read unconnected DF
    unconn_df = pd.read_parquet(path=data_for_unconnected_fit_name)

    if (data_for_connected_adjustment_fit_name != ''):
        # Load connected firing rate data
        unconn_conn_df = pd.read_parquet(path=data_for_connected_adjustment_fit_name)
        
        # Filter + preprocess
        filtered_unconn_conn_df = unconn_conn_df[(unconn_conn_df['ca']==ca) 
                            & (unconn_conn_df['depol_stdev_mean_ratio']==depol_stdev_mean_ratio) 
                            & (unconn_conn_df["window"] == 'conn_spont') 
                            & (unconn_conn_df['bursting'] == False)]


        filtered_unconn_conn_df["invivo_fr"] = filtered_unconn_conn_df['desired_connected_fr'] / filtered_unconn_conn_df['desired_connected_proportion_of_invivo_frs']
        filtered_unconn_conn_df = filtered_unconn_conn_df[filtered_unconn_conn_df['mean_of_mean_firing_rates_per_second'] < filtered_unconn_conn_df['invivo_fr'] * 1.05]
    
    # Iterate neuron classes to find determine target unconnected and connected firing rates
    for neuron_class_key, in_vivo_fr in in_vivo_reference_frs.items():

        neuron_class = scaling_and_data_neuron_class_keys[neuron_class_key]
        desired_connected_fr = desired_connected_proportion_of_invivo_frs*in_vivo_fr

        if (data_for_connected_adjustment_fit_name == ''):
            # If first iteration, unconnected FRs equal target connected FRs
            desired_unconnected_fr = desired_connected_fr

        else:
            # Fit exponential to unconnected vs connected FRs
            nc_filtered_unconn_conn_df = filtered_unconn_conn_df[filtered_unconn_conn_df['neuron_class']==neuron_class]
            if (unconnected_connected_fr_adjustment_fit_method == 'exponential'):            
                popt = fit_exponential(nc_filtered_unconn_conn_df['desired_unconnected_fr'], nc_filtered_unconn_conn_df['mean_of_mean_firing_rates_per_second'])
                desired_unconnected_fr = calculate_suggested_unconnected_firing_rate(desired_connected_fr, popt[0], popt[1], popt[2])


        # Find OU mean and std for target unconnected fr
        closest_ou_mean, closest_ou_std = ou_parameters_for_target_unconn_frs(desired_unconnected_fr, unconn_df, neuron_class, depol_stdev_mean_ratio)

        # Fill params dictionary
        final_params.update({f'desired_connected_fr_{neuron_class_key}': desired_connected_fr})
        final_params.update({f'desired_unconnected_fr_{neuron_class_key}': desired_unconnected_fr})
        final_params.update({f'ornstein_uhlenbeck_mean_pct_{neuron_class_key}': closest_ou_mean})
        final_params.update({f'ornstein_uhlenbeck_sd_pct_{neuron_class_key}': closest_ou_std})

    return final_params
