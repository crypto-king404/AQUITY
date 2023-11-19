import requests
import csv
from bs4 import BeautifulSoup

# Replace this URL with the actual URL of the website you want to scrape
url = "https://www.meetboston.com/events/?view=list&sort=date&skip=144&filter_daterange%5Bstart%5D=2023-10-21&filter_daterange%5Bend%5D=2023-11-21"
url2 = "https://www.bostonplans.org/news-calendar/news-updates"
# # Send an HTTP request and parse the HTML content
response = requests.get(url)

if response.status_code == 200:
    # Print the entire HTML content of the webpage
    print(response.text)
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

soup = BeautifulSoup(response.text, "html.parser")

titles = soup.find_all("a", class_="title truncate")

print(titles)
# Locate and extract event information (title, time, address)
events_dict = []
events = []

for event in soup.find_all("div", class_="event"):
    title = event.find("h2").text
    time = event.find("span", class_="event-time").text
    address = event.find("span", class_="event-address").text

    events.append({"title": title, "time": time, "address": address})

# Now you have a list of events with their details


new_events_list = []

for title, event_info in events_dict.items():
    new_event = {
        "title": title,
        "datetime": event_info["Date"],
        "address": event_info["Address"],
    }
    new_events_list.append(new_event)


csv_filename = "events.csv"

fieldnames = ["title", "datetime", "address"]

# Write the data to the CSV file
with open(csv_filename, mode="w", newline="") as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Write the header row
    csv_writer.writeheader()

    # Write the event data
    for event in new_events_list:
        csv_writer.writerow(event)
