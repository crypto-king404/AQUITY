import pandas as pd
import requests
import csv

# Replace with your API key
api_key = "REDACTED-PERSONAL-API-KEY"


# Function to get elevation for a given latitude and longitude
def get_elevation(latitude, longitude):
    url = f"https://maps.googleapis.com/maps/api/elevation/json?locations={latitude},{longitude}&key={api_key}"
    response = requests.get(url)
    data = response.json()
    elevation = data["results"][0]["elevation"]
    return elevation


input_file = "datasets/final_events_2.csv"
output_file = "datasets/elevations.csv"

with open(input_file, "r") as csv_in, open(output_file, "w", newline="") as csv_out:
    reader = csv.DictReader(csv_in)
    fieldnames = reader.fieldnames + ["Elevation"]
    writer = csv.DictWriter(csv_out, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        lat = row["Latitude"]
        lng = row["Longitude"]
        elevation = get_elevation(lat, lng)
        row["Elevation"] = elevation
        writer.writerow(row)
