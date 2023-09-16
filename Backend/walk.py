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

def compute_walk_route(start, end):
    """
    Compute the walk route from start to end based on the Manhattan distance.
    
    Parameters:
    - start: Tuple representing the starting point.
    - end: Tuple representing the ending point.
    
    Returns:
    - walk_route: A list of tuples representing the route from start to end.
    """
    walk_route = []
    
    # Calculate the Manhattan distance
    distance = abs(start[0] - end[0]) + abs(start[1] - end[1])
    distance_meters = distance * 100
    walk_time = distance_meters / 1.39

    
    # Generate the walk route based on segment length
    for i in range(0, distance + 1):
        if start[0] < end[0]:
            walk_route.append((start[0] + i, start[1]))
        elif start[0] > end[0]:
            walk_route.append((start[0] - i, start[1]))
        elif start[1] < end[1]:
            walk_route.append((start[0], start[1] + i))
        elif start[1] > end[1]:
            walk_route.append((start[0], start[1] - i))
    
    return walk_route

def walk_cost(start, end):
    """
    Compute the walk cost from start to end based on the Manhattan distance.
    
    Parameters:
    - start: Tuple representing the starting point.
    - end: Tuple representing the ending point.
    
    Returns:
    - walk_cost: The cost of walking from start to end.
    """
    # Calculate the Manhattan distance
    distance = abs(start[0] - end[0]) + abs(start[1] - end[1])
    
    # Assuming each grid point is 100 meters apart
    distance_meters = distance * 100
    walk_time = distance_meters / 1.39
    walk_cost = walk_time * 0
    
    return walk_cost



print(compute_walk_route((0, 0), (99, 99)))
