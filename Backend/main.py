from flask import Flask, jsonify, request
import matplotlib.pyplot as plt
from station import Station
from server import app
import numpy as np
import random
import math
import datetime
import heapq
from multiprocessing import Process, Pipe

# Background Methods
BASE_TRAFFIC_VARIATION = 0.25
SEARCH_RADIUS = 10

def gaussian(x, mu, sigma):
    """Gaussian function to model the base traffic coefficient."""
    g = math.exp(-((x - mu)**2) / (2 * sigma**2))
    # Scale and shift to ensure the output is between 0.05 and 1
    return 0.05 + 0.95 * g

def get_traffic_variation_bounds(hour):
    """
    Adjust the traffic variation bounds based on the time of day using a sinusoidal function.
    Peaks at 7-9 AM and 5-7 PM.
    """
    radian_conversion = 2 * math.pi / 24
    time_in_radians = hour * radian_conversion
    
    # Adjust the amplitude of the sinusoidal functions to ensure they don't push the coefficient out of the desired range
    overall_traffic_level = 0.45 * math.sin(2 * time_in_radians - 7 * radian_conversion)
    sinusoidal_variation = 0.005 * math.sin(3 * time_in_radians - 7 * radian_conversion)
    
    lower_bound = BASE_TRAFFIC_VARIATION - overall_traffic_level - sinusoidal_variation
    upper_bound = BASE_TRAFFIC_VARIATION + overall_traffic_level + sinusoidal_variation
    
    return (lower_bound, upper_bound)

def traffic_coefficient(x, y, hour, city_size=100):
    """
    Calculate the base traffic coefficient for a point based on its distance from the center.
    Adjusts for time of day.
    """
    center = city_size / 2
    distance_from_center = math.sqrt((x - center)**2 + (y - center)**2)
    max_distance = math.sqrt(2 * center**2)
    
    base_coeff = gaussian(distance_from_center, 0, max_distance / 3)
    
    lower_bound, upper_bound = get_traffic_variation_bounds(hour)
    variation = 1 + random.uniform(-lower_bound, upper_bound)
    final_coeff = base_coeff * variation
    
    return final_coeff

def generate_traffic_data(hour, city_size=100):
    """
    Generate a 2D array of traffic coefficients for the city.
    """
    traffic_data = np.zeros((city_size, city_size))
    for i in range(city_size):
        for j in range(city_size):
            traffic_data[i, j] = traffic_coefficient(i, j, hour)
    return traffic_data

def get_traffic_coefficient(x, y, hour):

    return traffic_data[round(hour)][x][y]

def dijkstra(graph, start, end, hour):
    """
    Dijkstra's algorithm for finding the shortest path between start and end.
    """
    dist = {vertex: float('infinity') for vertex in graph}
    prev = {vertex: None for vertex in graph}
    dist[start] = 0
    Q = [(0, start)]
    
    while Q:
        _, u = heapq.heappop(Q)
        
        # Early exit if we reach the end
        if u == end:
            path = []
            while u:
                path.append(u)
                u = prev[u]
            return path[::-1]
        
        for v, weight in graph[u].items():
            traffic_coeff = get_traffic_coefficient(v[0], v[1], hour)
            alt = dist[u] + weight * traffic_coeff
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
                heapq.heappush(Q, (dist[v], v))
    
    # Check Pythagorean routes
    direct_routes = [(start, (start[0], end[1])), ((start[0], end[1]), end), 
                     (start, (end[0], start[1])), ((end[0], start[1]), end)]
    for s, e in direct_routes:
        if dist[s] + heuristic(s, e) < dist[end]:
            return None
    
    return None

