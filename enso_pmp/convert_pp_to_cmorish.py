'''
NAME:
   convert_pp_to_cmorish

DESCRIPTION:
    Make pp data CMOR-like enough to use for PMP

USAGE: 
    Execute as a script from command line

AUTHOR:
    Malcolm Roberts (hadom)

LAST MODIFIED:
    2023-11-29

'''

import iris.coord_categorisation as icc
import os, subprocess, glob
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import iris
import iris.analysis
import iris.plot as iplt
from scipy.stats import norm
from matplotlib.patches import Circle, Wedge, Polygon
from matplotlib.collections import PatchCollection

DATADIR = '/data/scratch/malcolm.roberts/'

resols = ['n96e', 'n216e', 'n640e']
resols = ['n640e']
mask_dir = '/data/users/malcolm.roberts/masks'

variables = ['ts', 'pr', 'taux']
#suites = ['u-cy163', 'u-cy021', 'u-cx993']
#suites = ['u-da156', 'u-dc396', 'u-di356']
suites = ['u-cx993']
#suite_name = ['N96O1-1', 'N216O025', 'N640O12']
suite_name = ['N640O12']
suites_future = ['u-dc015', 'u-dg002']
#years = np.arange(1850, 2100)
years = np.arange(1851, 2050)
years = np.arange(1949, 2050)
calendar = 'gregorian'
model_names = '_'.join(suites)

stash_codes = {}
stash_codes['ts'] =  '24'
stash_codes['pr'] =  '5216'
stash_codes['taux'] =  '3392'
fname_out = '{}a.pm{}_{}.{}'


def run_cmd(
        cmd,
    check=True
):
    sts = subprocess.run(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        check=check,
    )
    print('cmd ', sts.stdout)
    if sts.stderr:
        print('err ',sts.stderr)
        if 'Warning' in sts.stderr:            
            msg = (
                "Warning found in cat output ", sts.stderr
            )
            print(msg)
        else:
            msg = (
                "Error found in cat output ", sts.stderr
            )
            if check:
                raise RuntimeError(msg)
            else:
                pass
    return sts

def alt_get_file(output_dir, um_suiteid, years, variable): 
    output_files = [] # This will be used later
    stash_code = stash_codes[variable]
    year_start = str(years[0])
    year_end = str(years[-1])
    #fout = os.path.join(output_dir, fname_out.format(um_suiteid[2:], str(year), variable, 'pp'))
    #if not os.path.exists(fout):
    #print('write file ',variable, stash_code, fout)
    select_file = './select_'+variable+'_'+um_suiteid
    file = open(select_file, "w") # Create a moo select file for each variable
    file.write("begin\n")
    file.write(f'  stash={stash_code}\n')
    file.write(f'  lbproc=128\n') # global
    if calendar == 'gregorian':
        file.write(f'  lbtim=121\n') # global
    else:
        file.write(f'  lbtim=122\n') # global
    file.write(f'  yr=['+year_start+'..'+year_end+']\n') # global
    file.write("end\n")
    file.close()
        
    cmd = 'moo select -i ' + select_file + ' moose:/crum/'+ um_suiteid + '/apm.pp/ ' + output_dir
    print(cmd)
    run_cmd(cmd, check=False)

    output_files = sorted(glob.glob(os.path.join(output_dir, um_suiteid[2:]+'*.pm*.pp')))
    
    #output_files.append(fout)

    return output_files

def alt_get_file_byyear(output_dir, um_suiteid, years, variable): 
    output_files = [] # This will be used later
    stash_code = stash_codes[variable]
    year_start = str(years[0])
    year_end = str(years[-1])

    for year in np.arange(years[0], years[-1]+1):
        print('get year ',year)
        select_file = './select_'+variable+'_'+um_suiteid
        file = open(select_file, "w") # Create a moo select file for each variable
        file.write("begin\n")
        file.write(f'  stash={stash_code}\n')
        file.write(f'  lbproc=128\n') # global
        if calendar == 'gregorian':
            file.write(f'  lbtim=121\n') # global
        else:
            file.write(f'  lbtim=122\n') # global
        file.write(f'  yr='+str(year)+'\n') # global
        file.write("end\n")
        file.close()
        
        cmd = 'moo select -i ' + select_file + ' moose:/crum/'+ um_suiteid + '/apm.pp/ ' + output_dir
        print(cmd)
        run_cmd(cmd, check=False)

def read_cube(fnames, runid):
    if runid == 'obs':
        cube = iris.load_cube(fnames, 'precip')
        cubem = cube.collapsed('time', iris.analysis.MEAN)
        cube = cubem
    else:
        cube = iris.load_cube(fnames)
    return cube


