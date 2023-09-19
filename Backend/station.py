#TODO: Train Wait Time
#TODO: Train Cost

class Station:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.id = "X" + str(x) + "Y" + str(y)
        self.speed = 111.76

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

    def train_travel_time(self, other_station):
        x, y = self.distance_to(other_station)
        distance_x = abs(x)
        distance_y = abs(y)
        time_x = (distance_x * 100 / self.speed) + ((distance_x / 10 - 1)) if distance_x != 0 else 0
        time_y = (distance_y * 100 / self.speed) + ((distance_y / 10 - 1)) if distance_y != 0 else 0
        total_time = (time_x + time_y) / 60
        return total_time

    def train_route(self, other_station):
        route = []
        x, y = self.distance_to(other_station)
        distance_x = abs(x)
        distance_y = abs(y)

        # Route along x-axis
        for i in range(0, distance_x + 1):
            if x < 0:
                route.append((self.x + i, self.y))
            elif x > 0:
                route.append((self.x - i, self.y))

        # Route along y-axis
        for i in range(0, distance_y + 1):
            if y < 0:
                route.append((self.x, self.y + i))
            elif y > 0:
                route.append((self.x, self.y - i))

        return route


stations = []
for i in range(10, 100, 10):  
    for j in range(10, 100, 10):  
        stations.append(Station(i, j))
