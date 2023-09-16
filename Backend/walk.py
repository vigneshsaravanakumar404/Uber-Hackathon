WALK_SPEED = 1.34112 # meters per second

def compute_walk_time(start, end):
    """
    Compute the walk time from start to end based on the Manhattan distance and average walking speed.
    
    Parameters:
    - start: Tuple representing the starting point.
    - end: Tuple representing the ending point.
    
    Returns:
    - walk_time: The time (in seconds) taken to walk from start to end.
    """
    # Calculate the Manhattan distance
    distance = abs(start[0] - end[0]) + abs(start[1] - end[1])
    
    # Assuming each grid point is 100 meters apart
    distance_meters = distance * 100
    
    # Average walking speed: 1.39 m/s
    walk_time = distance_meters / 1.39
    
    return walk_time


