"""Concatenating the CSV files of random parameter and output draws.

Usage:
  unify_draws.py <DIRLIST_FILE> <OUTPUT_DIR>
  unify_draws.py (-h | --help)
  unify_draws.py --version

Options:
  -h --help                       Show this screen.
  --version                       Show version.
  
"""

import os
import sys
import numpy as np
import pandas as pd
from docopt import docopt
from os.path import dirname, realpath
sys.path.append(dirname(realpath(__file__)))

if __name__ == '__main__':
    args = docopt(__doc__, version='0.0.1')
    
    def _getopt(key, default):
        return args[key] if key in args and args[key] is not None else default

    input_file = _getopt('<DIRLIST_FILE>', None)
    output_dir = _getopt('<OUTPUT_DIR>', None)
    try:
        os.mkdir(output_dir)
    except:
        pass
    
    with open(input_file, "r") as fin:
        dirlist = fin.read().splitlines()
    
    X = []
    Y = []
    for indir in dirlist:
        X_i = pd.read_csv('{}/input_parameter_samples.csv'.format(indir), index_col=0)
        Y_i = pd.read_csv('{}/output_loss_samples.csv'.format(indir), index_col=0)
        X.append(X_i)
        Y.append(Y_i)
    X = pd.concat(X, axis=0)
    Y = pd.concat(Y, axis=0)
    
    X.to_csv('{}/input_parameter_samples.csv'.format(output_dir))
    Y.to_csv('{}/output_loss_samples.csv'.format(output_dir))
