from server import app
from flask import Flask, jsonify, request
from station import Station
import math
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm


# Static Data
BASE_TRAFFIC_VARIATION = 0.15

# Methods
def gaussian(x, mu, sigma):
    """Gaussian function to model the base traffic coefficient."""
    return math.exp(-((x - mu)**2) / (2 * sigma**2))

def get_traffic_variation_bounds(hour):
    """
    Adjust the traffic variation bounds based on the time of day using a sinusoidal function.
    Peaks at 7-9 AM and 5-7 PM.
    """
    # Convert hour to radians
    radian_conversion = 2 * math.pi / 24
    time_in_radians = hour * radian_conversion
    
    # Sinusoidal function to model overall traffic level
    overall_traffic_level = 0.90 * math.sin(2 * time_in_radians - 7 * radian_conversion)
    
    # Sinusoidal function to model traffic variation
    sinusoidal_variation = 0.01 * math.sin(3 * time_in_radians - 7 * radian_conversion)
    
    # Adjust the bounds based on the overall traffic level and variation
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
    
    # Base coefficient using the Gaussian function
    base_coeff = gaussian(distance_from_center, 0, max_distance / 3)
    
    # Normalize the coefficient to be between 0.05 and 1
    normalized_coeff = 0.05 + 0.95 * base_coeff
    
    # Adjust traffic variation bounds based on time
    lower_bound, upper_bound = get_traffic_variation_bounds(hour)
    variation = 1 + random.uniform(-lower_bound, upper_bound)
    final_coeff = normalized_coeff * variation
    
    # Invert the coefficient
    inverted_coeff = 1 - final_coeff
    
    return inverted_coeff

def generate_traffic_data(hour, city_size=100):
    """
    Generate a 2D array of traffic coefficients for the city.
    """
    traffic_data = np.zeros((city_size, city_size))
    for i in range(city_size):
        for j in range(city_size):
            traffic_data[i, j] = traffic_coefficient(i, j, hour)
    return traffic_data


# Initialization
stations = []
traffic_data = np.zeros((100, 100))

for i in range(10, 100, 10):  # Rows 10, 20, ..., 90
    for j in range(10, 100, 10):  # Columns 10, 20, ..., 90
        stations.append(Station(i, j))

traffic_data = generate_traffic_data(0) # Change this to the hour





# # Visualization
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






