from flask import Blueprint, make_response
from flask import current_app as app
from ..models import db, Bin
from datetime import datetime as dt
from flask import request, jsonify
from .db_interface import tested

bins_blueprint = Blueprint('bins_blueprint', __name__)


@bins_blueprint.route('/test')
def test():
    return tested()


@bins_blueprint.route('/test/bin')  # create new bin
def create_bin(id=None, status=None, fullness=None, updated=None, position=None):
    print("Create new bin")
    if id is None or status is None or fullness is None or updated is None or position is None:
        response = "TEST BIN CALLED"
        id = 99
        status = 1
        fullness = 0
        updated = dt.now()
        position = "x:55 y:55"

    new_bin = Bin(
        id=id,
        status=status,
        fullness=fullness,
        updated=None,
        position=position
    )

    db.session.add(new_bin)  # Adds new User record to database
    db.session.commit()  # Commits all changes

    response += f"{new_bin} successfully created/updated!"

    return make_response(response)


@bins_blueprint.route('/bins', methods=['POST'])  # update a bin
def parse_bin(bin_id=None):
    id = request.args.get('id')
    status = request.args.get('status')
    fullness = request.args.get('fullness')
    position = request.args.get('position')
    updated = request.args.get('updated')

    result = db.session.query(Bin).filter(Bin.id == 0).all()
    if(len(result) == 0):
        create_bin(id, status, fullness, updated, position)
    else:
        result[0].fullness = fullness
        result[0].status = status
        result[0].position = position
        result[0].updated = updated

    print("Parsing new Bin")  # parse bin
    return make_response("POST called")


@bins_blueprint.route('/bins/<bin_id>', methods=['GET'])  # get a bin
def get_bin(bin_id=None):
    print("Getting Bin")  # get bin
    # bin_id = request.args.get('id', type=str)

    result = db.session.query(Bin).filter(Bin.id == bin_id).all()
    if(len(result) == 0):
        return make_response(f"No bin found with ID: {bin_id}")
    else:
        print(f"Gettind data of bin: {bin_id} ...")

        data_json = jsonify(
            fullness=result[0].fullness,
            status=result[0].status,
            position=result[0].position,
            updated=result[0].updated
        )

    return make_response(data_json)
