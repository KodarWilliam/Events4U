
# Events4U API Documentation

This project provides a local event finder API by integrating with the Ticketmaster API. It allows users to find events based on their location and interact with event data through a RESTful API.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need to have Python installed on your machine and preferably use a virtual environment to manage the dependencies.

### Installing

Follow these steps to get your development environment running:

1. Clone the repository to your local machine.
2. Navigate to the project directory.

```bash
cd path_to_your_project
```

3. Install the required packages using the provided `requirements.txt`.

```bash
pip install -r requirements.txt
```

4. Create the SQLite database and the required table by running the `database_creation.py` script.

```bash
python database_creation.py
```

5. Populate the database with events by running the `pop_db.py` script. You will be prompted to enter a city and country.

```bash
python pop_db.py
```

6. (Alternative) Populate the database with events for all locations by running the pop_db2.py script, which does not require city and country parameters.

```bash
python pop_db2.py
```

7. Run the Flask application using the `main.py` script.

```bash
python main.py
```

### Usage

After starting the Flask application, you can access the API documentation and test the endpoints by navigating to:

```
http://localhost:5000/apidocs
```

This will open the Swagger UI where you can see all available endpoints and perform actions like retrieving events, creating a new event, or deleting an existing one.

## Authors

* **William Svensson** - *Initial work* - [YourGithub](https://github.com/KodarWilliam)

