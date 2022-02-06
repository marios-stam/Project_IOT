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
        data = result[0].__dict__
        data.pop('_sa_instance_state')

        data_json = jsonify(data)

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

    print(f"Updating bin with ID:{id} ...")
    for key, value in data.items():
        if key == 'created' or key == 'updated':
            result[0].updated = dt.now()
            continue

        setattr(result[0], key, value)

    db.session.commit()

    return make_response(f"Updated bin with ID:{id}")


def create_bin(data=None):
    if data == None:
        data = request.get_json()

    data['updated'] = dt.now()  # set created date
    new_bin = Bin(**data)

    # add to database
    db.session.add(new_bin)
    db.session.commit()
    return make_response(f"New bin created with ID:{new_bin.id}")


def get_all_bins():
    print("Getting all Bins")  # get bin

    result = db.session.query(Bin).all()
    if(len(result) == 0):
        return make_response(f"No bin found!")

    bins = []
    for i in range(len(result)):
        bin = result[i].__dict__
        bin.pop('_sa_instance_state')

        bins.append(bin)

    return jsonify(bins)
