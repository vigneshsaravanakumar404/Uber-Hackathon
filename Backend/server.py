from flask import Flask, jsonify, request
from car import generate_route, time_to_uber, car_cost, environment_tax
from walk import compute_walk_time, compute_walk_route, walk_cost
from station import train_travel_time

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

@app.route('/main', methods=['GET'])
def main_api():
    """
    API endpoint to list the 4 travel options from start to end based on traffic data at a specific hour
    
    Inputs:
    - start: A tuple representing the starting point in the format (x, y)
    - end: A tuple representing the ending point in the format (x, y)
    - time: A tuple representing the time of the day in the format (hour, minute)
    
    Outputs:
    - route: List of tuples representing the path from start to end.
    
    Example URL:
    http://localhost:5000/main?start=[0,0]&end=[99,99]&time=[12,30]
    """
    
    # Input
    start = tuple(map(int, request.args.get('start').strip('[]').split(',')))
    end = tuple(map(int, request.args.get('end').strip('[]').split(',')))
    time = tuple(map(int, request.args.get('time').strip('[]').split(',')))
    
    # Variables
    hour = round(time[0] + time[1]/60)

    # Full Walk
    walk_time = compute_walk_time(start, end)
    walk_route = compute_walk_route(start, end)
    walk_cost = 0
    walk_wait_time = 0
    walk_env_tax = 0

    # Full Uber
    uber_time = time_to_uber(start, end, hour)
    uber_route = generate_route(start, end, hour)
    uber_cost = car_cost(start, end, hour)
    uber_wait_time = time_to_uber()
    uber_env_tax = environment_tax(start, end, hour)

    # Train + Walk
    train_walk_env_tax = 0

    # Train + Uber
    #TODO: To be coded

    # output
    # return as JSON


#TODO: Sub Functions
# Functions To Be Coded: 
    # Train Wait Time
    # Train Cost

#TODO: Other
    # Remove other API calls
    # Code main method in computation.py
    
