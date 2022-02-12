from flask import make_response
from ..models import db, Bin
from datetime import datetime as dt
from flask import request, jsonify
import geopy.distance
from datetime import datetime
from ..bounty.db_interface import create_bounty
from ..constants import consts


def tested():
    return "Tested"


def get_bin(bin_id=None):
    print("Getting Bin")  # get bin
    # bin_id = request.args.get('id', type=str)

    result = db.session.query(Bin).filter(Bin.sensor_id == bin_id).order_by(Bin.timestamp.desc()).limit(1).all()
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

    result = db.session.query(Bin).filter(Bin.sensor_id == id).all()
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

    if data['fall_status'] or data['fire_status'] or data['fire_status'] < consts['BATTERY_THRESHOLD']:
        prev = get_bin(data['sensor_id']).json

    if data['fill_level'] > consts['FILL_CRITICAL']:
        data['status'] = 'need_truck'

    if data['fall_status'] and not prev['fall_status']:
        print("Bin fell")
        create_bounty({
            'timestamp': data['timestamp'],
            'long': data['long'],
            'lat': data['lat'],
            'bin_id': data['sensor_id'],
            'message': 'Bin has been tipped over! Please turn it back normally.',
            'type': 'fall',
            'points': consts['FALL_POINTS'],
            'completed': False
        })

    if data['fire_status'] and not prev['fire_status']:
        print("Bin on fire")
        create_bounty({
            'timestamp': data['timestamp'],
            'long': data['long'],
            'lat': data['lat'],
            'bin_id': data['sensor_id'],
            'message': 'Bin is on fire! Please put it out and call proper authorities.',
            'type': 'fire',
            'points': consts['FIRE_POINTS'],
            'completed': False
        })

    if data['battery'] <= consts['BATTERY_THRESHOLD'] and prev['battery'] > consts['BATTERY_THRESHOLD']:
        print("Bin low battery")
        create_bounty({
            'timestamp': data['timestamp'],
            'long': data['long'],
            'lat': data['lat'],
            'bin_id': data['sensor_id'],
            'message': 'Sensor battery is low on power! Please charge.',
            'type': 'battery',
            'points': consts['CHARGE_POINTS'],
            'completed': False
        })

    # data['updated'] = dt.now()  # set created date
    new_bin = Bin(**data)

    # add to database
    db.session.add(new_bin)
    db.session.commit()
    return make_response(f"New bin created with ID:{new_bin.entry_id}")


def get_all_bins():
    print("Getting all Bins")  # get bin

    cte = (db.session.query(Bin.sensor_id, db.func.max(Bin.timestamp).label('max_time')).group_by(Bin.sensor_id).cte(name='cte'))
    result = db.session.query(Bin).join(cte, db.and_(
        Bin.sensor_id == cte.c.sensor_id,
        Bin.timestamp == cte.c.max_time
    )).all()

    # for bin in result:
    #     print(bin.sensor_id, " --> ", bin.timestamp)

    bins = []
    for i in range(len(result)):
        bin = result[i].__dict__
        bin.pop('_sa_instance_state')

        bins.append(bin)

    return jsonify(bins)


# This is buggy but not used anywhere
def get_bins_by_status(status, get_latest_values=True):
    # Getting all bins with 'status' field is same to parameter status
    if get_latest_values:
        result = db.session.query(Bin).filter(
            Bin.status == status).order_by(Bin.timestamp.desc()).first()  # get the latest record
    else:
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

    result = get_all_bins().json
    if(len(result) == 0):
        return make_response(f"No bin found!")

    bins = []
    for bin in result:
        bin_pos = (bin['long'], bin['lat'])
        distance = geopy.distance.distance(pos, bin_pos).km

        if distance <= radius:
            # bin.pop('_sa_instance_state')
            bins.append(bin)

    return jsonify(bins)


def get_bin_history(id, n):
    # Getting last n bins of a specific bin id
    result = db.session.query(Bin).filter(
        Bin.sensor_id == id).order_by(Bin.timestamp.desc()).limit(n).all()

    bins = []
    for i in range(len(result)):
        bin = result[i].__dict__
        bin.pop('_sa_instance_state')
        bins.append(bin)

    return jsonify(bins)
