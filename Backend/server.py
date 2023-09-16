from flask import Flask, jsonify, request
from traffic import generate_route, compute_travel_time, generate_traffic_data


app = Flask(__name__)

# Assuming you have the methods defined somewhere, either include them in this file or import them.
# For example:
# from your_module import generate_route, compute_travel_time, generate_traffic_data

@app.route('/generate_route', methods=['GET'])
def generate_route_api():
    hour = float(request.args.get('hour'))
    start = tuple(map(int, request.args.get('start').strip('[]').split(',')))
    end = tuple(map(int, request.args.get('end').strip('[]').split(',')))
    route = generate_route(start, end, hour)
    return jsonify({"route": route})

@app.route('/compute_travel_time', methods=['GET'])
def compute_travel_time_api():
    hour = float(request.args.get('hour'))
    start = tuple(map(int, request.args.get('start').strip('[]').split(',')))
    end = tuple(map(int, request.args.get('end').strip('[]').split(',')))
    travel_time = compute_travel_time(generate_route(start, end, hour), hour)
    return jsonify({"travel_time": travel_time})


@app.route('/generate_traffic_data', methods=['POST'])
def generate_traffic_data_api():
    data = request.json
    hour = data.get('hour')
    city_size = data.get('city_size', 100)
    traffic_data = generate_traffic_data(hour, city_size)
    return jsonify({"traffic_data": traffic_data.tolist()})  # Convert numpy array to list

@app.route('/api', methods=['GET', 'POST'])
def api():
    if request.method == 'GET':
        param = request.args.get('param', None)
        return jsonify({"message": f"You sent the parameter: {param}"})
    elif request.method == 'POST':
        data = request.json
        return jsonify({"message": f"You sent the data: {data}"})