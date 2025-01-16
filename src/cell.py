class Cell:
    def __init__(self, cell_type: str, position):
        self.type = cell_type  # 'L', 'B', 'T', or 'F'
        self.position = position  # (row, column)
        self.is_discovered = False  # Tracks if the cell is discovered
        self.is_consumed = False if self.type in 'T' else None  # Only applicable for treasures
        self.is_destroyed = False if self.type in 'B' else None # Only applicable for bombs

    def discover(self):
        self.is_discovered = True

    def consume_treasure(self):
        if self.type in 'T' and not self.is_consumed:
            self.is_consumed = True
            return True
        return False

    def destroy_bomb(self):
        if self.type in 'B' and not self.is_destroyed:
            self.is_destroyed = True
            return True
        return False

    def __repr__(self):
        """
        String representation of the Cell object for debugging.

        Returns:
            str: Representation of the cell's type and state.
        """
        status = "Discovered" if self.is_discovered else "Undiscovered"
        consumed_status = f", Consumed" if self.is_consumed else ""
        return f"Cell({self.type}, {status}{consumed_status}, Position={self.position})"
