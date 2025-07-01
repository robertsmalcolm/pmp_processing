#!/bin/bash -l
#SBATCH --mem=100G
#SBATCH --time=1:00:00
#SBATCH --qos=normal
#SBATCH -o ./clim_pmp.%j.out
#SBATCH -e ./clim_pmp.%j.err
#SBATCH --ntasks=1
#SBATCH --gres=tmp:6048
#SBATCH --export=NONE

conda activate /home/users/malcolm.roberts/.conda/envs/pmp-env

resol='MM'
annual_cycle_file='/home/users/malcolm.roberts/workspace/tenten/variability/pmp/mean_pmp/basic_annual_cycle_param_resol.py'

pcmdi_compute_climatologies.py -p $annual_cycle_file --version v20250701