def heuristic(a, b):
    """
    Calculate the Manhattan distance between two points a and b.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def is_within_distance_of_line(point, start, end, distance=30):
    """
    Check if a point is within a certain distance of the line connecting start and end.
    """
    x, y = point
    x1, y1 = start
    x2, y2 = end
    
    # Calculate the distance of the point from the line using the point-line distance formula
    numerator = abs((y2 - y1) * x - (x2 - x1) * y + x2 * y1 - y2 * x1)
    denominator = math.sqrt((y2 - y1)**2 + (x2 - x1)**2)
    distance_from_line = numerator / denominator
    
    return distance_from_line <= distance

def create_bounded_city_graph(start, end, city_size=100):
    graph = {}
    min_i = max(0, min(start[0], end[0]) - SEARCH_RADIUS)
    max_i = min(city_size, max(start[0], end[0]) + SEARCH_RADIUS + 1)
    min_j = max(0, min(start[1], end[1]) - SEARCH_RADIUS)
    max_j = min(city_size, max(start[1], end[1]) + SEARCH_RADIUS + 1)
    
    for i in range(min_i, max_i):
        for j in range(min_j, max_j):
            if is_within_distance_of_line((i, j), start, end):
                neighbors = {}
                if j < max_j - 1 and is_within_distance_of_line((i, j + 1), start, end):
                    neighbors[(i, j + 1)] = 1
                if j > min_j and is_within_distance_of_line((i, j - 1), start, end):
                    neighbors[(i, j - 1)] = 1
                if i < max_i - 1 and is_within_distance_of_line((i + 1, j), start, end):
                    neighbors[(i + 1, j)] = 1
                if i > min_i and is_within_distance_of_line((i - 1, j), start, end):
                    neighbors[(i - 1, j)] = 1
                graph[(i, j)] = neighbors
    return graph



# Main Methods
def generate_route(start, end, hour):
    """
    Generate a route from start to end.
    """
    graph = create_bounded_city_graph(start, end)
    route = dijkstra(graph, start, end, hour)
    return route

def compute_travel_time(route, hour):
    """
    Compute the travel time for a given route based on the traffic data at a specific hour.
    
    Parameters:
    - route: List of tuples representing the path from start to end.
    - hour: The hour at which the travel is happening.
    
    Returns:
    - travel_time: The total time taken to travel the route at the given hour.
    """
    travel_time = 0
    for i in range(len(route) - 1):
        start = route[i]
        end = route[i + 1]
        
        # Assuming the distance between each grid point is 1 unit.
        # The time taken to travel between two points is the distance (1 unit) multiplied by the traffic coefficient.
        # A higher traffic coefficient means slower travel.
        travel_time += 35.9973447 * traffic_coefficient(start[0], start[1], hour)
        
    return travel_time/60.0


# Initialization
traffic_data = []
for time in range(24):
    traffic_data.append(generate_traffic_data(time))


# # Visualization No. 2
# x_coords, y_coords = zip(*route)
# colormap = plt.get_cmap('RdYlGn_r')
# plt.imshow(traffic_data[hour], cmap=colormap, origin="lower")
# plt.colorbar(label="Traffic Coefficient")
# plt.title("Traffic Heatmap with Route")
# plt.xlabel("X Coordinate")
# plt.ylabel("Y Coordinate")
# plt.plot(y_coords, x_coords, color='black', linewidth=2)  # Note the order of y and x here due to how imshow works
# plt.savefig('Presentation Data/Traffic_Heatmap_with_Route.png', dpi=300, bbox_inches='tight')
# plt.show()

# # Visualization No. 1
# colormap = plt.get_cmap('RdYlGn')
# plt.imshow(traffic_data, cmap=colormap, origin="lower")
# plt.colorbar(label="Traffic Coefficient")
# plt.title("Traffic Heatmap")
# plt.xlabel("X Coordinate")
# plt.ylabel("Y Coordinate")
# plt.savefig('Presentation Data/Traffic_Heatmap.png', dpi=300, bbox_inches='tight')
# #plt.show()
# for hour in range(24):
#     traffic_data = generate_traffic_data(hour)
#     plt.imshow(traffic_data, cmap='RdYlGn', origin="lower")
#     plt.colorbar(label="Traffic Coefficient")
#     plt.title(f"Traffic Heatmap at {hour}:00")
#     plt.xlabel("X Coordinate")
#     plt.ylabel("Y Coordinate")
#     plt.savefig(f'Presentation Data/Traffic_Heatmap_{hour}h.png', dpi=300, bbox_inches='tight')
#     plt.close()