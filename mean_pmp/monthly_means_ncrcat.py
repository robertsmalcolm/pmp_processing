import os
import glob

#vars = ['pr', 'rlut', 'rsdt', 'rsut', 'tas', 'ts', 'psl', 'tauu']
vars = ['pr', 'psl', 'rlds',  'rlus',  'rlut',  'rlutcs',  'rsds',  'rsdscs',  'rsdt',  'rsut',  'rsutcs',  'tas',  'tauu',  'ts']
vars = ['ta', 'ua', 'va', 'zg']

resol = 'MM'

fname_format = '/data/users/malcolm.roberts/CMIP6/GCModelDev/DECK/MOHC/HadGEM3-GC5E-{resol}/historical/r1i1p1f1/Amon/{var}/gn/embargoed/v20250409/{var}_Amon_HadGEM3-GC5E-{resol}_historical_r1i1p1f1_gn_{year}.nc'

fout_format = '/data/users/malcolm.roberts/CMIP6/GCModelDev/DECK/MOHC/HadGEM3-GC5E-{resol}/historical/r1i1p1f1/Amon/{var}/gn/{var}_Amon_HadGEM3-GC5E-{resol}_historical_r1i1p1f1_gn_195001-201412.nc'
#fout_format = '/data/users/malcolm.roberts/CMIP6/GCModelDev/DECK/MOHC/HadGEM3-GC5E-{resol}/historical/r1i1p1f1/Amon/{var}/gn/{var}_Amon_HadGEM3-GC5E-{resol}_historical_r1i1p1f1_gn_193001-197912.nc'

for var in vars:
    #fnames_19 = fname_format.format(var=var, year='19[579]*', resol=resol)
    #fnames_20 = fname_format.format(var=var, year='20*', resol=resol)
    #fout = fout_format.format(var=var, resol=resol)
    fnames_19 = fname_format.format(var=var, year='19[56789]*', resol=resol)
    fnames_20 = fname_format.format(var=var, year='20*', resol=resol)
    fout = fout_format.format(var=var, resol=resol)
    if not os.path.exists(fout):
        cmd = 'ncrcat -O '+fnames_19+' '+fnames_20+' '+fout
        #cmd = 'ncrcat -O '+fnames_19+' '+fout
        print(cmd)
        os.system(cmd)
    
