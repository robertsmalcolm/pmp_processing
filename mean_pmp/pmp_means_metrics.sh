#!/bin/bash -l
#SBATCH --mem=100G
#SBATCH --time=1:00:00
#SBATCH --qos=normal
#SBATCH -o ./clim_metrics_pmp.%j.out
#SBATCH -e ./clim_metrics_pmp.%j.err
#SBATCH --ntasks=1
#SBATCH --gres=tmp:6048
#SBATCH --export=NONE

conda activate /home/users/malcolm.roberts/.conda/envs/pmp-env

#pcmdi_compute_climatologies.py -p /data/users/malcolm.roberts/git/pcmdi_metrics/doc/jupyter/Demo/basic_annual_cycle_param_N640.py

python /home/users/malcolm.roberts/workspace/tenten/variability/pmp/mean_pmp/pmp_mean_driver.py
