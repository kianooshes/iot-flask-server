from flask import Flask, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)

last_data = {}

@app.route('/')
def index():
    return "Server is up and running!"

@app.route('/iot-data', methods=['POST'])
def receive_data():
    global last_data
    data = request.get_json()  

    if 'ID' not in data or 'MCC' not in data or 'MNC' not in data or 'LAC' not in data:
        return jsonify({'status': 'error', 'message': 'Missing data fields'}), 400

    data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    last_data = data

    return jsonify({'status': 'success', 'message': 'Data received', 'data': data}), 200

@app.route('/latest', methods=['GET'])
def latest_data():
    if last_data:
        return jsonify(last_data), 200
    else:
        return jsonify({'status': 'error', 'message': 'No data available'}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
