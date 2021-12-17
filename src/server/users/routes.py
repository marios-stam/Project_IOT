from flask import Blueprint, make_response
from flask import current_app as app
from ..models import db, User
from datetime import datetime as dt
from flask import request, jsonify
from .db_interface import *
import json

users_blueprint = Blueprint('users_blueprint', __name__)


@users_blueprint.route('/users', methods=['POST'])  # create new user
def create_user_route():
    return create_user()


@users_blueprint.route('/users', methods=['PUT'])  # update a user
def update_user_route():
    return update_user()


@users_blueprint.route('/users/<user_id>', methods=['GET'])  # get a user
def get_user_route(user_id):
    return get_user(user_id)
