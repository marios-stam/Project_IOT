from flask import Flask
from flask_restful import Api
from .sensor_resources import Sensors, Measurements, AllSensors, SensorSendMessage

SERVER_IP = ""


def init_app():
    """Initialize the core application."""
    # =========== FLASK ===========
    app = Flask(__name__)
    api = Api(app)

    # Routing RESTful API endpoints
    api.add_resource(Sensors, '/sensor/<string:sensor_id>', '/sensor')
    api.add_resource(Measurements, '/measurement/<string:sensor_id>', '/measurement/<string:sensor_id>/<int:count>')
    api.add_resource(AllSensors, '/sensor_list')
    api.add_resource(SensorSendMessage, '/send_msg/<string:sensor_id>/<string:msg>')

    return app