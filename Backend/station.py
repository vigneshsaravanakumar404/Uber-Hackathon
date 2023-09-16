import math

class Station:
    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.station_id = f"S-{row}{column}-S"
    
    def distance_between_stations(self, other_station):
        x_displacement = other_station.column - self.column
        y_displacement = other_station.row - self.row
        return x_displacement, y_displacement

    

    