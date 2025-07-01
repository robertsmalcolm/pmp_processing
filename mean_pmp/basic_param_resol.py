import os

#
#  OPTIONS ARE SET BY USER IN THIS FILE AS INDICATED BELOW BY:
#
#

# RUN IDENTIFICATION
# DEFINES A SUBDIRECTORY TO METRICS OUTPUT RESULTS SO MULTIPLE CASES CAN
# BE COMPARED
case_id = 'N216_clim'
#case_id = 'N96_clim'
#case_id = 'N640_clim'

# LIST OF MODEL VERSIONS TO BE TESTED - WHICH ARE EXPECTED TO BE PART OF
# CLIMATOLOGY FILENAME
if case_id == 'N640_clim':
    test_data_set = ['GC5E-HH']
elif case_id == 'N216_clim':
    test_data_set = ['GC5E-MM']
elif case_id == 'N96_clim':
    test_data_set = ['GC5E-LL']

# VARIABLES TO USE
vars = ['pr', 'psl', 'rlds',  'rlus',  'rlut',  'rlutcs',  'rsds',  'rsdscs',  'rsdt',  'rsut',  'rsutcs',  'tas',  'tauu',  'ts']
#vars = ['ts']
vars = ['ta_200', 'ta_850', 'ua_200', 'va_200', 'zg_500']

# Observations to use at the moment "default" or "alternate"
#reference_data_set = ['all']
reference_data_set = ['default']
reference_data_set = ['all']
#custom_observations = '/data/users/malcolm.roberts/pcmdi_metrics/demo_data_obs/PMP_obs4MIPsClims/PMP_obs4MIPsClims_catalogue_byVar_v20250305.json'

#ext = '.nc'

# INTERPOLATION OPTIONS
target_grid = '2.5x2.5'  # OPTIONS: '2.5x2.5' or an actual cdms2 grid object
regrid_tool = 'regrid2'  # 'regrid2' # OPTIONS: 'regrid2','esmf'
# OPTIONS: 'linear','conservative', only if tool is esmf
regrid_method = 'linear'
regrid_tool_ocn = 'esmf'    # OPTIONS: "regrid2","esmf"
# OPTIONS: 'linear','conservative', only if tool is esmf
regrid_method_ocn = 'linear'

# Templates for climatology files
# %(param) will subsitute param with values in this file
#filename_template = "cmip5.historical.%(model_version).r1i1p1.mon.%(variable).198101-200512.AC.v20200426.nc"
#filename_template = "%(variable)_mon_%(model_version)_BE_gn.193001-197912.AC.v20250420.nc"
#filename_template = "%(variable)_mon_%(model_version)_BE_gn.193001-197912.AC.v20250503.nc"
filename_template = "%(variable)_mon_%(model_version)_BE_gn.195001-201412.AC.v20250701.nc"

# filename template for landsea masks ('sftlf')
sftlf_filename_template = "sftlf_%(model_version).nc"
generate_sftlf = True # if land surface type mask cannot be found, generate one

# Region
# if not set, will try and do many regions
regions = {}
for var in vars:
    regions[var] = ['global']

# ROOT PATH FOR MODELS CLIMATOLOGIES
test_data_path = '/data/users/malcolm.roberts/pcmdi_metrics/EERIE_output/GC5E_clims'
# ROOT PATH FOR OBSERVATIONS
# Note that atm/mo/%(variable)/ac will be added to this
reference_data_path = '/data/users/malcolm.roberts/pcmdi_metrics/demo_data/obs4MIPs_PCMDI_clims'
reference_data_path = '/data/users/malcolm.roberts/pcmdi_metrics/demo_data_obs/PMP_obs4MIPsClims/'
# setting this points to json file with REF paths
custom_observations = '/data/users/malcolm.roberts/pcmdi_metrics/demo_data_obs/PMP_obs4MIPsClims/PMP_obs4MIPsClims_catalogue_byVar_v20250305.json'

# DIRECTORY WHERE TO PUT RESULTS
metrics_output_path = os.path.join(
    '/data/users/malcolm.roberts/pcmdi_metrics/demo_output',
    "%(case_id)")
