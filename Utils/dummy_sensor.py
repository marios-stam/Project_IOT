from flask import Flask
from flask_restful import Resource, Api
from multiprocessing import Process
from queue import Queue
from uuid import uuid4
from datetime import datetime
from time import sleep
from random import randint

ARRAY_SIZE = 10
CENTER_POS = {'x': 38.246639, 'y': 21.734573}
FILL_RATE = 0.05

app = Flask(__name__)
api = Api(app)

sensorArray = []
queue = Queue()


def diff_time(t1, t2):
    if type(t1) is str:
        t1 = datetime.strptime(t1, '%d/%m/%Y %H:%M:%S')
    if type(t1) is str:
        t2 = datetime.strptime(t2, '%d/%m/%Y %H:%M:%S')

    res = t2 - t1
    if res.days < 0: raise Exception("Cannot process measurement from the future!")

    return int(res.total_seconds())


def rand_perc(inc=False, neg=False, center=False):
    res = randint(0, 1000000) / 1000000
    if inc: return res + 1
    if neg: return res * -1
    if center: return (res - 0.5) * 2


TEMPLATE = {
    'id': 'bba10e9b-32da-427f-82b9-0420aafe6528',
    'timestamp': '23/11/2021 18:58:32'
}


class Sensor(Process):
    interval = 60 ** 2

    def __init__(self, position):
        self.id = str(uuid4())

        self.position = CENTER_POS
        self.position['x'] += randint(-9999, 9999) / 100000
        self.position['y'] += randint(-9999, 9999) / 100000

        super().__init__(target=self.loop, args=(self.id, queue))

    @staticmethod
    def loop(id, queue):
        start_time = datetime.now()
        prev_time = datetime.min

        while True:
            print("Test")

            sleep(.5)


class SensorGateway(Resource):

    def __init__(self):
        super().__init__()

        self.history = []
        for i in range(ARRAY_SIZE):
            sensorArray.append(Sensor())

        for sensor in sensorArray:
            sensor.start()

    def measure(self):
        pass

    @staticmethod
    def sensor_IDs():
        return [sensor.id for sensor in sensorArray]

    def get(self):
        pass

    def put(self):
        pass


# api.add_resource(Sensor, '/')

if __name__ == '__main__':
    pass
