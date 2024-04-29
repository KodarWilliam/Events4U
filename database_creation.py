import sqlite3

# Connect to the SQLite database. If the file does not exist, it will be created.
conn = sqlite3.connect('events.db')
cursor = conn.cursor()

# Check if the 'events' table already exists.
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='events'")
table_exists = cursor.fetchone()

# If the table does not exist, create it.
if not table_exists:
    sql = '''CREATE TABLE events(
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       name TEXT NOT NULL,
       event_date DATETIME NOT NULL,
       venue TEXT,
       country TEXT NOT NULL,
       city TEXT NOT NULL
    )'''
    cursor.execute(sql)
    print("Table 'events' created successfully.")
else:
    print("Table 'events' already exists.")

# Commit the changes and close the connection
conn.commit()
conn.close()
