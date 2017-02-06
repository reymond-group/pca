import sys
import os
import argparse
import pandas as pd
import numpy as np
import flask
import scipy

from flask_cors import CORS, cross_origin

from sklearn.decomposition import IncrementalPCA
from sklearn.externals import joblib

# Initialize the Flask application
app = flask.Flask(__name__)
CORS(app)

app.config.update(
    PROPAGATE_EXCEPTIONS='DEBUG'
)

def scale(x, minimum, maximum, a, b) :
    return (((b - a) * (x - minimum)) / (maximum - minimum)) + a

if len(sys.argv) < 2:
    print('Please provide a directory containing the models.')
    print('Usage: ' + sys.argv[0] + ' /directory/to/models/')
    sys.exit()

port = 8080
if len(sys.argv) > 2:
    port = int(sys.argv[2])

model_dir = sys.argv[1]

if not model_dir.endswith('/'):
    model_dir += '/'

# For GET, show a simple message
@app.route('/')
def form():
    return flask.render_template('index.html')

# The POST request doing the incremental pca
@app.route('/', methods=['POST'])
def ipca():
    json = flask.request.get_json(silent=True)

    if (json is None) or ('database' not in json) or ('fingerprint' not in json) or ('dimensions' not in json):
        return flask.jsonify({'success': False, 'error': 'Malformed request.'})

    database = json['database']
    fingerprint = json['fingerprint']
    dimensions = json['dimensions']
    data = json['data']
    binning = json['binning']
    resolution = json['resolution']

    model_file = database + '.' + fingerprint + '.' + str(dimensions) + '.pkl'
    min_max_file = database + '.' + fingerprint + '.' + str(dimensions) + '.minmax'
    path = model_dir + database + '/' + fingerprint + '/' + str(dimensions) + '/'
    
    if not os.path.isfile(path + model_file):
        return flask.jsonify({'success': False, 'error': 'Transformation not available.'})
    if binning and not os.path.isfile(path + min_max_file):
        return flask.jsonify({'success': False, 'error': 'Min-Max file not found. Provide the file or run without binning.'})

    pca = joblib.load(path + model_file)

    transformed_data = None

    try:
        transformed_data = pca.transform(data).tolist()
        if binning: 
            min_max = pd.read_csv(path + min_max_file, header=None)
            for i, v in enumerate(transformed_data):
                for j, c in enumerate(v):
                    transformed_data[i][j] = int(scale(c, min_max[0][j], min_max[1][j], 0, resolution))


    except:
        return flask.jsonify({'success': False, 'error': 'Could not transform data. Do the fingerprints match the selected model?'})

    # Scale the data
    

    return flask.jsonify({
        'success': True,
        'database': database,
        'fingerprint': fingerprint,
        'dimensions': dimensions,
        'binning': binning,
        'resolution': resolution,
        'data': transformed_data
    })
    
# Run the app
if __name__ == '__main__':
    app.run(
        host = '0.0.0.0',
        port = port
    )
