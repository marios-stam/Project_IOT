from flask import Blueprint, make_response
from flask import current_app as app
from flask.json import _dump_arg_defaults
from ..models import db, Truck
from datetime import datetime as dt
from flask import request, jsonify


def get_truck(truck_id=None):
    result = db.session.query(Truck).filter(Truck.id == truck_id).all()
    if(len(result) == 0):
        return make_response(f"No truck found with ID: {truck_id}")
    else:
        print(f"Gettind data of truck: {truck_id} ...")
        data = result[0].__dict__
        data.pop('_sa_instance_state')

        data_json = jsonify(data)

        return make_response(data_json)


def update_truck(truck_id=None):
    data = request.get_json()
    id = data['id']
    result = db.session.query(Truck).filter(Truck.id == id).all()
    if(len(result) == 0):
        return create_truck(data)

    print(f"Updating truck with ID:{id} ...")
    for key, value in data.items():
        if key == 'created' or key == 'updated':
            result[0].updated = dt.now()
            continue

        setattr(result[0], key, value)

    db.session.commit()

    return make_response(f"Updated truck with ID:{id}")


def create_truck(data=None):
    if data == None:
        data = request.get_json()

    data['updated'] = dt.now()  # set created date
    new_truck = Truck(**data)

    # add to database
    db.session.add(new_truck)
    db.session.commit()
    return make_response(f"New truck created with ID:{new_truck.id}")


def get_all_reports():
    print("Getting all Reports")  # get bin

    result = db.session.query(Bin).all()
    if(len(result) == 0):
        return make_response(f"No bin found!")

    bins = []
    for i in range(len(result)):
        bin = result[i].__dict__
        bin.pop('_sa_instance_state')

        bins.append(bin)

    return jsonify(bins)
