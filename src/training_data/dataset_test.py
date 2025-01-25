import itertools
import pandas as pd
import numpy as np

# Rules for determining the best move
def determine_best_move(left, right, up, down, has_power):
    """
    Define a priority for movement based on the environment and empowerment.
    Agents can move into bombs if has_power is 1, but it is not prioritized.
    """
    # Define the priority of moves
    if has_power:
        cell_priority = ["T", "L", "?", "B"]  # Can move into bombs if empowered
    else:
        cell_priority = ["T", "L", "?"]  # Avoid bombs

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

    return None  # Shouldn't happen with valid input


# Generate dataset
def generate_dataset(output_file):
    """
    Generate a dataset with an additional 'has_power' column, allowing agents
    to move into bombs when empowered (has_power=1), but without prioritizing it.
    """
    # Define possible values for each position
    cell_values = ["L", "B", "T", "-", "?"]
    all_combinations = itertools.product(cell_values, repeat=4)

    data = []

    for combination in all_combinations:
        left, right, up, down = combination

        # Generate both cases: has_power = 0 and has_power = 1
        for has_power in [0, 1]:

            # Skip invalid combinations where all moves are "-" or "B" (when not empowered)
            if not has_power and all(cell in ["-", "B"] for cell in combination):
                continue

            # Determine the best move
            move = determine_best_move(left, right, up, down, has_power)

            # Add the entry to the dataset
            data.append({
                "left": left,
                "right": right,
                "up": up,
                "down": down,
                "has_power": has_power,
                "Move": move
            })

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Save to CSV
    df.to_csv(output_file, index=False)
    print(f"Dataset written to {output_file} with {len(df)} rows.")

# Main function
if __name__ == "__main__":
    output_file = "dataset_test.csv"
    generate_dataset(output_file)
