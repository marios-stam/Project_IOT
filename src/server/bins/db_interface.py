from flask import Blueprint, make_response
from flask import current_app as app
from ..models import db, Bin
from datetime import datetime as dt
from flask import request, jsonify
import geopy.distance


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
    longtitude = data['longtitude']
    latitude = data['latitude']

    updated = dt.now()

    print("status:", status)
    print("fullness:", fullness)
    print("longtitude:", longtitude)
    print("latitude:", latitude)
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

    # data['updated'] = dt.now()  # set created date
    new_bin = Bin(**data)

    # add to database
    db.session.add(new_bin)
    db.session.commit()
    return make_response(f"New bin created with ID:{new_bin.entry_id}")


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


def get_bins_by_status(status):
    # Getting all bins with 'status' field is same to parameter status
    result = db.session.query(Bin).filter(Bin.status == status).all()
    if(len(result) == 0):
        return []

    bins = []
    for i in range(len(result)):
        bin = result[i].__dict__
        bin.pop('_sa_instance_state')

        bins.append(bin)

    return bins


def get_bins_in_radius(pos, radius):
    # Getting all bins within radius
    # pos--> (long, lat)
    # radius--> in km

    result = db.session.query(Bin).all()
    if(len(result) == 0):
        return make_response(f"No bin found!")

    bins = []
    for i in range(len(result)):
        bin = result[i].__dict__
        bin_pos = (bin['long'], bin['lat'])
        distance = geopy.distance.distance(pos, bin_pos).km

        if distance <= radius:
            bin.pop('_sa_instance_state')
            bins.append(bin)

    return jsonify(bins)


def get_bin_history(id, n):
    # Getting last n bins of a specific bin id
    result = db.session.query(Bin).filter(
        Bin.id == id).order_by(Bin.updated.desc()).limit(n).all()

    bins = []
    for i in range(len(result)):
        bin = result[i].__dict__
        bin.pop('_sa_instance_state')
        bins.append(bin)

    return jsonify(bins)