def cmor_ish(fname, var):
    cmd = 'ncatted -O -a cell_measures,'+var+',a,c,"area: areacella" '+fname
    print(cmd)
    run_cmd(cmd)
    cmd = 'ncatted -O -a grid_mapping,'+var+',d,, '+fname
    print(cmd)
    run_cmd(cmd)
    cmd = 'ncatted -O -a coordinates,'+var+',d,, '+fname
    print(cmd)
    run_cmd(cmd)

    cmd = 'ncrename -O -d latitude,lat -d longitude,lon -v latitude,lat -v longitude,lon '+fname
    print(cmd)
    run_cmd(cmd)

def convert_to_nc(files, var):
    year_start = int(os.path.basename(files[0]).split('.')[1][2:6])
    year_end = int(os.path.basename(files[-1]).split('.')[1][2:6])
    dir_out = os.path.join(os.path.dirname(files[0]),'nc')
    if not os.path.exists(dir_out):
        os.makedirs(dir_out)

    files_all = []
    for year in np.arange(year_start, year_end+1):
        print('year ',year)
        file_yr = []
        for f in files:
            if int(os.path.basename(f).split('.')[1][2:6]) == year:
                file_yr.append(f)
        #print('file_yr ',file_yr)
        if len(file_yr) != 12:
            print('not 12 months in year ',year)
            continue
        fout = os.path.join(dir_out, os.path.basename(file_yr[0])[:-6]+'.nc')
        if not os.path.exists(fout):
            print('saving ',fout)
            c = iris.load_cube(file_yr)
            if var == 'taux':
                c.var_name = 'tauu'
            else:
                c.var_name = var
            iris.save(c, fout, unlimited_dimensions=['time'], netcdf_format='NETCDF3_64BIT')
        files_all.append(fout)
    
    fout_all = files_all[0][:-7]+str(year_start)+'-'+str(year_end)+'.nc'
    if not os.path.exists(fout_all):
        print('fout_all ',fout_all)
        cmd = 'ncrcat -O '+' '.join(files_all)+' '+fout_all
        print(cmd)
        run_cmd(cmd)

        cmor_ish(fout_all, var)

    return fout_all

def mask_for_pmp(resol):
    varname = 'sftlf'
    search = glob.glob(os.path.join(mask_dir, resol+'*frac_land_sea_mask.nc'))
    pmp_mask = os.path.join(mask_dir, varname+'_fx_'+resol+'_amip_r1i1p1f1.nc')
    print('pmp_mask ',pmp_mask)
    if os.path.exists(pmp_mask):
        return
    if len(search) == 1:
        c = iris.load_cube(search[0])
        c.data *= 100.
        c.var_name = varname
        c1 = iris.util.squeeze(c)
        iris.save(c1, pmp_mask, netcdf_format='NETCDF3_64BIT')
        
        cmd = 'ncatted -O -a cell_measures,'+varname+',a,c,"area: areacella" '+pmp_mask
        print(cmd)
        run_cmd(cmd)

        #cmd = 'ncwa -a time '+fname+' '+fname1
        #cmd = 'ncwa -a surface '+fname+' '+fname1
        cmd = 'ncatted -O -a coordinates,'+varname+',d,, '+pmp_mask
        print(cmd)
        run_cmd(cmd)
        cmd = 'ncatted -O -a units,'+varname+',o,c,% '+pmp_mask
        print(cmd)
        run_cmd(cmd)
        #cmd = 'ncrename -O -d latitude,lat -d longitude,lon -v latitude,lat -v longitude,lon '+pmp_mask
        cmd = 'ncrename -O -d latitude,lat -d longitude,lon '+pmp_mask
        print(cmd)
        run_cmd(cmd)
        #cmd = 'ncrename -O -d latitude,lat -d longitude,lon -v latitude,lat -v longitude,lon '+pmp_mask
        cmd = 'ncrename -O -v latitude,lat -v longitude,lon '+pmp_mask
        print(cmd)
        run_cmd(cmd)
    
if __name__ == '__main__':
    for resol in resols:
        mask_for_pmp(resol)
        stop
    
    suites_all = suites.copy()
    #suites_all.extend(suites_future)

    for run in suites_all:
        for var in variables:
            output_dir = DATADIR+'/'+run+'/'+var
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            #files_out = alt_get_file_byyear(output_dir, run, years, var)
            files_out = alt_get_file(output_dir, run, years, var)
            search = os.path.join(output_dir, run[2:]+'*.pm???????.pp')
            print(search)
            files_out = sorted(glob.glob(search))
            convert_to_nc(files_out, var)



            
