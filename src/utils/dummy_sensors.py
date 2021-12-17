from flask import Flask
from flask_restful import Resource, Api, abort
from multiprocessing import Process, Pipe
from uuid import uuid4
from datetime import datetime
from utils import diff_time, rand_perc, rand_check

# =========== CONSTANTS ===========
ARRAY_SIZE = 5                  # Number of bins in infrastructure
CENTER_POS = {
        'x': 38.246639,
        'y': 21.734573
    }                           # Center position to randomly scatter bins
FILL_RATE = 0.05                # Fill rate (each interval)
AMBIENT_TEMP = 25               # Ambient (starting) temperature
AUTO_DEATH = 2 * 60 * 60 * 24   # Automatically kill process after (seconds)
INTERVAL = 5                    # Interval between measurements (seconds)
FIRE_PERC = 0.005               # Chance of bin catching fire (each interval)
FIRE_TEMP = 135                 # Temperature of bin when on fire
TILT_PERC = 0.005               # Chance of bin being overturned (each interval)
BATTERY_RATE = 0.007            # Rate at which battery is depleted (each interval)
MAX_MEASURE_PER_REQ = 10        # Maximum measurements returned per request


# =========== FLASK ===========
app = Flask(__name__)
api = Api(app)


# =========== HELPER CLASSES ===========
class AccelData:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, p):
        self.x += p.x
        self.y += p.y
        self.z += p.z

    def __sub__(self, p):
        self.x -= p.x
        self.y -= p.y
        self.z -= p.z

    def __mul__(self, k: float):
        self.x *= k
        self.y *= k
        self.z *= k

    def __iter__(self):
        yield 'x', self.x
        yield 'y', self.y
        yield 'z', self.z


# =========== RESOURCE CLASSES ===========
class Sensors(Resource):
    def get(self, sensor_id=None):
        if sensor_id in gateway.get_sensor_IDs():
            return gateway.get_sensor_details(sensor_id), 200
        elif sensor_id is None:
            abort(400, message="No ID provided")
        else:
            abort(404, message="Sensor with ID {} doesn't exist".format(sensor_id))

    def post(self, sensor_id=None):
        abort(501, message="Not implemented yet")

    def put(self, sensor_id=None):
        abort(501, message="Not implemented yet")

    def delete(self, sensor_id=None):
        if sensor_id in gateway.get_sensor_IDs():
            abort(501, message="Not implemented yet")
        elif sensor_id is None:
            abort(400, message="No ID provided")
        else:
            abort(404, message="Sensor with ID {} doesn't exist".format(sensor_id))


class Measurements(Resource):
    def get(self, sensor_id, count=1):
        if sensor_id in gateway.get_sensor_IDs():
            return gateway.get_last_measurements(sensor_id, count), 200
        else:
            abort(404, message="Sensor with ID {} doesn't exist".format(sensor_id))


class AllSensors(Resource):
    def get(self):
        return gateway.get_sensor_IDs(), 200


class Kill(Resource):
    def get(self):
        pass


# =========== SENSOR CLASSES ===========
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
            self.position = position
        else:
            self.position = CENTER_POS
        self.position['x'] += 0.06 * rand_perc(center=True)
        self.position['y'] += 0.06 * rand_perc(center=True)

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

                self.history.append({
                    'sensor_id': self.sensor_id,
                    'measurement': {
                        'id': str(uuid4()),
                        'timestamp': datetime.strftime(self.prev_time, '%d/%m/%Y %H:%M:%S'),
                        'fill_level': fullness,
                        'temperature': temp,
                        'fire_status': self.fire_status,
                        'orientation': dict(tilt),
                        'fall_status': self.fallen_status
                    }
                })

            if pipe.poll(INTERVAL * 0.1) is not None:
                cmd = pipe.recv()
                if cmd == 'get_details':
                    pipe.send({
                        'sensor_id': self.sensor_id,
                        'position': dict(self.position),
                        'battery': self.battery,
                        'time_online': int(diff_time(self.start_time, datetime.now())),
                        'last_measurement': datetime.strftime(self.prev_time, '%d/%m/%Y %H:%M:%S')
                    })

                if cmd.startswith('get_measurements'):
                    n = int(cmd.split()[1])
                    pipe.send(self.history[-n:][::-1])

                if cmd == 'toggle_fire': self.fire_status = not self.fire_status

                if cmd == 'toggle_fall': self.fallen_status = not self.fire_status


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


if __name__ == '__main__':
    # Routing RESTful API endpoints
    api.add_resource(Sensors, '/sensor/<string:sensor_id>', '/sensor')
    api.add_resource(Measurements, '/measurement/<string:sensor_id>', '/measurement/<string:sensor_id>/<int:count>')
    api.add_resource(AllSensors, '/sensor_list')

    # Creating gateway
    gateway = SensorGateway()

    # Running Flask server
    app.run(debug=True)
