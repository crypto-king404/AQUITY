import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv("datasets/elevations.csv")


# Define a function to process the date column
def process_date(date_str):
    if " - " in date_str:
        # Split the string on ' - ' and keep only the part before it
        return date_str.split(" - ")[0]
    else:
        # If there is no ' - ' in the string, return it as is
        return date_str


# Apply the function to the date_column
df["Date"] = df["Date"].apply(process_date)

# Save the modified DataFrame to a new CSV file
df.to_csv("output.csv", index=False)
