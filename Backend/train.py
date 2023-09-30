class Train:
    """
    Represents a train object with attributes for direction, speed, and position.
    
    Attributes:
    - direction: A string representing the direction of the train ("F" for forward, "B" for backward).
    - speed: An integer representing the speed of the train in km/h.
    - vertical: An integer representing the vertical position of the train, or None if not applicable.
    - horizontal: An integer representing the horizontal position of the train, or None if not applicable.
    """
    
    def __init__(self, direction, speed, vertical=None, horizontal=None):
        self.direction = direction
        self.speed = speed
        self.vertical = vertical
        self.horizontal = horizontal

    class Train:
        class Train:
            """
            A class representing a train object.

            Attributes:
            - direction (str): The direction the train is moving in.
            - speed (float): The speed of the train in km/h.
            - vertical (float): The vertical position of the train in meters.
            - horizontal (float): The horizontal position of the train in meters.
            """

            def __init__(self, direction, speed, vertical, horizontal):
                self.direction = direction
                self.speed = speed
                self.vertical = vertical
                self.horizontal = horizontal

        def __repr__(self):
            """
            Returns a string representation of the Train object.

            Returns:
                str: A string representation of the Train object.
            """
            return f"Train(direction={self.direction}, speed={self.speed}, vertical={self.vertical}, horizontal={self.horizontal})"

    def time_to_station(self, station, time_passed, direction):
        """
        Calculate the time for the train to reach a given station.
        
        Parameters:
        - station: A tuple representing the station coordinates (x, y).
        - time_passed: Time passed since the train started its journey.
        - direction: Direction of the train ("N", "S", "E", "W").
        
        Returns:
        - remaining_time: Time remaining for the train to reach the station.
        """
        
        distance = abs(self.vertical - station[0]) if self.vertical else abs(self.horizontal - station[1])
        
        # Convert speed from km/h to km/min and calculate travel time
        speed_per_minute = self.speed / 60
        travel_time = distance / speed_per_minute

        # Calculate stops and total time including stops
        stops = distance // 10
        total_time = travel_time + stops  # 1 minute stop at each station

        # Check for turn-around time
        if direction in ["N", "W"] and self.direction == "B":
            total_time += (100 / speed_per_minute) + 9
        elif direction in ["S", "E"] and self.direction == "F":
            total_time += (100 / speed_per_minute) + 9

        # Calculate remaining time
        remaining_time = total_time - time_passed

        return remaining_time


# Initialize trains with a constant speed
SPEED = 10
trains = [Train(dir, SPEED, vertical=i) for i in range(10, 100, 10) for dir in ["F", "B"]] + \
         [Train(dir, SPEED, horizontal=j) for j in range(10, 100, 10) for dir in ["F", "B"]]
