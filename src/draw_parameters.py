"""Random Drawing of (Parameter, Output Statistic) Samples for Sensitivity Analysis

Usage:
  draw_parameters.py <OUTPUT_DIR> [--job-name=<name>] [--n-simulations=<n_sim>] [--seed=<seed>] [--java-project-dir=<JPDIR>] [--output-summary-file=<OSFILE>] [--output-stat-file=<OSFILE>] [--save-all]
  draw_parameters.py (-h | --help)
  draw_parameters.py --version

Options:
  -h --help                       Show this screen.
  --version                       Show version.
  --job-name=<name>               This name is used for output indexing [default: job]
  --n-simulations=<n_sim>         Number of parameter samples generated [default: 1000].
  --seed=<seed>                   Random seed [default: 1234].
  --java-project-dir=<JPDIR>      Project directory of Contact Tracing Model Java codes
  --output-summary-file=<OSFILE>  CSV file that stores a summary of one simulation [default: Compartments.csv]
  --output-stat-file=<OSFILE>     CSV file that stores another summary of one simulation [default: stats.txt]
  --save-all                      Store all Monte Carlo samples 
  
"""

import json
import os
import sys
import numpy as np
import pandas as pd
import shutil
import time
from docopt import docopt
from os.path import expanduser, dirname, realpath, sep
from scipy.odr.odrpack import Output
sys.path.append(dirname(realpath(__file__)))
from uk.co.ramp.gencfg.disease import DiseaseSettings
from uk.co.ramp.gencfg.population import PopulationSettings
from uk.co.ramp.gencfg.isolation_policies import IsolationPolicies
from uk.co.ramp.gencfg.tracing_policies import TracingPolicies

loss_names = ['peak_severity', 'total_death', 'total_infections', 'death_to_recovery_ratio', 'person_days_in_isolation']


def losses(output_summary, output_stat):
    """
    Returns a list of negative utility, where each element is a function of the entire output time-series.
    In production, this part should be provided from an external file.
    
    Examples considerable are
        Total number of deaths
        DTW distance between the output and observations in the real world (when doing parameter estimation)
        
        
    Because output_summary is given as total population, number of death at the LAST timestamp is taken.
    About severity, here we focus on the peak value, that is hitting hospital capacity.
    """
    return [
        output_summary['sev'].max(),
        output_summary['d'].iloc[-1],
        output_summary['d'].iloc[-1] + output_summary['r'].iloc[-1],
        float(output_summary['d'].iloc[-1]) / output_summary['r'].iloc[-1],
        output_stat['Person Days in Isolation']]


