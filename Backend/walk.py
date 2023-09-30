WALK_SPEED = 1.34112  # meters per second


def compute_walk_time(start, end):
    """
    Compute the walk time from start to end based on the Manhattan distance and average walking speed.
    
    Parameters:
    - start: Tuple representing the starting point (x, y).
    - end: Tuple representing the ending point (x, y).
    
    Returns:
    - walk_time: The time (in seconds) taken to walk from start to end.
    """
    distance = abs(start[0] - end[0]) + abs(start[1] - end[1])
    distance_meters = distance * 100
    walk_time = distance_meters / WALK_SPEED
    return walk_time

def compute_walk_route(start, end):
    """
    Computes a walk route between two points on a 2D grid.

    Args:
        start (tuple): The starting point as a tuple of (x, y) coordinates.
        end (tuple): The ending point as a tuple of (x, y) coordinates.

    Returns:
        list: A list of (x, y) coordinates representing the walk route.
    """
    walk_route = []
    x1, y1 = start
    x2, y2 = end
    
    # Horizontal segment
    for x in range(x1, x2 + 1) if x1 <= x2 else range(x1, x2 - 1, -1):
        walk_route.append((x, y1))
    
    # Vertical segment
    for y in range(y1, y2 + 1) if y1 <= y2 else range(y1, y2 - 1, -1):
        walk_route.append((x2, y))
    
    return walk_route

def walk_cost(start, end):
    """
    Compute the walk cost from start to end based on the Manhattan distance.
    
    Parameters:
    - start: Tuple representing the starting point (x, y).
    - end: Tuple representing the ending point (x, y).
    
    Returns:
    - walk_cost: The cost of walking from start to end (always 0 in this case).
    """
    return 0  # Walking is free
