from station import stations

class Train:

    def __init__(self, direction, speed, vertical=None, horizontal=None):
        self.direction = direction
        self.speed = speed
        self.vertical = vertical
        self.horizontal = horizontal

    def __repr__(self):
        return f"Train(direction={self.direction}, speed={self.speed}, vertical={self.vertical}, horizontal={self.horizontal})"

    def time_to_station(self, station, time_passed, direction):
        distance = 0
        if self.vertical:
            distance = abs(self.vertical - station[0])
        elif self.horizontal:
            distance = abs(self.horizontal - station[1])

        # Convert speed from km/h to km/min
        speed_per_minute = self.speed / 60

        # Calculate the time taken to travel the distance
        travel_time = distance / speed_per_minute

        # Add the stop time for each station
        stops = distance // 10
        total_time = travel_time + (stops * 1)  # 1 minute stop at each station

        # Check if the train has to turn around
        if direction in ["N", "W"]:
            if self.direction == "B":
                total_time += (100 / speed_per_minute) + (9 * 1)  # Time to reach the end and turn around
        elif direction in ["S", "E"]:
            if self.direction == "F":
                total_time += (100 / speed_per_minute) + (9 * 1)

        # Subtract the time passed to get the remaining time
        remaining_time = total_time - time_passed

        return remaining_time




# Variables
trains = []
SPEED = 10

# Create trains for vertical lines
for i in range(10, 100, 10):
    trains.append(Train("F", SPEED, vertical=i))
    trains.append(Train("B", SPEED, vertical=i))

# Create trains for horizontal lines
for j in range(10, 100, 10):
    trains.append(Train("F", SPEED, horizontal=j))
    trains.append(Train("B", SPEED, horizontal=j))