class Station:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.id = "X" + str(x) + "Y" + str(y)
        self.speed = 27.7778

    def get_id(self):
        return self.id

    def distance_to(self, other_station):
        """Compute the distance to another station.

        Parameters:
        - other_station: The other Station object.

        Returns:
        - (dx, dy): A tuple where dx is the distance along the x-axis and dy is the distance along the y-axis.
        """
        dx = other_station.x - self.x
        dy = other_station.y - self.y
        return (dx, dy)

    def time_to(self, other_station):
        """Compute the time to another station.

        Parameters:
        - other_station: The other Station object.

        Returns:
        - time: The time in minutes to the other station.
        """
        (dx, dy) = self.distance_to(other_station)
        return (dx + dy) * self.speed


stations = []
for i in range(10, 100, 10):  
    for j in range(10, 100, 10):  
        stations.append(Station(i, j))