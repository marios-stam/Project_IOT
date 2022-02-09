from flask import Blueprint, make_response
from flask import current_app as app
from ..models import db, User
from datetime import datetime as dt
from flask import request, jsonify
from .db_interface import *
import json

trucks_blueprint = Blueprint('trucks_blueprint', __name__)


@trucks_blueprint.route('/trucks', methods=['POST'])  # create new truck
def create_truck_route():
    return create_truck()


@trucks_blueprint.route('/trucks', methods=['PUT'])  # update a truck
def update_truck_route():
    return update_truck()


@trucks_blueprint.route('/trucks/<truck_id>', methods=['GET'])  # get a truck
def get_truck_route(truck_id):
    return get_truck(truck_id)


@trucks_blueprint.route('/trucks/fleet_routing', methods=['GET'])
def get_trucks_routing_route():
    return get_trucks_routing()
