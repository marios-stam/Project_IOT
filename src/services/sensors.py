from multiprocessing import Process, Pipe
from uuid import uuid4
from utils import *
import requests
import json

# =========== CONSTANTS ===========
ARRAY_SIZE = 5                              # Number of bins in infrastructure
CENTER_POS = {
    'x': 38.246639,
    'y': 21.734573
}                                           # Center position to randomly scatter bins
FILL_RATE = 2.5                             # Fill rate (each interval)
AMBIENT_TEMP = 25                           # Ambient (starting) temperature
AUTO_DEATH = 2 * 60 * 60 * 24               # Automatically kill process after (seconds)
INTERVAL = 30                               # Interval between measurements (seconds)
FIRE_PERC = 0.005                           # Chance of bin catching fire (each interval)
FIRE_TEMP = 135                             # Temperature of bin when on fire
TILT_PERC = 0.005                           # Chance of bin being overturned (each interval)
BATTERY_RATE = 0.007                        # Rate at which battery is depleted (each interval)
MAX_MEASURE_PER_REQ = 10                    # Maximum measurements returned per request
SERVER_IP = "http://31.208.108.233:5000/"   # Central server IP address


class Sensor:
    interval = 60 ** 2

    def __init__(self, pipe, sensor_id, position=None):

        # Initialize sensor data
        self.sensor_id = sensor_id
        self.start_time = datetime.now()
        self.battery = 1.0
        self.fallen_status = False
        self.fire_status = False
        self.prev_time = datetime.min
        self.history = []

        # Initialize position
        if position is not None:
            self.lat = position['x']
            self.long = position['y']
        else:
            self.lat = CENTER_POS['x']
            self.long = CENTER_POS['y']
        self.lat += 0.06 * rand_perc(center=True)
        self.long += 0.06 * rand_perc(center=True)

        self.process = Process(target=self.loop, args=(pipe, ))

    def loop(self, pipe):
        fullness = rand_perc()

        while True:
            if diff_time(self.prev_time, datetime.now()) > INTERVAL:

                # Set fill level
                fullness += FILL_RATE * (1 + 0.2 * rand_perc(center=True))
                fullness = min(fullness, 1.0)

                # Set temperature
                if rand_check(FIRE_PERC):
                    self.fire_status = not self.fire_status
                if self.fire_status:
                    temp = FIRE_TEMP + (60 * rand_perc())
                else:
                    temp = AMBIENT_TEMP + (8 * rand_perc())

                # Set tilt
                if rand_check(TILT_PERC):
                    self.fallen_status = not self.fallen_status
                if self.fallen_status:
                    tilt = AccelData(0, 9.81, 0)
                else:
                    tilt = AccelData(0, 0, 9.81)

                # Set battery
                self.battery -= BATTERY_RATE * (1 + 0.2 * rand_perc(center=True))
                self.battery = max(self.battery, 0.0)

                # Reset previous time
                self.prev_time = datetime.now()

                msg = {
                    'sensor_id': self.sensor_id,
                    'lat': self.lat,
                    'long': self.long,
                    'fall_status': self.fallen_status,
                    'battery': self.battery,
                    'time_online': int(diff_time(self.start_time, datetime.now())),
                    'entry_id': str(uuid4()),
                    'timestamp': datetime.strftime(self.prev_time, '%Y-%m-%d %H:%M:%S.000'),
                    'fill_level': fullness,
                    'temperature': temp,
                    'fire_status': self.fire_status,
                    'orientation': dict(tilt)
                }

                self.history.append(msg)
                # self.history = [msg]

                # Fix for transmission
                msg['orientation'] = json.dumps(msg['orientation'])
                try:
                    requests.put(SERVER_IP + "/bins", json=msg)
                    print("Sent message to server at", msg['timestamp'])
                except requests.exceptions.ConnectionError:
                    print("Server unreachable")

            if pipe.poll(INTERVAL * 0.1):
                cmd = pipe.recv()
                if cmd == 'get_details':
                    pipe.send({
                        'sensor_id': self.sensor_id,
                        'lat': self.lat,
                        'long': self.long,
                        'battery': self.battery,
                        'time_online': int(diff_time(self.start_time, datetime.now())),
                        'last_measurement': datetime.strftime(self.prev_time, '%d/%m/%Y %H:%M:%S')
                    })

                if cmd.startswith('get_measurements'):
                    n = int(cmd.split()[1])
                    pipe.send(self.history[-n:][::-1])

                if cmd == 'toggle_fire':
                    self.fire_status = not self.fire_status

                if cmd == 'toggle_fall':
                    self.fallen_status = not self.fire_status


class SensorGateway:
    def __init__(self):
        super().__init__()

        self.history = []
        self.sensors = {}
        self.pipes = {}

        for i in range(ARRAY_SIZE):
            tmp_id = str(uuid4())
            parent, child = Pipe()
            self.sensors[tmp_id] = Sensor(child, tmp_id)
            self.pipes[tmp_id] = parent

        for sensor in self.sensors:
            self.sensors[sensor].process.start()

    def get_sensor_IDs(self):
        return list(self.sensors.keys())

    def get_last_measurements(self, sensor_id, n=1):
        pipe = self.pipes[sensor_id]
        pipe.send('get_measurements ' + str(min(n, MAX_MEASURE_PER_REQ)))
        return pipe.recv()

    def get_sensor_details(self, sensor_id):
        pipe = self.pipes[sensor_id]
        pipe.send('get_details')
        return pipe.recv()
