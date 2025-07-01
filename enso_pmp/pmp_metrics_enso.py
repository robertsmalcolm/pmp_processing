'''
Code in e.g. /home/users/malcolm.roberts/.conda/envs/pmp-env/lib/python3.10/site-packages/pcmdi_metrics/graphics/share/Metrics_enso.py
/home/users/malcolm.roberts/.conda/envs/pmp-env/lib/python3.10/site-packages/EnsoMetrics
File has -1.0e30 values over land, rather than missing data (1.0e20)
/data/users/malcolm.roberts/pcmdi_metrics//demo_data/obs4MIPs_PCMDI_monthly/MOHC/HadISST-1-1/mon/ts/gn/v20210727/ts_mon_HadISST-1-1_PCMDI_gn_187001-201907.nc
'''

# To open and display one of the graphics
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib import rcParams

import os, glob, sys

suite = sys.argv[1]
# This is where you will be downloading the sample_data
demo_data_directory = "/data/users/malcolm.roberts/pcmdi_metrics/"
# this line is where your output will be stored
demo_output_directory = "/data/users/malcolm.roberts/pcmdi_metrics/"

#param_file_in = '/data/users/malcolm.roberts/git/pcmdi_metrics/doc/jupyter/Demo/basic_enso_param_MO_'+suite+'.py.in'
param_file_in = '/home/users/malcolm.roberts/workspace/tenten/variability/pmp/enso_pmp/basic_enso_param_MO_model.py.in'

def generate_parameter_files(demo_data_directory, demo_output_directory, filenames=[]):
    # This prepares the various parameter files used in the demo notebooks
    # to reflect where you downloaded the data
    sub_dict = {"INPUT_DIR": demo_data_directory, "OUTPUT_DIR": demo_output_directory, "MODEL_NAME": suite}
    if len(filenames) < 1:
        filenames = glob.glob("*.in")
    for name in filenames:
        with open(name) as template_file:
            print("Preparing parameter file: {}".format(name[:-3]))
            template = template_file.read()
            for key in sub_dict:
                template = template.replace("${}$".format(key), sub_dict[key])
            with open(name[:-3], "w") as param_file:
                param_file.write(template)

    print("Saving User Choices")
    with open("user_choices.py", "w") as f:
        print("demo_data_directory = '{}'".format(demo_data_directory), file=f)
        print("demo_output_directory = '{}'".format(demo_output_directory), file=f)

def generate_param_file(param_file_in):
    filenames=[param_file_in]
    generate_parameter_files(demo_data_directory, demo_output_directory, filenames=filenames)
    filenames_processed = filenames[0][:-3]
    with open(filenames_processed) as f:
        print(f.read())
    return filenames_processed

def ENSO_perf(param_file):
    cmd = 'enso_driver.py -p '+param_file
    os.system(cmd)

def ENSO_coll(param_file, collection):
    cmd = 'enso_driver.py -p '+param_file+' --metricsCollection '+collection+' --results_dir '+demo_output_directory+'/basicTestEnso/'+collection+' --nc_out True'
    os.system(cmd)

def work():
    param_file = generate_param_file(param_file_in)
    ENSO_perf(param_file)

    for coll in ['ENSO_tel', 'ENSO_proc']:
        ENSO_coll(param_file, coll)

if __name__ == '__main__':
    work()
