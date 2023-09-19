from flask import Flask, jsonify, request
from car import generate_route, time_to_uber, car_cost, environment_tax, compute_travel_time
from walk import compute_walk_time, compute_walk_route, walk_cost
from station import Station
from math import sqrt
import random

app = Flask(__name__)

# Background Computation
stations = []
for i in range(10, 100, 10):  
    for j in range(10, 100, 10):  
        stations.append(Station(i, j))

def euclidean_distance(point1, point2):
    return sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def find_nearest_station(start, stations):
    nearest_station = min(stations, key=lambda station: euclidean_distance(start, (station.x, station.y)))
    return nearest_station

def coords_to_str(route):
    return ', '.join([f"({x},{y})" for x, y in route])

def generate_train_wait_time():
    mean = 5.75
    std_dev = 1.75
    min_wait = 0
    max_wait = mean * 2

    wait_time = random.gauss(mean, std_dev)

    # Clip the wait time to be within the min and max limits
    wait_time = max(min_wait, min(max_wait, wait_time))

    return wait_time


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

    # Computations
    nearest_station_start = find_nearest_station(start, stations)
    nearest_station_end = find_nearest_station(end, stations)

    # Walk
    walk_time = compute_walk_time(start, end)
    walk_route = compute_walk_route(start, end)
    walk_cost = 0
    walk_env_tax = 0

    # Uber
    uber_route_1 = generate_route(start, end, hour)
    uber_time_1 = compute_travel_time(uber_route_1, hour)  # Changed this line
    uber_cost_1 = car_cost(start, end, hour)
    uber_wait_time_1 = time_to_uber()  # Changed this line
    uber_env_tax_1 = environment_tax(start, end, hour)
    
    total_time_1 = uber_time_1 + uber_wait_time_1
    total_cost_1 = uber_cost_1 + uber_env_tax_1
    total_env_tax_1 = uber_env_tax_1


    #TODO Walk + Train + Walk
    walk_time_start_2 = compute_walk_time(start, (nearest_station_start.x, nearest_station_start.y))
    walk_time_end_2 = compute_walk_time((nearest_station_end.x, nearest_station_end.y), end)
    train_time_2 = nearest_station_start.train_travel_time(nearest_station_end)
    train_route_2 = nearest_station_start.train_route(nearest_station_end)
    train_cost_2 = len(train_route_2) * 0.1
    train_wait_time_2 = generate_train_wait_time()
    train_env_tax_2 = 0
    walk_env_tax_2 = 0

    total_time_2 = walk_time_start_2 + train_time_2 + train_wait_time_2 + walk_time_end_2
    total_cost_2 = walk_cost + train_cost_2 + train_env_tax_2 + walk_env_tax
    total_env_tax_2 = train_env_tax_2 + walk_env_tax
    walk_route_start_2 = compute_walk_route(start, (nearest_station_start.x, nearest_station_start.y))
    walk_route_end_2 = compute_walk_route((nearest_station_end.x, nearest_station_end.y), end)
    

    # Walk + Train + Uber
    walk_time_start_4 = compute_walk_time(start, (nearest_station_start.x, nearest_station_start.y))
    uber_route_end_4 = generate_route((nearest_station_end.x, nearest_station_end.y), end, hour)
    uber_time_end_4 = compute_travel_time(uber_route_end_4, hour)
    uber_cost_end_4 = car_cost((nearest_station_end.x, nearest_station_end.y), end, hour)
    uber_wait_time_end_4 = time_to_uber()
    uber_env_tax_end_4 = environment_tax((nearest_station_end.x, nearest_station_end.y), end, hour)
    total_time_4 = walk_time_start_4 + train_time_2 + train_wait_time_2 + uber_time_end_4 + uber_wait_time_end_4
    total_cost_4 = walk_cost + train_cost_2 + train_env_tax_2 + uber_cost_end_4 + uber_env_tax_end_4
    total_env_tax_4 = train_env_tax_2 + uber_env_tax_end_4
    walk_route_start_4 = compute_walk_route(start, (nearest_station_start.x, nearest_station_start.y))

    # Uber + Train + Walk
    uber_route_start_5 = generate_route(start, (nearest_station_start.x, nearest_station_start.y), hour)
    uber_time_start_5 = compute_travel_time(uber_route_start_5, hour)
    uber_cost_start_5 = car_cost(start, (nearest_station_start.x, nearest_station_start.y), hour)
    uber_wait_time_start_5 = time_to_uber()
    uber_env_tax_start_5 = environment_tax(start, (nearest_station_start.x, nearest_station_start.y), hour)
    walk_time_end_5 = compute_walk_time((nearest_station_end.x, nearest_station_end.y), end)
    total_time_5 = uber_time_start_5 + uber_wait_time_start_5 + train_time_2 + train_wait_time_2 + walk_time_end_5
    total_cost_5 = uber_cost_start_5 + uber_env_tax_start_5 + train_cost_2 + train_env_tax_2 + walk_cost
    total_env_tax_5 = uber_env_tax_start_5 + train_env_tax_2
    walk_route_end_5 = compute_walk_route((nearest_station_end.x, nearest_station_end.y), end)

    # Uber + Train + Uber
    uber_route_start_3 = generate_route(start, (nearest_station_start.x, nearest_station_start.y), hour)
    uber_time_start_3 = compute_travel_time(uber_route_start_3, hour)
    uber_cost_start_3 = car_cost(start, (nearest_station_start.x, nearest_station_start.y), hour)
    uber_wait_time_start_3 = time_to_uber()

    uber_route_end_3 = generate_route((nearest_station_end.x, nearest_station_end.y), end, hour)
    uber_time_end_3 = compute_travel_time(uber_route_end_3, hour)
    uber_cost_end_3 = car_cost((nearest_station_end.x, nearest_station_end.y), end, hour)
    uber_wait_time_end_3 = time_to_uber()

    uber_env_tax_3 = environment_tax(start, (nearest_station_start.x, nearest_station_start.y), hour) + environment_tax((nearest_station_end.x, nearest_station_end.y), end, hour)

    train_time_3 = nearest_station_start.train_travel_time(nearest_station_end)
    train_route_3 = nearest_station_start.train_route(nearest_station_end)
    train_cost_3 = len(train_route_3) * 0.1
    train_wait_time_3 = generate_train_wait_time()
    train_env_tax_3 = 0

    total_time_3 = uber_time_start_3 + uber_wait_time_start_3 + train_time_3 + train_wait_time_3 + uber_time_end_3 + uber_wait_time_end_3
    total_cost_3 = uber_cost_start_3 + uber_cost_end_3 + train_cost_3 + train_env_tax_3
    total_env_tax_3 = train_env_tax_3 + uber_env_tax_3


    # Return JSON
    return jsonify({
        'Walk': {'time': walk_time, 'cost': walk_cost, 'env_tax': walk_env_tax, 'route': coords_to_str(walk_route)},
        'Uber': {'time': total_time_1, 'cost': total_cost_1, 'env_tax': total_env_tax_1, 'route': coords_to_str(uber_route_1)},
        'Walk_Train_Walk': {'time': total_time_2, 'cost': total_cost_2, 'env_tax': total_env_tax_2, 'route': f"{coords_to_str(walk_route_start_2)}|{coords_to_str(train_route_2)}|{coords_to_str(walk_route_end_2)}"},
        'Uber_Train_Uber': {'time': total_time_3, 'cost': total_cost_3, 'env_tax': total_env_tax_3, 'route': f"{coords_to_str(uber_route_start_3)}|{coords_to_str(train_route_3)}|{coords_to_str(uber_route_end_3)}"},
        'Walk_Train_Uber': {'time': total_time_4, 'cost': total_cost_4, 'env_tax': total_env_tax_4, 'route': f"{coords_to_str(walk_route_start_4)}|{coords_to_str(train_route_2)}|{coords_to_str(uber_route_end_4)}"},
        'Uber_Train_Walk': {'time': total_time_5, 'cost': total_cost_5, 'env_tax': total_env_tax_5, 'route': f"{coords_to_str(uber_route_start_5)}|{coords_to_str(train_route_2)}|{coords_to_str(walk_route_end_5)}"}
    })


