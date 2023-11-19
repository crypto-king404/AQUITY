import pandas as pd

# Load your water quality dataset into another DataFrame (replace 'water_quality_data.csv' with your file path)
water_quality_df = pd.read_csv("datasets/final_data/normalized_data.csv")

# Assuming you have a DataFrame named water_quality_df

# Iterate through the DataFrame rows and print row number and Date values
for index, row in water_quality_df.iterrows():
    if "/" not in row["Date"]:
        print(f"Row {index + 1}: {row['Date']}")
