from flask import Flask, jsonify, request, abort
from flasgger import Swagger
import sqlite3

app = Flask(__name__)
Swagger(app)

def get_db_connection():
    conn = sqlite3.connect('events.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/events', methods=['GET'])
def get_events():
    """Endpoint to list all events
    ---
    responses:
      200:
        description: A list of all events
        schema:
          id: Events
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                description: The event's ID
              name:
                type: string
                description: The name of the event
              event_date:
                type: string
                format: date
                description: The date of the event
              venue:
                type: string
                description: The venue of the event
              city:
                type: string
                description: The city of the event
              country:
                type: string
                description: The country of the event
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM events')
    events = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in events])

@app.route('/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    """Endpoint to get a specific event
    ---
    parameters:
      - name: event_id
        in: path
        type: integer
        required: true
        description: The ID of the event
    responses:
      200:
        description: An event object
        schema:
          id: Event
          properties:
            id:
              type: integer
              description: The event's ID
            name:
              type: string
              description: The name of the event
            event_date:
              type: string
              format: date
              description: The date of the event
            venue:
              type: string
              description: The venue of the event
            city:
              type: string
              description: The city of the event
            country:
              type: string
              description: The country of the event
      404:
        description: Event not found
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM events WHERE id = ?', (event_id,))
    event = cursor.fetchone()
    conn.close()

    if event is None:
        abort(404, description="Resource not found")
    
    return jsonify(dict(event))

@app.route('/events', methods=['POST'])
def create_event():
    """Endpoint to create a new event
    ---
    parameters:
      - in: body
        name: event
        schema:
          id: Event
          required:
            - name
            - event_date
          properties:
            name:
              type: string
              description: The name of the event
            event_date:
              type: string
              format: date
              description: The date of the event
            venue:
              type: string
              description: The venue of the event
            city:
              type: string
              description: The city of the event
            country:
              type: string
              description: The country of the event
    responses:
      201:
        description: The event was created successfully
        schema:
          id: Event
          properties:
            id:
              type: integer
              description: The event's ID
    """
    if not request.json or not 'name' in request.json:
        abort(400, description="Missing name or other required data")

    event = {
        'name': request.json['name'],
        'event_date': request.json.get('event_date', ''),
        'venue': request.json.get('venue', ''),
        'city': request.json.get('city', ''),
        'country': request.json.get('country', '')
    }

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO events (name, event_date, venue, city, country) 
                      VALUES (?, ?, ?, ?, ?)''', 
                   (event['name'], event['event_date'], event['venue'], event['city'], event['country']))
    event_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return jsonify(event), 201, {'Location': f"/events/{event_id}"}

@app.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    """Endpoint to delete an event
    ---
    parameters:
      - name: event_id
        in: path
        type: integer
        required: true
        description: The ID of the event to delete
    responses:
      200:
        description: Event deleted successfully
      404:
        description: Event not found
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM events WHERE id = ?', (event_id,))
    deleted_rows = cursor.rowcount
    conn.commit()
    conn.close()

    if deleted_rows == 0:
        abort(404, description="Resource not found")

    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True)
