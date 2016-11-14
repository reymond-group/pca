""" Incremental PCA for dimension reduction of large data sets.  """
import os
import argparse
import pandas as pd
import numpy as np

from sklearn.decomposition import IncrementalPCA
from sklearn.externals import joblib

PARSER = argparse.ArgumentParser(
    description='Incremental PCA for dimension reduction of large data sets.')

PARSER.add_argument('input', metavar='INPUT', type=str,
                    help='the input (csv) file')

PARSER.add_argument('output', metavar='OUTPUT', type=str,
                    help='the output (csv) file')

PARSER.add_argument('-d', '--delimiter', type=str, default=',',
                    help='use DELIMITER instead of \',\' for field delimiter')

PARSER.add_argument('-k', '--dimensions', type=int, default=3,
                    help='use DIMENSIONS instead of 3 as the number of dimensions' +
                    ' to reduce the data to')

PARSER.add_argument('-m', '--model', type=str, default='',
                    help='the filename of the model file to be loaded, if empty, the model ' +
                    'will be created and then saved as OUTPUT.')

PARSER.add_argument('-c', '--chunksize', type=int, default=50000,
                    help='the number of lines to be read from the INPUT file ' +
                    'at a time and stored in memory, the default value is 50000')

ARGS = PARSER.parse_args()

ARGS.output = os.path.splitext(ARGS.output)[0]

READER = pd.read_csv(ARGS.input, sep=ARGS.delimiter, chunksize=ARGS.chunksize)

PCA = IncrementalPCA(n_components=ARGS.dimensions)

if ARGS.model and os.path.isfile(ARGS.model):
    PCA = joblib.load(ARGS.model)
else:
    for chunk in READER:
        PCA.partial_fit(chunk)
    if ARGS.model:
        if not ARGS.model.endswith('.pkl'):
            ARGS.model += '.pkl'
        joblib.dump(PCA, ARGS.model)

np.savetxt(ARGS.output + '-means.csv', PCA.mean_, delimiter=',')
np.savetxt(ARGS.output + '-vars.csv', PCA.var_, delimiter=',')

with open(ARGS.output + '.csv', 'a+') as f:
    for chunk in pd.read_csv(ARGS.input, sep=ARGS.delimiter, chunksize=ARGS.chunksize):
        transformed_chunk = PCA.transform(chunk)
        pd.DataFrame(transformed_chunk).to_csv(f, header=False, index=False)
