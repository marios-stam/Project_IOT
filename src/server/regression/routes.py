from flask import Blueprint
from .db_interface import *

regression_blueprint = Blueprint('regression_blueprint', __name__)


@regression_blueprint.route('/regression/<sensor_id>', methods=['GET'])  # get an angle prediction
def get_angle_prediction(sensor_id):
    return get_angle(sensor_id)
