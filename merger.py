import pandas as pd

# Load your event dataset into a DataFrame (replace 'event_data.csv' with your file path)
event_df = pd.read_csv("datasets/final_data/complete_event_list.csv")

# Load your water quality dataset into another DataFrame (replace 'water_quality_data.csv' with your file path)
water_quality_df = pd.read_csv("datasets/final_data/cwi.csv")

# Assuming both datasets have a 'date' column, convert it to a datetime format
event_df["Date"] = pd.to_datetime(event_df["Date"])
water_quality_df["Date"] = pd.to_datetime(water_quality_df["Date"])

# Merge the two DataFrames based on the 'date' column
merged_df = pd.merge(event_df, water_quality_df, on="Date", how="inner")

merged_df.to_csv("datasets/final_data/merged_data.csv", index=False)
