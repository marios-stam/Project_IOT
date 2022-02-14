# Project_IOT

Team 4

- Fragiskos Fourlas
- Marios Stamatopoulos
- Nikos Panagiotopoulos

Smart Garbage Management

## Preperation

### Install dependencies : 
Use the following commands to install all dependencies from the requirements.txt file.
`pip install -r /path/to/requirements.txt`

### API Keys
This software uses two external services that need API keys. Place each key in an empty text document named `api_key.txt`. Place each file in the following directories accordingly
- `/src/server/trucks/truck_routing/trav_salesman_problem` for the Travelling Salesman problem API key
- `/src/server/trucks/truck_routing/mapbox` for the mapbox API key

### Configuration
Change configuration settings for the dummy sensor service in the `/src/dummy_sensors/__config__.py` file. These parameters should be changed according to user preference in order to present the app better. The current configuration will be used during the grading presentation in class.

Change configuration settings for the server service in the `/src/server/constants.json` file. These parameters should NOT be changed in normal usage. The current configuration will be changed by the developers when needed.

## Usage
Run all files from the /src directory ONLY

Start server (default is localhost on port 5000)
`python wsgi.py`

Start dummy sensors service (default is localhost on port 26223)
`python dummy_sensors.py`