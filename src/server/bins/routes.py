from flask import Blueprint, make_response
from flask import current_app as app
from ..models import db, Bin
from datetime import datetime as dt
from flask import request, jsonify
from .db_interface import tested, get_bin, create_bin, update_bin, get_all_bins, get_bins_by_status, get_bins_within_radius
import json

bins_blueprint = Blueprint('bins_blueprint', __name__)


@bins_blueprint.route('/test')
def test():
    return tested()


@bins_blueprint.route('/test/bin')  # create new bin
def test_create_bin_route(id=None, status=None, fullness=None, updated=None, position=None):
    return create_bin(id, status, fullness, updated, position)


@bins_blueprint.route('/bins', methods=['POST'])  # create new bin
def create_bin_route():
    return create_bin()


@bins_blueprint.route('/bins', methods=['PUT'])  # update a bin
def update_bin_route():
    return update_bin()


@bins_blueprint.route('/bins/<bin_id>', methods=['GET'])  # get a bin
def get_bin_route(bin_id):
    return get_bin(bin_id)


@bins_blueprint.route('/bins/get_all', methods=['GET'])  # get all bins
def get_all_bins_route():
    return get_all_bins()


@bins_blueprint.route('/bins_within_radius')
def get_bins_within_radius_route(pos_long=None, pos_lat=None, radius=None):
    pos_long = request.args.get('long', type=float)
    pos_lat = request.args.get('lat', type=float)
    radius = request.args.get('radius', type=float)

    #radius in km
    print(pos_long, pos_lat, radius)

    pos_long, pos_lat, radius = float(pos_long), float(pos_lat), float(radius)
    pos = (pos_long, pos_lat)
    return get_bins_within_radius(pos, radius)
