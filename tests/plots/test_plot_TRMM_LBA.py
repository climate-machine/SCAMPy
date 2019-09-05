import sys, os
PS = os.sep
code_path = os.path.dirname(os.path.realpath(__file__))
while not code_path.endswith('SCAMPy'):
    code_path = os.path.dirname(code_path)
    if not 'SCAMPy' in code_path: break
code_path = code_path+PS
test_path = code_path+PS+'tests'+PS
plot_path = code_path+PS+'tests'+PS+'plots'+PS
sys.path.insert(0, code_path)
sys.path.insert(0, test_path)
sys.path.insert(0, plot_path)

import os
import subprocess
import json
import warnings

from netCDF4 import Dataset

import pytest
import numpy as np

import main as scampy
import common as cmn
import plot_scripts as pls

@pytest.fixture(scope="module")
def sim_data(request):

    # generate namelists and paramlists
    setup = cmn.simulation_setup('TRMM_LBA')

    # run scampy
    scampy.main1d(setup["namelist"], setup["paramlist"])

    # simulation results
    sim_data = Dataset(setup["outfile"], 'r')

    # remove netcdf file after tests
    request.addfinalizer(cmn.removing_files)

    return sim_data

def test_plot_TRMM_LBA(sim_data):
    """
    plot TRMM_LBA profiles
    """
    data_to_plot = cmn.read_data_avg(sim_data, n_steps=100)

    pls.plot_mean(data_to_plot,   "TRMM_LBA_quicklook.pdf")
    pls.plot_drafts(data_to_plot, "TRMM_LBA_quicklook_drafts.pdf")

def test_plot_timeseries_TRMM_LBA(sim_data):
    """
    plot timeseries
    """
    data_to_plot = cmn.read_data_srs(sim_data)

    pls.plot_timeseries(data_to_plot, "TRMM_LBA")

def test_plot_timeseries_1D_TRMM_LBA(sim_data):
    """
    plot TRMM_LBA 1D timeseries
    """
    data_to_plot = cmn.read_data_timeseries(sim_data)

    pls.plot_timeseries_1D(data_to_plot, "TRMM_LBA_timeseries_1D.pdf")

def test_plot_var_covar_TRMM_LBA(sim_data):
    """
    plot TRMM LBA var covar
    """
    data_to_plot = cmn.read_data_avg(sim_data, n_steps=100, var_covar=True)

    pls.plot_var_covar_mean(data_to_plot,       "TRMM_LBA_var_covar_mean.pdf")
    pls.plot_var_covar_components(data_to_plot, "TRMM_LBA_var_covar_components.pdf")
