from flask import Flask, request, jsonify, render_template
from datetime import datetime

app = Flask(__name__)

last_data = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/iot-data', methods=['POST'])
def receive_data():
    global last_data
    data = request.get_json()
    data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    last_data = data
    return jsonify({'status': 'success', 'message': 'Data received', 'data': data})

@app.route('/latest')
def latest_data():
    if last_data:
        return jsonify(last_data)
    else:
        return jsonify({'temperature': None, 'humidity': None, 'timestamp': None})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
