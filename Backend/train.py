class Train:
    def __init__(self, starting_direction, is_east_west):

        if is_east_west:
            is_east_west = "EW"
        else:
            is_east_west = "NS"

        # Attributes
        self.train_id = f"T-{starting_direction}{is_east_west}-T"
        self.starting_direction = starting_direction
        self.speed = 250/9
        self.stop_time = 60
        self.is_east_west = is_east_west
        self.current_direction = starting_direction

    
    
