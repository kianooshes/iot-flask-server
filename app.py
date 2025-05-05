from flask import Flask, request, jsonify, render_template
from datetime import datetime
import os

app = Flask(__name__)

last_data = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/iot-data', methods=['POST'])
def receive_data():
    global last_data
    data = request.get_json()

    if 'lat' in data:
        data['latitude'] = data.pop('lat')
    if 'lon' in data:
        data['longitude'] = data.pop('lon')

    data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    last_data = data
    return jsonify({'status': 'success', 'message': 'Data received', 'data': data})


@app.route('/latest')
def latest_data():
    if last_data:
        return jsonify(last_data)
    else:
        return jsonify({'latitude': None, 'longitude': None, 'timestamp': None})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

