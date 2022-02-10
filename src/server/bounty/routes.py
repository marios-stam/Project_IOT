from flask import Blueprint, make_response
from flask import current_app as app
from ..models import db, Bounty
from datetime import datetime as dt
from flask import request, jsonify
from .db_interface import *
import json

bounties_blueprint = Blueprint('bounties_blueprint', __name__)


@bounties_blueprint.route('/bounties', methods=['POST'])  # create new bounty
def create_bounty_route():
    return create_bounty()


@bounties_blueprint.route('/bounties', methods=['PUT'])  # update a bounty
def update_bounty_route():
    return update_bounty()


# get a bounty
@bounties_blueprint.route('/bounties/<bounty_id>', methods=['GET'])
def get_bounty_route(bounty_id):
    return get_bounty(bounty_id)


# get all bounties
@bounties_blueprint.route('/bounties/get_all', methods=['GET'])
def get_all_bounties_route():
    return get_all_bounties()


# get uncompleted bounties within radius
@bounties_blueprint.route('/bounties/get_uncompleted_bounties_in_radius', methods=['PUT'])
def get_uncompleted_bounties_in_radius_route():
    return get_uncompleted_bounties_in_radius()


# complete a bounty
@bounties_blueprint.route('/bounties/complete_bounty', methods=['PUT'])
def complete_bounty_route():
    data = request.get_json()
    bounty_id = data['id']
    usr_id = data['assigned_usr_id']

    return complete_bounty(bounty_id, usr_id)


# assign a bounty
@bounties_blueprint.route('/bounties/assign_bounty', methods=['PUT'])
def assign_bpunty_route():
    data = request.get_json()
    bounty_id = data['id']
    usr_id = data['assigned_usr_id']

    return assign_bounty(bounty_id, usr_id)
