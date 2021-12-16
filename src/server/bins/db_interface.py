from flask import Blueprint, make_response
from flask import current_app as app
from ..models import db, Bin
from datetime import datetime as dt
from flask import request, jsonify


def tested():
    return "Tested"


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


def update_bin(bin_id=None):
    data = request.get_json()
    id = data['id']
    status = data['status']
    fullness = data['fullness']
    position = data['position']
    updated = dt.now()

    print("status:", status)
    print("fullness:", fullness)
    print("position:", position)
    print("updated:", updated)

    result = db.session.query(Bin).filter(Bin.id == id).all()
    if(len(result) == 0):
        return create_bin(data)
    else:
        result[0].fullness = fullness
        result[0].status = status
        result[0].position = position
        result[0].updated = updated

    # update database
    db.session.commit()
    return make_response("PUT called")


def create_bin(data=None):
    if data == None:
        data = request.get_json()

    id = data['id']
    status = data['status']
    fullness = data['fullness']
    position = data['position']
    updated = dt.now()

    print("status:", status)
    print("fullness:", fullness)
    print("position:", position)
    print("updated:", updated)

    response = ""
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
        updated=dt.now(),
        position=position
    )

    db.session.add(new_bin)  # Adds new User record to database
    db.session.commit()  # Commits all changes

    response += f"{new_bin} successfully created"

    return make_response(response)
