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
    else:
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
    
    for event in events:
        name = event.get('name')
        event_date = datetime.strptime(event['dates']['start']['localDate'], '%Y-%m-%d')
        venue = event['_embedded']['venues'][0].get('name', 'Unknown venue')
        city = event['_embedded']['venues'][0]['city'].get('name', 'Unknown city')
        country = event['_embedded']['venues'][0]['country'].get('name', 'Unknown country')
        
        cursor.execute('''INSERT INTO events (name, event_date, venue, city, country)
                          VALUES (?, ?, ?, ?, ?)''', (name, event_date, venue, city, country))
    
    conn.commit()
    conn.close()

city = input("Enter the name of your city: ")
country = input("Enter the name of your country: ")
latitude, longitude = get_coordinates_for_city(city, country)

if latitude and longitude:
    events = get_events_by_coordinates(latitude, longitude)
    insert_events_into_db(events)
    print(f"Events for {city}, {country} have been added to the database.")
else:
    print("Could not find coordinates for the given city and country.")
