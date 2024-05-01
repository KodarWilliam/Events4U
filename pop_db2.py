import sqlite3
import requests
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_events_from_ticketmaster():
    ticketmaster_api_key = os.getenv('TICKETMASTER_API_KEY')
    today = datetime.now()
    next_month = today + timedelta(days=30)
    url = (f"https://app.ticketmaster.com/discovery/v2/events.json?apikey={ticketmaster_api_key}&"
           f"startDateTime={today.strftime('%Y-%m-%dT%H:%M:%SZ')}&"
           f"endDateTime={next_month.strftime('%Y-%m-%dT%H:%M:%SZ')}")
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
            inserted_rows += 1  # Increment counter for each inserted row
        except sqlite3.IntegrityError:
            print(f"Skipping duplicate event: {name}")

    conn.commit()
    conn.close()

    print(f"{inserted_rows} rows were inserted into the database.")

events = get_events_from_ticketmaster()
insert_events_into_db(events)
print("Events have been added to the database.")
