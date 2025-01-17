class Cell:
    def __init__(self, cell_type: str, position):
        self.type = cell_type  # 'L', 'B', 'T', or 'F'
        self.position = position  # (row, column)
        self.is_discovered = False  # Tracks if the cell is discovered
        self.is_consumed =  False  # Only applicable for treasures
        self.is_destroyed = False  # Only applicable for bombs
        self.is_flag_found = False # Only applicable for the flag

    def discover(self):
        self.is_discovered = True

    def consume_treasure(self, consume_all):
        if self.type in 'T' and not self.is_consumed:
            self.is_consumed = True
            if consume_all:
                self.change_cell_type('L')
            return True
        return False

    def destroy_bomb(self):
        if self.type in 'B' and not self.is_destroyed:
            self.is_destroyed = True
            self.change_cell_type('L')
            return True
        return False

    def found_the_flag(self):
        if self.type in 'F' and not self.is_flag_found:
            self.is_flag_found = True
            return True
        return False

    def change_cell_type(self, cell_type):
        self.type = cell_type

    def display_color(self):
        if self.type == 'L': return "white"
        if self.type == 'B': return "light coral"
        if self.type == 'T': return "gold"
        if self.type == 'F': return "green"

    def __repr__(self):
        status = "Discovered" if self.is_discovered else "Undiscovered"
        consumed_status = f", Consumed" if self.is_consumed else ""
        return f"Cell({self.type}, {status}{consumed_status}, Position={self.position})"
