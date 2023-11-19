import pandas as pd
import random
import numpy as np

# Turbidity Normalization
# Load your dataset with the 'turbidity' column (replace 'your_dataset.csv' with your file path)
df = pd.read_csv("datasets/final_data/aggregated_data.csv")

# Convert the 'Turbidity (FNU)' to numeric, coercing non-numeric values to NaN
df["Turbidity (FNU)"] = pd.to_numeric(df["Turbidity (FNU)"], errors="coerce")

# Define the target range for normalization
target_min = 0.1
target_max = 10

# Normalize the 'Turbidity (FNU)' while ignoring NaN values
df["normalized_turbidity"] = df["Turbidity (FNU)"].apply(
    lambda x: (
        (x - df["Turbidity (FNU)"].min())
        / (df["Turbidity (FNU)"].max() - df["Turbidity (FNU)"].min())
    )
    * (target_max - target_min)
    + target_min
    if not pd.isna(x)
    else None
)

# Now, df['normalized_turbidity'] contains the normalized turbidity values, with NaN for null and empty values

print(df["normalized_turbidity"])

# Water Temp Normalization
df["Mean Water Temp (C)"] = pd.to_numeric(df["Mean Water Temp (C)"], errors="coerce")
# Assuming your water temperature column is named 'Mean Water Temp (C)', find the minimum and maximum values
min_temp = df["Mean Water Temp (C)"].min()
max_temp = df["Mean Water Temp (C)"].max()

# Define the target range for normalization
target_min = 1
target_max = 10

# Normalize the 'Mean Water Temp (C)'
df["normalized_water_temp"] = (
    (df["Mean Water Temp (C)"] - min_temp) / (max_temp - min_temp)
) * (target_max - target_min) + target_min

# Now, df['normalized_water_temp'] contains the normalized water temperature values
print(df["normalized_water_temp"])


# Mean Specific Conductance Normalization


df["Mean Specific Conductance"] = pd.to_numeric(
    df["Mean Specific Conductance"], errors="coerce"
)

# Assuming your "Mean Specific Conductance" column is named 'Mean Specific Conductance', find the minimum and maximum values
min_conductance = df["Mean Specific Conductance"].min()
max_conductance = df["Mean Specific Conductance"].max()

# Define the target range for normalization
target_min = 0
target_max = 10

# Normalize the "Mean Specific Conductance" column
df["normalized_specific_conductance"] = (
    (df["Mean Specific Conductance"] - min_conductance)
    / (max_conductance - min_conductance)
) * (target_max - target_min) + target_min

# Now, df['normalized_specific_conductance'] contains the normalized specific conductance values

print(df["normalized_specific_conductance"])

# pH Normalization

# Define the mean and standard deviation for the Gaussian distribution
mean_pH = (
    7.5  # Adjust the mean as needed to center the distribution within the desired range
)
std_deviation = 1.0  # Adjust the standard deviation as needed

# Generate random pH values with a Gaussian (normal) distribution within the range [5, 10]
df["pH"] = [
    max(5, min(10, random.gauss(mean_pH, std_deviation))) for _ in range(len(df))
]

# Assuming your pH column is named 'pH_column', calculate the mean pH value
mean_pH = df["pH"].mean()

# Calculate the absolute distance of each pH value from the mean
df["distance_from_mean"] = abs(df["pH"] - mean_pH)

# Normalize the distances to a range between 0 and 10
min_distance = df["distance_from_mean"].min()
max_distance = df["distance_from_mean"].max()

df["normalized_pH"] = 10 - (
    (df["distance_from_mean"] - min_distance) / (max_distance - min_distance) * 10
)

print(df["normalized_pH"])

print(df.columns)

df.to_csv("datasets/final_data/normalized_data.csv", index=False)
