import itertools
import pandas as pd

# Rules for determining the best move
def determine_best_move(left, right, up, down):
    # Define the priority of moves
    cell_priority = ["T", "L", "?"]  # Prioritize treasure, then free cells, then unknown
    move_options = {
        "left": left,
        "right": right,
        "up": up,
        "down": down
    }

    # Filter moves based on priority
    for cell_type in cell_priority:
        for direction, cell in move_options.items():
            if cell == cell_type:
                return direction

    # If no valid move, return None (shouldn't happen with valid input)
    return None

# Generate dataset
def generate_dataset(output_file):
    # Define possible values for each position
    cell_values = ["L", "B", "T", "-", "?"]
    all_combinations = itertools.product(cell_values, repeat=4)

    data = []

    for combination in all_combinations:
        left, right, up, down = combination

        # Skip invalid combinations where all moves are "-" or "B"
        if all(cell in ["-", "B"] for cell in combination):
            continue

        # Determine the best move
        move = determine_best_move(left, right, up, down)

        # Add the entry to the dataset
        data.append({"left": left, "right": right, "up": up, "down": down, "Move": move})

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Save to CSV
    df.to_csv(output_file, index=False)
    print(f"Dataset written to {output_file} with {len(df)} rows.")

# Main function
if __name__ == "__main__":
    output_file = "dataset.csv"
    generate_dataset(output_file)
