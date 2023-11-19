import pandas as pd

# Specify the path to your CSV file
csv_file = "datasets/final_events.csv"

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file)

# Add quotes around all values in the first column
df.iloc[:, 0] = df.iloc[:, 0].apply(lambda x: f'"{x}"')

# Save the modified DataFrame back to a CSV file
output_csv_file = "final_events_2.csv"
df.to_csv(output_csv_file, index=False)

print(f"Quotes added to the first column and saved to {output_csv_file}")
