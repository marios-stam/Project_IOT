from flask import Flask
from flask_restful import Api
from flask_restful import Resource, abort
from .__config__ import SERVER_IP
from .gateway import SensorGateway
import os


# =========== FLASK ===========
class App(Flask):
    def __init__(self, *args, **kwargs):
        # print("FLASK TEST", os.getpid())
        super().__init__(*args, **kwargs)
        self.gateway = SensorGateway(server=SERVER_IP)

    def run(self, *args, **kwargs):
        self.gateway.start_processes()
        super().run(*args, **kwargs)


# =========== RESOURCE CLASSES ===========
class Sensors(Resource):
    def __init__(self, gateway, *args, **kw):
        self.gateway = gateway
        super().__init__(*args, **kw)

    def get(self, sensor_id=None):
        if sensor_id in self.gateway.get_sensor_IDs():
            return self.gateway.get_sensor_details(sensor_id), 200
        elif sensor_id is None:
            abort(400, message="No ID provided")
        else:
            abort(404, message="Sensor with ID {} doesn't exist".format(sensor_id))

    def post(self, sensor_id=None):
        abort(501, message="Not implemented yet")

    def put(self, sensor_id=None):
        abort(501, message="Not implemented yet")

    def delete(self, sensor_id=None):
        if sensor_id in self.gateway.get_sensor_IDs():
            abort(501, message="Not implemented yet")
        elif sensor_id is None:
            abort(400, message="No ID provided")
        else:
            abort(404, message="Sensor with ID {} doesn't exist".format(sensor_id))


class Measurements(Resource):
    def __init__(self, gateway, *args, **kw):
        self.gateway = gateway
        super().__init__(*args, **kw)

    def get(self, sensor_id, count=1):
        if sensor_id in self.gateway.get_sensor_IDs():
            return self.gateway.get_last_measurements(sensor_id, count), 200
        else:
            abort(404, message="Sensor with ID {} doesn't exist".format(sensor_id))


class AllSensors(Resource):
    def __init__(self, gateway, *args, **kw):
        self.gateway = gateway
        super().__init__(*args, **kw)
        
    def get(self):
        return self.gateway.get_sensor_IDs(), 200


class Kill(Resource):
    def __init__(self, gateway, *args, **kw):
        self.gateway = gateway
        super().__init__(*args, **kw)
        
    def get(self):
        pass

class SensorSendMessage(Resource):
    def __init__(self, gateway, *args, **kw):
        self.gateway = gateway
        super().__init__(*args, **kw)
        
    def post(self, sensor_id, msg):
        if sensor_id in self.gateway.get_sensor_IDs():
            return self.gateway.send_msg(sensor_id, msg), 200
        elif sensor_id is None or msg is None:
            abort(400, message="No ID or Message provided")
        else:
            abort(404, message=f"Sensor with ID {sensor_id} doesn't exist")


def init_app():
    """Initialize the core application."""

    app = App(__name__)
    api = Api(app)
    
    # Routing RESTful API endpoints
    api.add_resource(Sensors, '/sensor/<string:sensor_id>', '/sensor')
    api.add_resource(Measurements, '/measurement/<string:sensor_id>', '/measurement/<string:sensor_id>/<int:count>')
    api.add_resource(AllSensors, '/sensor_list')
    api.add_resource(SensorSendMessage, '/send_msg/<string:sensor_id>/<string:msg>')

    return app 