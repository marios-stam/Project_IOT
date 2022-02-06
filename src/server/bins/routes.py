from flask import Blueprint, make_response
from flask import current_app as app
from ..models import db, Bin
from datetime import datetime as dt
from flask import request, jsonify
from .db_interface import tested, get_bin, create_bin, update_bin
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

@bins_blueprint.route('/bins', methods=['GET'])
def list_bin_route():
    pass

# Θέλω να γυρνάει λίστα με JSONs.
# 
# return jsonify(data)
# 
# Όπου data θα είναι της μορφής:
# data = [geojson1, geojson2, ...]
# 
# και κάθε geojson της μορφής:
# geojson = {
#     'type': "Feature",
#     'properties': {
#         'id': "id",
#         'status': "status",
#         'updated': "updated",
#         'fullness': "fullness",
#     },
#     'geometry': {'type': "Point", 'coordinates': ["lon", "lat"]},
# }
# 
# Από τη db να είναι: "id", "status", "updated", "fullness", "lon" (longitude in degrees), "lat" (latitude in degrees)
# Άρα στήλη position πρέπει να σπάσει σε δύο στήλες lon και lat
# 
# Τεστ συντεταγμένες: [21.734068, 38.245932], [21.73601, 38.246417], [21.736659, 38.24597], [21.733017, 38.247251], [21.737346, 38.247533]
# Τεστ fullness να είναι μοιρασμένα στα διαστήματα: (0, 20), (20, 40), (40, 60), (60, 80), (80, 100)
