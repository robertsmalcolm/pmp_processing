import os

#
#  OPTIONS ARE SET BY USER IN THIS FILE AS INDICATED BELOW BY:
#
#

# VARIABLES TO USE
vars = ['pr', 'psl', 'rlds',  'rlus',  'rlut',  'rlutcs',  'rsds',  'rsdscs',  'rsdt',  'rsut',  'rsutcs',  'tas',  'tauu',  'ts']
vars = ['ta', 'ua', 'va', 'zg']

resol = 'MM'

# START AND END DATES FOR CLIMATOLOGY
start = '1950-01'
end = '2014-12'

# INPUT DATASET - CAN BE MODEL OR OBSERVATIONS
#infile = '/data/users/malcolm.roberts/pcmdi_metrics/demo_data/obs4MIPs_PCMDI_monthly/NASA-LaRC/CERES-EBAF-4-1/mon/rlut/gn/v20210727/rlut_mon_CERES-EBAF-4-1_PCMDI_gn_200301-201812.nc'

# MM, HH need ncrcat to upper directory
if resol != 'LL':
    infile = '/data/users/malcolm.roberts/CMIP6/GCModelDev/DECK/MOHC/HadGEM3-GC5E-'+resol+'/historical/r1i1p1f1/Amon/%(variable)/gn/%(variable)_Amon_HadGEM3-GC5E-'+resol+'_historical_r1i1p1f1_gn_195001-201412.nc'
else:
    # LL already has this time period
    infile = '/data/users/malcolm.roberts/CMIP6/GCModelDev/DECK/MOHC/HadGEM3-GC5E-'+resol+'/historical/r1i1p1f1/Amon/%(variable)/gn/embargoed/v20250409/%(variable)_Amon_HadGEM3-GC5E-'+resol+'_historical_r1i1p1f1_gn_195001-201412.nc'

# DIRECTORY WHERE TO PUT RESULTS
#outfile = '/data/users/malcolm.roberts/pcmdi_metrics/demo_output/climo/rlut_mon_CERES-EBAF-4-1_BE_gn.nc'
#outfile = '/data/users/malcolm.roberts/pcmdi_metrics/demo_output/GC5c_demo_clims/rlut_mon_GC5c-N96ORCA1_BE_gn.nc'
outfile = '/data/users/malcolm.roberts/pcmdi_metrics/EERIE_output/GC5E_clims/%(variable)_mon_GC5E-'+resol+'_BE_gn.nc'
