import pandas as pd
import xgboost as xgb
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, GridSearchCV
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error
import numpy as np
import folium
from folium.plugins import HeatMap
from geopy.distance import geodesic
from sklearn.preprocessing import MinMaxScaler
from scipy.interpolate import griddata  # Import griddata function from SciPy


# 1. Load the dataset
file_path = "merged_data.csv"
df = pd.read_csv(file_path)

# 2. Preprocessing

# Filling missing values with the mean of the numeric columns
numeric_columns = df.select_dtypes(include=[np.number]).columns
df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].mean())

# Vectorizing the title using TF-IDF vectorizer
vectorizer = TfidfVectorizer()
title_features = vectorizer.fit_transform(df["Title"]).toarray()
title_df = pd.DataFrame(
    title_features, columns=[f"title_{i}" for i in range(title_features.shape[1])]
)

# Dropping the original Title column and concatenating the vectorized title features
df.drop(columns=["Title"], inplace=True)
df = pd.concat([df, title_df], axis=1)

# Converting the date to datetime format and extracting features
df["Date"] = pd.to_datetime(df["Date"])
df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month
df["Day"] = df["Date"].dt.day
df.drop(columns=["Date"], inplace=True)  # drop the original Date column

# 3. Training the XGBoost model with hyperparameter tuning

# Selecting the feature and target columns
features = df.drop(
    columns=[
        "Mean Water Temp (C)",
        "Mean Specific Conductance",
        "Turbidity (FNU)",
        "pH",
        "normalized_turbidity",
        "normalized_water_temp",
        "normalized_specific_conductance",
        "normalized_pH",
        "cwi",
        "cwi_100",
        "site_no",
    ]
)
targets = df[
    [
        "normalized_turbidity",
        "normalized_water_temp",
        "normalized_specific_conductance",
        "normalized_pH",
    ]
]

# Splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    features, targets, test_size=0.2, random_state=42
)

# Define the parameter grid for hyperparameter tuning
best_params = {
    "objective": "reg:squarederror",
    "n_estimators": 300,
    "learning_rate": 0.2,
    "max_depth": 5,
}

# Train the model using the best parameters
model = xgb.XGBRegressor(**best_params)
model.fit(X_train, y_train)
# # Create the XGBoost model
# model = XGBRegressor(objective="reg:squarederror")

# # Perform Grid Search with cross-validation
# grid_search = GridSearchCV(
#     estimator=model,
#     param_grid=param_grid,
#     scoring="neg_mean_squared_error",
#     cv=5,  # 5-fold cross-validation
#     n_jobs=-1,  # Use all available CPU cores
# )

# # Fit the grid search to the training data
# grid_search.fit(X_train, y_train)

# # Get the best model from the grid search
# best_model = grid_search.best_estimator_

# Predict using the best model
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(
    y_test, y_pred, multioutput="raw_values"
)  # you can use other metrics too
print(f"Mean Squared Errors for each target: {mse}")


# Example latitude and longitude grid covering an area around Cambridge
lat_min, lat_max = 42.36, 42.38
lon_min, lon_max = -71.14, -71.11
lat_values = np.linspace(lat_min, lat_max, 100)
lon_values = np.linspace(lon_min, lon_max, 100)
lat_lon_grid = np.array(np.meshgrid(lat_values, lon_values)).T.reshape(-1, 2)

# Event information
event_location = (42.37066, -71.12505)
event_title = "Water Conservation Efforts by Students"

# Vectorizing event title with TF-IDF
vectorizer = TfidfVectorizer()
vectorizer.fit([event_title])
event_vectorized = vectorizer.transform([event_title]).toarray()

# Compute distances from each point in the grid to the event location
distances = np.array([geodesic(event_location, point).km for point in lat_lon_grid])

# Normalize the distances using MinMaxScaler
scaler = MinMaxScaler()
normalized_distances = scaler.fit_transform(distances.reshape(-1, 1))

# Create a template feature vector
num_features = 343  # Adjust as per your model
template_feature_vector = np.zeros((1, num_features))

# Update the template with latitude, longitude, and event title
template_feature_vector[0, 0:2] = np.array(event_location)
template_feature_vector[0, 2 : 2 + len(event_vectorized[0])] = event_vectorized[0]

# Predict the effect of the event on each parameter at the event location
predicted_changes = model.predict(template_feature_vector)

# Ensure that the dimensions are compatible
weighted_changes = np.array(predicted_changes * (1 - normalized_distances)).flatten()

# Interpolate to get a smooth heatmap
num_points = 100
lats = np.linspace(lat_min, lat_max, num_points)
lons = np.linspace(lon_min, lon_max, num_points)
grid_lats, grid_lons = np.meshgrid(lats, lons)

# Correcting the weighted_changes shape issue here
grid_changes = griddata(
    lat_lon_grid,
    weighted_changes[: len(lat_lon_grid)],
    (grid_lats, grid_lons),
    method="cubic",
)

# Creating a Folium map to plot the heatmap
m = folium.Map(location=event_location, zoom_start=15)

# Adding a heatmap layer to the map using the interpolated data
HeatMap(
    np.column_stack((grid_lats.ravel(), grid_lons.ravel(), grid_changes.ravel())),
    radius=10,
).add_to(m)

# Show the map
m.save("event_effect_heatmap.html")
