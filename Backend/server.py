from flask import Flask, jsonify, request
from traffic import generate_route, compute_travel_time, generate_traffic_data
from walk import compute_walk_time, compute_walk_route

app = Flask(__name__)

@app.route('/generate_route', methods=['GET'])
def generate_route_api():
    """
    API endpoint to generate the optimal route from start to end based on traffic data at a specific hour.
    
    Inputs:
    - start: A tuple representing the starting point in the format (x, y).
    - end: A tuple representing the ending point in the format (x, y).
    - hour: The hour at which the travel is happening.
    
    Outputs:
    - route: List of tuples representing the path from start to end.
    
    Example URL:
    http://localhost:5000/generate_route?hour=12&start=[0,0]&end=[99,99]
    """
    hour = float(request.args.get('hour'))
    start = tuple(map(int, request.args.get('start').strip('[]').split(',')))
    end = tuple(map(int, request.args.get('end').strip('[]').split(',')))
    route = generate_route(start, end, hour)
    return jsonify({"route": route})

@app.route('/compute_travel_time', methods=['GET'])
def compute_travel_time_api():
    """
    API endpoint to compute the travel time for a route based on traffic data at a specific hour.
    
    Inputs:
    - start: A tuple representing the starting point in the format (x, y).
    - end: A tuple representing the ending point in the format (x, y).
    - hour: The hour at which the travel is happening.
    
    Outputs:
    - travel_time: The estimated travel time in minutes from the starting point to the ending point.
    
    Example URL:
    http://localhost:5000/compute_travel_time?hour=12&start=[0,0]&end=[99,99]
    """
    hour = float(request.args.get('hour'))
    start = tuple(map(int, request.args.get('start').strip('[]').split(',')))
    end = tuple(map(int, request.args.get('end').strip('[]').split(',')))
    travel_time = compute_travel_time(generate_route(start, end, hour), hour)
    return jsonify({"travel_time": travel_time})

@app.route('/generate_traffic_data', methods=['POST'])
def generate_traffic_data_api():
    """
    API endpoint to generate a 2D array of traffic coefficients for the city at a specific hour.
    
    Inputs (JSON):
    - hour: The hour for which traffic data is required.
    - city_size (optional): The size of the city grid. Defaults to 100.
    
    Outputs:
    - traffic_data: 2D array of traffic coefficients.
    
    Example POST data:
    {
        "hour": 12,
        "city_size": 100
    }
    """
    data = request.json
    hour = data.get('hour')
    city_size = data.get('city_size', 100)
    traffic_data = generate_traffic_data(hour, city_size)
    return jsonify({"traffic_data": traffic_data.tolist()})

@app.route('/ping', methods=['GET', 'POST'])
def api():
    """
    Generic API endpoint for testing GET and POST requests.
    
    For GET:
    - Returns the 'param' query parameter from the URL.
    
    For POST:
    - Returns the JSON data sent in the request body.
    
    Example URL (GET):
    http://localhost:5000/ping?param=test
    
    Example POST data:
    {
        "key": "value"
    }
    """
    if request.method == 'GET':
        param = request.args.get('param', None)
        return jsonify({"message": f"You sent the parameter: {param}"})
    elif request.method == 'POST':
        data = request.json
        return jsonify({"message": f"You sent the data: {data}"})
   
@app.route('/compute_walk_time', methods=['GET'])
def compute_walk_time_api():
    """
    API endpoint to compute the walk time from start to end based on the Manhattan distance and average walking speed.
    
    Inputs:
    - start: A tuple representing the starting point in the format (x, y). Extracted from the request parameter 'start'.
    - end: A tuple representing the ending point in the format (x, y). Extracted from the request parameter 'end'.
    
    Outputs:
    - walk_time: The estimated walking time in minutes from the starting point to the ending point.
    
    Example URL:
    http://localhost:5000/compute_walk_time?start=[0,0]&end=[99,99]
    """
    # Extract start and end points from the request parameters
    start = tuple(map(int, request.args.get('start').strip('[]').split(',')))
    end = tuple(map(int, request.args.get('end').strip('[]').split(',')))
    
    # Compute the walk time
    walk_time = compute_walk_time(start, end)
    
    return jsonify({"walk_time": walk_time})

@app.route('/compute_walk_route', methods=['GET'])
def compute_walk_route_api():
    """
    API endpoint to compute the walk route from start to end based on the Manhattan distance.
    
    Inputs:
    - start: A tuple representing the starting point in the format (x, y). Extracted from the request parameter 'start'.
    - end: A tuple representing the ending point in the format (x, y). Extracted from the request parameter 'end'.
    
    Outputs:
    - walk_route: A list of tuples representing the route from start to end.
    
    Example URL:
    http://localhost:5000/compute_walk_route?start=[0,0]&end=[99,99]
    """
    # Extract start and end points from the request parameters
    start = tuple(map(int, request.args.get('start').strip('[]').split(',')))
    end = tuple(map(int, request.args.get('end').strip('[]').split(',')))
    
    # Compute the walk route
    walk_route = compute_walk_route(start, end)
    
    return jsonify({"walk_route": walk_route})



#TODO: 
# 1. Return 5 Travel Options
    # 1.1. Travel Time
        # 1.1.1. Train
        # 1.1.2. Uber
        # 1.1.3. Walk
    # 1.2. Travel Cost
        # 1.2.1. Train
        # 1.2.2. Uber
        # 1.2.3. Walk
        # 1.2.4. Tax
    # 1.3. Eco-Friendliness
        # 1.3.1. Train
        # 1.3.2. Uber
        # 1.3.3. Walk
    # 1.4. Train Route + Walk Route + Uber Route
        # 1.4.1. Train Route
        # 1.4.2. Walk Route
        # 1.4.3. Uber Route
    # 1.5. Time to Uber Arrival