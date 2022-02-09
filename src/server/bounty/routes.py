from flask import Blueprint
from .db_interface import *

bounty_blueprint = Blueprint('bounty_blueprint', __name__)


@bounty_blueprint.route('/bounty/<sensor_id>', methods=['GET'])  # get an angle prediction
def get_angle_prediction(sensor_id):
    return get_angle(sensor_id)