if __name__ == '__main__':
    args = docopt(__doc__, version='0.0.1')
    
    def _getopt(key, default):
        return args[key] if key in args and args[key] is not None else default

    java_project_dir = _getopt('--java-project-dir', expanduser('~/git/Contact-Tracing-Model'))
    output_summary_file = _getopt('--output-summary-file', 'Compartments.csv')
    output_stat_file = _getopt('--output-stat-file', 'stats.txt')
    
    top_output_dir = _getopt('<OUTPUT_DIR>', None)
    jobname = _getopt('--job-name', 'job')
    n_simulations = int(_getopt('--n-simulations', 1000))
    seed = int(_getopt('--seed', 1234))
    save_all = _getopt('--save-all', False)
    
    try:
        os.mkdir(top_output_dir)
    except:
        pass
    
    os.chdir(java_project_dir)
    
    disease = DiseaseSettings(random_state=seed)
    population = PopulationSettings(random_state=seed)
    isopolicy = IsolationPolicies(random_state=seed, simplified=True)  # simplified=False if more complex policy space is searched for.
    tracepolicy = TracingPolicies(random_state=seed)
    
    X_columns = []
    X = []
    Y = []
    for trial in range(n_simulations):
        X_t = []

        if save_all:       
            subdir = '{}/sample{}'.format(top_output_dir, trial)
        else:
            subdir = top_output_dir
        input_dir = '{}/config'.format(subdir, trial)
        output_dir = '{}/data'.format(subdir, trial)
            
        try:
            os.mkdir(subdir)
        except:
            pass

        try:
            os.mkdir(input_dir)
        except:
            pass
        
        try:
            os.mkdir(output_dir)
        except:
            pass

        input_loc_file = '{}/input/inputLocations.json'.format(java_project_dir)
        with open(input_loc_file, 'r') as fin:
            input_locations = json.load(fin)
            
        # Create a copy of default files in input/inputLocations.json
        # For contact data we could add random noise in the future, for reflecting
        # the missing contacts not recorded in contact data.
        for key, val in input_locations.items():
            shutil.copy2('{}/input/{}'.format(java_project_dir, val), input_dir)
    
        # Each job should have a unique seed in runSettings
        run_file = '{}/runSettings.json'.format(input_dir)
        with open(run_file, 'r') as fin:
            run_sample = json.load(fin)
        run_sample['seed'] = seed + trial  # override
        with open(run_file, 'w') as fout:
            json.dump(run_sample, fout, sort_keys=True, indent=2)

        # Due to outflow/inflow of people, population should also be slightly perturbed.
        population_file = '{}/populationSettings.json'.format(input_dir)
        population_sample = population.next()
        if trial == 0:
            for key in population_sample.keys():
                X_columns.append(key)
        X_t.append(list(population_sample.values()))
        with open(population_file, 'w') as fout:
            json.dump(PopulationSettings.export(population_sample), fout, sort_keys=True, indent=2)
        
        # Disease settings are highly perturbed because they are main parameters
        disease_file = '{}/diseaseSettings.json'.format(input_dir)
        disease_sample = disease.next()
        if trial == 0:
            for key in disease_sample.keys():
                X_columns.append(key)
        X_t.append(list(disease_sample.values()))
        with open(disease_file, 'w') as fout:
            json.dump(DiseaseSettings.export(disease_sample), fout, sort_keys=True, indent=2)

        # Policy parameters are perturbed to seek out good isolation & tracing policies
        isopolicy_file = '{}/isolationPolicies.json'.format(input_dir)
        isopolicy_sample = isopolicy.next()
        if trial == 0:
            for key in isopolicy_sample.keys():
                X_columns.append(key)
        X_t.append(list(isopolicy_sample.values()))
        with open(isopolicy_file, 'w') as fout:
            json.dump(IsolationPolicies.export(isopolicy_sample), fout, sort_keys=True, indent=2)

        # Policy parameters are perturbed to seek out good isolation & tracing policies
        tracepolicy_file = '{}/tracingPolicies.json'.format(input_dir)
        tracepolicy_sample = tracepolicy.next()
        if trial == 0:
            for key in tracepolicy_sample.keys():
                X_columns.append(key)
        X_t.append(list(tracepolicy_sample.values()))
        with open(tracepolicy_file, 'w') as fout:
            json.dump(TracingPolicies.export(tracepolicy_sample), fout, sort_keys=True, indent=2)

        finished = False
        while not finished:
           exitcode = os.system("{}/build/install/ContactTracing/bin/ContactTracing --overrideInputFolderLocation={} --overrideOutputFolderLocation={} --seed={}".format(java_project_dir, input_dir, output_dir, seed + trial))
           if exitcode > 0:
               time.sleep(3)
               os.system('gradle install')
               time.sleep(3)
               continue
           else:
               finished = True
            
        X.append(np.concatenate(X_t).reshape(1, -1))
    
        # Read the summary results file and calculate the summary statistic
        output_summary = pd.read_csv('{}/{}'.format(output_dir, output_summary_file)).set_index('time')
        stat_ = pd.read_csv('{}/{}'.format(output_dir, output_stat_file), header=None).set_index(0)
        stat_.index = stat_.index.str.strip()
        output_stat = {stat_.index[i]: stat_.values.reshape(-1,)[i] for i in range(stat_.shape[0])}
        Y.append(np.array(losses(output_summary, output_stat)).reshape(1, -1))
    
    outindex = np.array(['{}.sample{}'.format(jobname, trial) for trial in range(n_simulations)])
    X = pd.DataFrame(data=np.vstack(tuple(X)), index=outindex, columns=X_columns)
    Y = pd.DataFrame(data=np.vstack(tuple(Y)), index=outindex, columns=loss_names)
    
    X.to_csv('{}/input_parameter_samples.csv'.format(top_output_dir))
    Y.to_csv('{}/output_loss_samples.csv'.format(top_output_dir))
