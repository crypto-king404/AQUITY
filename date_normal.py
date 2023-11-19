import pandas as pd

# Load your dataset with the date column (replace 'your_dataset.csv' with your file path)
df = pd.read_csv("datasets/final_data/output.csv")

# Assuming your date column is named 'Date', convert it to datetime format
df["Date"] = pd.to_datetime(df["Date"])

# Find the minimum and maximum dates in the column
min_date = df["Date"].min()
max_date = df["Date"].max()

# Define the target date range
target_start_date = pd.to_datetime("04/01/2023")
target_end_date = pd.to_datetime("10/21/2023")

# Normalize the dates using linear scaling
df["Date"] = (df["Date"] - min_date) / (max_date - min_date) * (
    target_end_date - target_start_date
) + target_start_date

# Convert the Date column to the desired string format
df["Date"] = df["Date"].dt.strftime("%m/%d/%Y")

# Now, df['Date'] contains the normalized dates

print(df["Date"])

# Save the modified DataFrame to a new CSV file
df.to_csv("output.csv", index=False)
