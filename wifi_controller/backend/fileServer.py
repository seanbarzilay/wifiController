import json
import os
from os import listdir

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
config_path = '/var/config'

CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/config', methods=['GET'])
def list_config_files():
    filenames = listdir(config_path)
    return jsonify({
        'files': filenames
    })


@app.route('/config/<file_name>', methods=['GET', 'POST'])
def config_file(file_name):
    if request.method == 'GET':
        try:
            file_path = os.path.realpath(os.path.join(config_path, file_name))
            if not file_path.startswith(os.path.realpath(config_path) + os.sep):
                return jsonify({'error': 'Invalid file name'}), 400
            with open(file_path, 'r') as f:
                data = f.read()
                return jsonify({
                    'data': data
                })
        except FileNotFoundError:
            return jsonify(({
                'data': ''
            }))
    else:
        data = json.loads(request.data.decode())['text']
        file_path = os.path.realpath(os.path.join(config_path, file_name))
        if not file_path.startswith(os.path.realpath(config_path) + os.sep):
            return jsonify({'error': 'Invalid file name'}), 400
        with open(file_path, 'w') as f:
            f.write(data)
        return jsonify({
            'result': 'Successfully update config file'
        })


def main():
    app.run(host='0.0.0.0')


if __name__ == '__main__':
    main()
