""" Incremental PCA for dimension reduction of large data sets.  """
import os
import argparse
import numpy as np
import matplotlib.colors

from pandas import read_csv, DataFrame
from numpy.random import seed
from sklearn.preprocessing import minmax_scale, robust_scale, quantile_transform
from sklearn.model_selection import train_test_split
from keras.layers import Input, Dense
from keras.models import Model
from keras import regularizers

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

ARGS = PARSER.parse_args()

read_csv(ARGS.input, sep=ARGS.delimiter, header=None, error_bad_lines=False)

df_X = read_csv('drugbank.morgan', sep=';')

# SCALE EACH FEATURE INTO [0, 1] RANGE
#X = minmax_scale(df_X, axis = 0)
X = df_X.as_matrix().astype('float32')
# Y = quantile_transform(df_Y, axis = 0)
# Y = df_Y.as_matrix()
# Y = Y[:,0]
ncol = X.shape[1]
X_train, X_test = train_test_split(X, train_size = 0.25, random_state = seed(2017))


inputs = Input(shape = (ncol, ))
# DEFINE THE DIMENSION OF ENCODER ASSUMED 3
encoding_dim = ARGS.dimensions


# DEFINE THE ENCODER LAYER
encoded1 = Dense(1500, activation = 'relu')(inputs)
encoded2 = Dense(256, activation = 'relu')(encoded1)
encoded3 = Dense(128, activation = 'sigmoid')(encoded2)
encoded4 = Dense(64, activation = 'sigmoid')(encoded3)
encoded5 = Dense(32, activation = 'sigmoid')(encoded4)
encoded6 = Dense(16, activation = 'sigmoid')(encoded5)
encoded7 = Dense(encoding_dim, activation = 'sigmoid')(encoded6)
# DEFINE THE DECODER LAYERS
decoded1 = Dense(16, activation = 'relu')(encoded7)
decoded2 = Dense(32, activation = 'relu')(decoded1)
decoded3 = Dense(64, activation = 'relu')(decoded2)
decoded4 = Dense(128, activation = 'relu')(decoded3)
decoded5 = Dense(256, activation = 'relu')(decoded4)
decoded6 = Dense(1500, activation = 'relu')(decoded5)
decoded7 = Dense(ncol, activation = 'sigmoid')(decoded6)
# COMBINE ENCODER AND DECODER INTO AN AUTOENCODER MODEL
autoencoder = Model(inputs, decoded7)


# Vanilla
# encoded = Dense(encoding_dim, activation='relu')(inputs)
# decoded = Dense(ncol)(encoded)
# autoencoder = Model(inputs, decoded)


# CONFIGURE AND TRAIN THE AUTOENCODER
autoencoder.compile(optimizer = 'adam', loss = 'binary_crossentropy')
autoencoder.fit(X_train, X_train, epochs = 50, batch_size = 100, shuffle = True, validation_data = (X_test, X_test))
# THE ENCODER TO EXTRACT THE REDUCED DIMENSION FROM THE ABOVE AUTOENCODER
encoder = Model(inputs, decoded7)
encoded_input = Input(shape = (encoding_dim, ))
encoded_out = encoder.predict(X)

with open(ARGS.output, 'a+') as f:
    DataFrame(encoded_out).to_csv(f, header=None, index=False)
