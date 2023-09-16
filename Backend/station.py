#TODO: Train Wait Time
#TODO: Train Cost

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

    def train_travel_time(self, other_station):
        """Compute the travel time to another station.

        Parameters:
        - other_station: The other Station object.

        Returns:
        - time: The travel time in minutes to the other station.
        """
        
        x,y = self.distance_to(other_station) 
        if (x==0) or (y==0):
            distance = abs(x) + abs(y)
            time = ((distance * 100 / self.speed) + ((distance/10 - 1)))/60
            return time
        else:
            return -1

    def train_route(self, other_station):
        """Compute the route to another station.

        Parameters:
        - other_station: The other Station object.

        Returns:
        - route: A list of tuples representing the route from this station to the other station.
        """
        route = []
        x,y = self.distance_to(other_station)
        if (x==0) or (y==0):
            distance = abs(x) + abs(y)
            for i in range(0, distance + 1):
                if x < 0:
                    route.append((self.x + i, self.y))
                elif x > 0:
                    route.append((self.x - i, self.y))
                elif y < 0:
                    route.append((self.x, self.y + i))
                elif y > 0:
                    route.append((self.x, self.y - i))
            return route
        else:
            return -1


stations = []
for i in range(10, 100, 10):  
    for j in range(10, 100, 10):  
        stations.append(Station(i, j))


start_station = stations[0]
end_station = stations[5]

print(f"Travel time from station {start_station.x},{start_station.y} to station {end_station.x},{end_station.y}: {start_station.train_travel_time(end_station)} minutes")
