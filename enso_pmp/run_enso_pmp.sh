#!/bin/bash -l
#SBATCH --mem=200G
#SBATCH --time=4:00:00
#SBATCH --qos=normal
#SBATCH -o ./enso_pmp.%j.out
#SBATCH -e ./enso_pmp.%j.err
#SBATCH --ntasks=1
#SBATCH --gres=tmp:6048
#SBATCH --export=NONE

#which conda
#conda init
conda activate /home/users/malcolm.roberts/.conda/envs/pmp-env

python -u /home/users/malcolm.roberts/workspace/tenten/variability/pmp/enso_pmp/pmp_metrics_enso.py HadGEM3-GC5E-HH

