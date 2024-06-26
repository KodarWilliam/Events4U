import sqlite3
import requests
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_coordinates_for_city(city, country):
    opencage_api_key = os.getenv('OPENCAGE_API_KEY')
    query = f"{city}, {country}"
    url = f'https://api.opencagedata.com/geocode/v1/json?q={query}&key={opencage_api_key}'
    response = requests.get(url)
    if response.status_code == 200 and response.json()['results']:
        result = response.json()['results'][0]
        return result['geometry']['lat'], result['geometry']['lng']
    return None, None

def get_events_by_coordinates(latitude, longitude):
    ticketmaster_api_key = os.getenv('TICKETMASTER_API_KEY')
    today = datetime.now()
    next_week = today + timedelta(days=7)
    url = (f"https://app.ticketmaster.com/discovery/v2/events.json?apikey={ticketmaster_api_key}&"
           f"latlong={latitude},{longitude}&startDateTime={today.strftime('%Y-%m-%dT%H:%M:%SZ')}&"
           f"endDateTime={next_week.strftime('%Y-%m-%dT%H:%M:%SZ')}")
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('_embedded', {}).get('events', [])
    return []

def insert_events_into_db(events):
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    inserted_rows = 0

    for event in events:
        event_id = event['id']  # Extract event ID
        name = event.get('name', 'No title')

        # Extract event date and time
        event_date_str = event['dates']['start'].get('localDate', '1970-01-01')
        event_time_str = event['dates']['start'].get('localTime', '00:00:00')
        event_datetime_str = f"{event_date_str} {event_time_str}"

        # Convert the combined string into a datetime object
        event_date = datetime.strptime(event_datetime_str, '%Y-%m-%d %H:%M:%S')

        # Extract venue
        venue = event['_embedded']['venues'][0].get('name', 'Unknown venue')

        # Extract city
        city = event['_embedded']['venues'][0]['city'].get('name', 'Unknown city')

        # Extract country
        country = event['_embedded']['venues'][0]['country'].get('name', 'Unknown country')

        # Insert into the database
        try:
            cursor.execute('''INSERT INTO events (id, name, event_date, venue, city, country)
                              VALUES (?, ?, ?, ?, ?, ?)''', (event_id, name, event_date.strftime('%Y-%m-%d %H:%M:%S'), venue, city, country))
            inserted_rows += 1
        except sqlite3.IntegrityError:
            print(f"Skipping duplicate event: {name}")

    conn.commit()
    conn.close()

    print(f"{inserted_rows} rows were inserted into the database.")

city = input("Enter the name of your city: ")
country = input("Enter the name of your country: ")
latitude, longitude = get_coordinates_for_city(city, country)

if latitude and longitude:
    events = get_events_by_coordinates(latitude, longitude)
    insert_events_into_db(events)
    print(f"Events for {city}, {country} have been added to the database.")
else:
    print("Could not find coordinates for the given city and country.")
