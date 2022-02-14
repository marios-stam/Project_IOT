import os
from uuid import uuid4
from multiprocessing import Pipe
from .__config__ import *
from .sensor import Sensor

class SensorGateway:
    RUNNING = False

    def __init__(self, server):
        print("Creating SensorGateway", os.getpid())

        self.history = []
        self.sensors = {}
        self.pipes = {}

        for i in range(ARRAY_SIZE):
            tmp_id = str(uuid4())
            parent, child = Pipe()
            self.sensors[tmp_id] = Sensor(child, tmp_id, server)
            self.pipes[tmp_id] = parent

    def start_processes(self):
        if SensorGateway.RUNNING:
            return

        print("Running SensorGateway", os.getpid())
        SensorGateway.RUNNING = True
        for sensor in self.sensors:
            self.sensors[sensor].process.start()

    def get_sensor_IDs(self):
        return list(self.sensors.keys())

    def send_msg(self, sensor_id, msg):
        pipe = self.pipes[sensor_id]
        pipe.send(msg)
        return pipe.recv()

    def get_last_measurements(self, sensor_id, n=1):
        return self.send_msg(sensor_id, 'get_measurements ' + str(min(n, MAX_MEASURE_PER_REQ)))

    def toggle_fire(self, sensor_id):
        return self.send_msg(sensor_id, 'toggle_fire')

    def toggle_fall(self, sensor_id):
        return self.send_msg(sensor_id, 'toggle_fall')

    def get_sensor_details(self, sensor_id):
        pipe = self.pipes[sensor_id]
        pipe.send('get_details')
        return pipe.recv()
