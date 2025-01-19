import pandas as pd

# Example data
data = [
    {"left": "B", "right": "B", "up": "B", "down": "L", "Move": "down"},
    {"left": "L", "right": "T", "up": "B", "down": "B", "Move": "right"},
    {"left": "T", "right": "B", "up": "L", "down": "B", "Move": "left"},
    {"left": "L", "right": "L", "up": "B", "down": "B", "Move": "left"},
    {"left": "L", "right": "B", "up": "T", "down": "L", "Move": "up"},
    {"left": "B", "right": "L", "up": "B", "down": "T", "Move": "down"},
    {"left": "B", "right": "B", "up": "T", "down": "L", "Move": "up"},
    {"left": "T", "right": "L", "up": "B", "down": "B", "Move": "left"},
    {"left": "L", "right": "L", "up": "T", "down": "T", "Move": "down"},
    {"left": "T", "right": "T", "up": "L", "down": "L", "Move": "right"},
]

# Convert to DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv("dataset.csv", index=False)

print("CSV file saved as 'dataset.csv'")
