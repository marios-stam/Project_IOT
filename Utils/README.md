# Utilities

## Dummy Sensors

dummy_sensors.py is a script that generates mock data for testing. The data are accessed via RESTful API.

### Sensor Implementation
Each dummy sensor is a Sensor object that contains an id, characteristics and mock data values, a Process and a Pipe 
connection.
- The ID is a UUID v.4 unique for the Sensor
- Mock data are either final for the Sensor (e.g. position) or dynamically changing by time
- Each sensor has a separate Process running that handles commands and implements data change with time
- Communication with the Process is done with a Pipe

A parent class SensorGateway implements a data collector (e.g. LoRaWAN Server) that creates Sensors, keeps them in a 
list and handles get/post/put requests from the API using the Sensor Pipes

### API Implementation
The RESTful API implemented in this script is built on top of flask using flask-restful. It uses 3 endpoints to 
communicate with the sensors.

#### /sensor_list
**GET** to receive list of IDs of active sensors
```shell
$ curl http://localhost:5000/sensor_list
[
    "0c8e145e-4cec-479e-8c3a-2129285e6db7",
    "6a287ea3-9305-4335-ad81-86b6d0f9f552",
    "9eab94b4-5c89-47c7-88d2-3fc5f1cf6206",
    "0cfb5b3e-c16a-4b85-b3ee-357cd5a015ff",
    "6d95f42a-c7b4-460c-b044-4588e7041f62"
]
```

### /sensor/<sensor_id>
**GET** to receive the status of a sensor


```shell
$ curl http://localhost:5000/sensor/0c8e145e-4cec-479e-8c3a-2129285e6db7
{
    "sensor_id": "0c8e145e-4cec-479e-8c3a-2129285e6db7",
    "position": {
        "x": 38.151837703999995,
        "y": 21.7170638
    },
    "battery": 0.9783687778,
    "time_online": 1844,
    "last_measurement": "25/11/2021 02:07:58"
}
```

**POST** to create new sensors
```shell
$ culr http://localhost:5000/sensor -X POST -v
{'message': 'Not implemented yet'}
```

**PUT** to change sensor values (e.g. put out a fire)
```shell
$ culr http://localhost:5000/sensor -d "cmd=toggle_fire" -X PUT -v
{'message': 'Not implemented yet'}
```

### /measurement/<sensor_id>/<count>
**GET** to receive last *count* measurements of a sensor (/count is optional, defaults to 1)
```shell
$ curl http://localhost:5000/measurement/0c8e145e-4cec-479e-8c3a-2129285e6db7/2
[
    {
        "sensor_id": "0c8e145e-4cec-479e-8c3a-2129285e6db7",
        "measurement": {
            "id": "5b34d500-d1d1-48e8-a8ee-de109c41f804",
            "timestamp": "25/11/2021 02:38:23",
            "fill_level": 0.69993232,
            "temperature": 29.788464,
            "fire_status": false,
            "orientation": {
                "x": 0,
                "y": 0,
                "z": 9.81
            },
            "fall_status": false
        }
    },
    {
        "sensor_id": "0c8e145e-4cec-479e-8c3a-2129285e6db7",
        "measurement": {
            "id": "79a50908-793f-405d-b22e-c70b6ba9fb9b",
            "timestamp": "25/11/2021 02:07:58",
            "fill_level": 0.658775612,
            "temperature": 32.8654256,
            "fire_status": false,
            "orientation": {
                "x": 0,
                "y": 0,
                "z": 9.81
            },
            "fall_status": false
        }
    }
]
```