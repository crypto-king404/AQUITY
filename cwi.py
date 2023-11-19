import pandas as pd
import numpy as np

df = pd.read_csv("datasets/final_data/normalized_data.csv")


# Weights for the parameters
weights = {
    "normalized_turbidity": 0.3,
    "normalized_specific_conductance": 0.2,
    "normalized_pH": 0.2,
    "normalized_water_temp": 0.3,
}


def compute_cwi(row):
    available_params = {
        param: weight for param, weight in weights.items() if not np.isnan(row[param])
    }
    if not available_params:  # if all values are NaN, return NaN as the CWI
        return np.nan

    adjusted_weights = {
        param: weight / sum(available_params.values())
        for param, weight in available_params.items()
    }
    cwi = np.sum([row[param] * adjusted_weights[param] for param in adjusted_weights])
    return cwi


# Compute the CWI considering missing values and adjusted weights
df["cwi"] = df.apply(compute_cwi, axis=1)

# Since CWI is already on a scale of 1-10, we just need to convert it to a scale of 1-100
df["cwi_100"] = np.round(100 * (df["cwi"] - 1) / 9).astype(int)


print(df["cwi_100"].max())
print(df["cwi_100"].min())

df.to_csv("datasets/final_data/cwi.csv", index=False)
