from flask import Flask, request, jsonify, render_template
from datetime import datetime
import os

app = Flask(__name__)

cell_data = {}

def load_cell_data():
    global cell_data
    with open('cell_data.txt', 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            cell_type, mcc, mnc, lac, cell_id, _, lon, lat, *_ = parts
            key = (cell_id, mcc, mnc, lac)  
            cell_data[key] = {'lat': float(lat), 'lon': float(lon)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/iot-data', methods=['POST'])
def receive_data():
    data = request.get_json()

    ids = data.get('ID', [])
    mcc = data.get('MCC', [])
    mnc = data.get('MNC', [])
    lac = data.get('LAC', [])

    updated_cells = []
    for i in range(len(ids)):
        cell_key = (str(ids[i]), str(mcc[i]), str(mnc[i]), str(lac[i]))
        if cell_key in cell_data:
            updated_cells.append(cell_data[cell_key])

    return jsonify({'status': 'success', 'message': 'Data received', 'cells': updated_cells})

@app.route('/latest')
def latest_data():
    return jsonify(cell_data)

if __name__ == '__main__':
    load_cell_data()
    app.run(host='0.0.0.0', port=5000)
