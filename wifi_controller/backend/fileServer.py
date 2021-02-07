import json
from os import walk

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
config_path = '../config'

CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/config', methods=['GET'])
def list_config_files():
    _, _, filenames = next(walk(config_path))
    return jsonify({
        'files': filenames
    })


@app.route('/config/<file_name>', methods=['GET', 'POST'])
def config_file(file_name):
    if request.method == 'GET':
        try:
            with open(f'{config_path}/{file_name}', 'r') as f:
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
        with open(f'{config_path}/{file_name}', 'w') as f:
            f.write(data)
        return jsonify({
            'result': 'Successfully update config file'
        })


if __name__ == '__main__':
    app.run()
