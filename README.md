# Project_IOT

Team 4

- Fragiskos Fourlas
- Marios Stamatopoulos
- Nikos Panagiotopoulos

Waste Management & Citizen Engagement

## Note to professor and first user
You can find the Poerpoint presentation of the project at **Powerpoints/Final Presentation/Waste-management-Final.pptx**

The manual of the platform is the file **Waste-Management-Manual.pdf**
## Preperation

### Install dependencies : 
Use the following commands to install all dependencies from the requirements.txt file.
`pip install -r /path/to/requirements.txt`

### API Keys
This software uses two external services that need API keys. ~~Place each key in an empty text document named `api_key.txt`. Place each file in the following directories accordingly~~ 
- ~~`/src/server/trucks/truck_routing/trav_salesman_problem` for the Travelling Salesman problem API key~~
- ~~`/src/server/trucks/truck_routing/mapbox` for the mapbox API key~~

The API keys are uploaded on the repo and the user doesn't need to change or configure anything. The app is ready to run.

### Configuration
Change configuration settings for the dummy sensor service in the `/src/dummy_sensors/__config__.py` file. These parameters should be changed according to user preference in order to present the app better. The current configuration will be used during the grading presentation in class.

Change configuration settings for the server service in the `/src/server/constants.json` file. These parameters should **NOT** be changed in normal usage. The current configuration will be changed by the developers when needed.

## Usage
Run all files from the /src directory ONLY. Start the services using the following commands on a terminal:

- Start server (default is localhost on port 5000)
`python wsgi.py`
- Start dummy sensors service (default is localhost on port 26223)
`python dummy_sensors.py`

View the app on [localhost](http://localhost:5000/) on your browser

To access the dummy sensors API use localhost on port 26223. A good place to start is the [sensor list](http://localhost:26223/sensor_list). 

## Documentation

### Dummy Sensors
You can find the API documentation for dummy sensors [here](/src/dummy_sensors/README.md)

### Server
You can find the API documentation for the server [here](/src/server/README.md). Please note that this documentation is *INCOMPLETE*.
