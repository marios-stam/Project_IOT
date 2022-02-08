from flask import Blueprint, make_response
from flask import current_app as app
from ..models import db, Bin
from datetime import datetime as dt
from flask import request, jsonify
from .db_interface import *

regression_blueprint = Blueprint('regression_blueprint', __name__)


# @bins_blueprint.route('/regression', methods=['POST'])  # create new bin
# def create_bin_route():
#     return create_bin()
#
#
# @bins_blueprint.route('/regression', methods=['PUT'])  # update a bin
# def update_bin_route():
#     # return update_bin()
#     return create_bin()


@regression_blueprint.route('/regression/<sensor_id>', methods=['GET'])  # get an angle prediction
def get_angle_prediction(sensor_id):
    return get_angle(sensor_id)
