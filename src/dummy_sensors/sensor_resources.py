from flask_restful import Resource, abort
from .__config__ import SERVER_IP
from .sensor_classes import SensorGateway

# Creating gateway
gateway = SensorGateway(server=SERVER_IP)


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