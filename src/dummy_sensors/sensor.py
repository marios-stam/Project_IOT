from multiprocessing import Process
from uuid import uuid4
from .utils import *
import requests
import json
from .__config__ import *


class Sensor:

    def __init__(self, pipe, sensor_id, server, position=None):

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
        self.lat += SCATTER * rand_perc(center=True)
        self.long += SCATTER * rand_perc(center=True)

        # Initialize structure
        self.process = Process(target=self.loop, args=(pipe, ))
        self.server = server

    def update(self):

        if not self.fallen_status and not self.fire_status:
            # Set fill level
            self.fullness += max(FILL_RATE * (1 + FILL_COVAR * rand_perc(center=True)), 0) if rand_perc() > NO_TRASH_CHANCE else 0
            self.fullness = min(self.fullness, 1.0)

        # Set temperature
        if rand_check(FIRE_PERC):
            self.fire_status = not self.fire_status
        if self.fire_status:
            temp = FIRE_TEMP + (FIRE_TEMP_COVAR * rand_perc())
        else:
            temp = AMBIENT_TEMP + (AMBIENT_TEMP_COVAR * rand_perc())

        # Set tilt
        if rand_check(TILT_PERC):
            self.fallen_status = not self.fallen_status
        if self.fallen_status:
            tilt = AccelData(0, 9.81, 0)
        else:
            tilt = AccelData(0, 0, 9.81)

        # Set battery
        self.battery -= max(BATTERY_RATE * (1 + BATTERY_COVAR * rand_perc(center=True)), 0)
        self.battery = max(self.battery, 0.0)

        # Reset previous time
        self.prev_time = datetime.now()

        

        if self.battery > BATTERY_CRITICAL:
            msg = {
                'sensor_id': self.sensor_id,
                'lat': self.lat,
                'long': self.long,
                'fall_status': self.fallen_status,
                'battery': self.battery,
                'time_online': int(diff_time(self.start_time, datetime.now())),
                'entry_id': str(uuid4()),
                'timestamp': datetime.strftime(self.prev_time, '%Y-%m-%d %H:%M:%S.000'),
                'fill_level': self.fullness,
                'temperature': temp,
                'fire_status': self.fire_status,
                'orientation': dict(tilt)
            }

            self.history.append(msg)
            
            # Fix for transmission
            msg['orientation'] = json.dumps(msg['orientation'])

            try:
                requests.put(self.server + "/bins", json=msg)
                print("Sent message to server at", msg['timestamp'])
            except requests.exceptions.ConnectionError:
                print("Server unreachable")

    def loop(self, pipe):
        if STARTS_AT_ZERO:
            self.fullness = 0.0
        else:
            self.fullness = rand_perc()

        while True:
            if diff_time(self.prev_time, datetime.now()) > INTERVAL:
                self.update()

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
                    continue

                if cmd.startswith('get_measurements'):
                    n = int(cmd.split()[1])
                    pipe.send(self.history[-n:][::-1])
                    continue

                if cmd == 'toggle_fire':
                    self.fire_status = not self.fire_status
                if cmd == 'on_fire':
                    self.fire_status = True
                if cmd == 'off_fire':
                    self.fire_status = False

                if cmd == 'toggle_fall':
                    self.fallen_status = not self.fire_status
                if cmd == 'on_fall':
                    self.fallen_status = True
                if cmd == 'off_fall':
                    self.fallen_status = False

                if cmd == 'charge':
                    self.battery = 1.0
                if cmd == 'discharge':
                    self.battery = BATTERY_CRITICAL + 0.05

                if cmd == 'empty':
                    self.fullness = 0.0
                if cmd == 'fill':
                    self.fullness = 1.0

                pipe.send(self.history[-1:][::-1])
