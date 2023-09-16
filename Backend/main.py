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



# Static Data
BASE_TRAFFIC_VARIATION = 0.25
SEARCH_RADIUS = 10


# Methods
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

# Initialization
traffic_data = []
for hour in range(24):
    traffic_data.append(generate_traffic_data(hour))

import random
import time

##########################################################

def display_progress_bar(iteration, total, bar_length=50):
    """
    Display a progress bar in the console.
    """
    progress = (iteration / total)
    arrow = '=' * int(round(progress * bar_length) - 1) + '>'
    spaces = ' ' * (bar_length - len(arrow))
    
    print(f"\rProgress: [{arrow + spaces}] {int(progress * 100)}%", end='')



# Number of tests
NUM_TESTS = 10000

# List to store the time taken for each test
times_taken = []
output = ""

# Fancy console output
print("Starting tests...\n")
output += "Starting tests...\n"
print("========================================")
output += "========================================\n"

for i in range(NUM_TESTS):
    # Randomly select hour (including decimals)
    hour = random.uniform(0, 23)
    
    # Randomly select starting and ending points on the grid
    start_point = (random.randint(0, 99), random.randint(0, 99))
    end_point = (random.randint(0, 99), random.randint(0, 99))
    
    # Start the timer
    start_time = time.time()
    
    # Run the provided code
    graph = create_bounded_city_graph(start_point, end_point)
    route = dijkstra(graph, start_point, end_point, hour)
    
    # End the timer
    end_time = time.time()
    
    # Calculate time taken for this test
    time_taken = end_time - start_time
    times_taken.append(time_taken)
    
    # Display the average time taken every 100 tests
    display_progress_bar(i + 1, NUM_TESTS)
    if (i + 1) % 100 == 0:
        avg_time = sum(times_taken) / len(times_taken)
        print(f" Test {i + 1}/{NUM_TESTS} | Average Time: {avg_time:.4f} seconds")
        output += f"Test {i + 1}/{NUM_TESTS} | Average Time: {avg_time:.4f} seconds\n"
    
print("========================================")
output += "========================================\n"
print("\nTests completed!")
output += "\nTests completed!\n"

# Display the final average
final_avg_time = sum(times_taken) / len(times_taken)
print(f"Final Average Time: {final_avg_time:.4f} seconds")
output += f"Final Average Time: {final_avg_time:.4f} seconds\n"

# Write to Presentation Data folder
with open("Presentation Data/Performance_Testing.txt", "w") as f:
    f.write(output)

###################################################################

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


#TODO: Make the function actually work for peak hours and not work around it