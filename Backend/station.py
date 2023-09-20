class Station:
    """
    Represents a train station with coordinates (x, y) and methods to calculate travel time and route to another station.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.id = f"X{x}Y{y}"
        self.speed = 111.76  # Speed in meters per minute

    def get_id(self):
        """
        Returns the unique ID of the station.
        """
        return self.id

    def distance_to(self, other_station):
        """
        Compute the distance to another station.

        Parameters:
        - other_station: The other Station object.

        Returns:
        - (dx, dy): A tuple where dx is the distance along the x-axis and dy is the distance along the y-axis.
        """
        return other_station.x - self.x, other_station.y - self.y

    def train_travel_time(self, other_station):
        """
        Calculate the time required to travel to another station.

        Parameters:
        - other_station: The other Station object.

        Returns:
        - total_time: The total time required to travel to the other station in minutes.
        """
        dx, dy = self.distance_to(other_station)
        time_x = (abs(dx) * 100 / self.speed) + (abs(dx) // 10 - 1) if dx != 0 else 0
        time_y = (abs(dy) * 100 / self.speed) + (abs(dy) // 10 - 1) if dy != 0 else 0
        return (time_x + time_y) / 60

    def train_route(self, other_station):
        """
        Generate the route to another station.

        Parameters:
        - other_station: The other Station object.

        Returns:
        - route: A list of tuples representing the coordinates along the route.
        """
        route = []
        dx, dy = self.distance_to(other_station)

        # Horizontal segment
        for x in range(self.x, other_station.x + 1) if dx >= 0 else range(self.x, other_station.x - 1, -1):
            route.append((x, self.y))

        # Vertical segment
        for y in range(self.y, other_station.y + 1) if dy >= 0 else range(self.y, other_station.y - 1, -1):
            route.append((other_station.x, y))

        return route

# Initialize stations
stations = [Station(i, j) for i in range(10, 100, 10) for j in range(10, 100, 10)]