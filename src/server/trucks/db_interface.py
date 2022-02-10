from flask import Blueprint, make_response
from flask import current_app as app
from flask.json import _dump_arg_defaults

from server.trucks.truck_routing.example_usage import fleet_route_optimising
from ..models import db, Truck
from datetime import datetime as dt
from flask import request, jsonify
from ..bins.db_interface import get_bins_by_status
from .truck_routing.example_usage import fleet_route_optimising


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


def get_all_trucks():
    print("Getting all Trucks")

    result = db.session.query(Truck).all()
    if(len(result) == 0):
        return make_response(f"No truck found!")

    trucks = []
    for i in range(len(result)):
        truck = result[i].__dict__
        truck.pop('_sa_instance_state')

        trucks.append(truck)

    return jsonify(trucks)


def get_all_available_trucks():
    result = db.session.query(Truck).filter(Truck.status == "available").all()
    if(len(result) == 0):
        return None

    trucks = []
    for i in range(len(result)):
        truck = result[i].__dict__
        truck.pop('_sa_instance_state')

        trucks.append(truck)

    return trucks


def get_trucks_routing():
    # get  trucks where status is available
    trucks = get_all_available_trucks()
    if trucks == None:
        return make_response(f"No available truck found!")
    trucks = [(truck.id, truck.long, truck.lat) for truck in trucks]

    # get all bins that need service from a truck
    # not sure if this is the right status
    bins = get_bins_by_status("need_truck")
    if bins == None:
        return make_response(f"No bin needs truck service!")

    bins = [(bin.long, bin.lat) for bin in bins]

    # solve travellings salesman problem and get routes for each truck
    fleet_route_optimising(trucks, bins)
