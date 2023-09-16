class Train:

    def __init__(self, direction, speed, vertical=None, horizontal=None):
        self.direction = direction
        self.speed = speed
        self.vertical = vertical
        self.horizontal = horizontal

    def __repr__(self):
        return f"Train(direction={self.direction}, speed={self.speed}, vertical={self.vertical}, horizontal={self.horizontal})"



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

# Print the trains to verify
for train in trains:
    print(train)