from flask import request, make_response
from ..models import db, Bounty
from flask import jsonify
from datetime import datetime as dt
from ..utils import diff_time
from ..__config__ import REFRESH_INTERVAL, NUM_MEASUREMENTS
import geopy.distance


def get_bounty(bounty_id=None):
    result = db.session.query(Bounty).filter(Bounty.id == bounty_id).all()
    if(len(result) == 0):
        return make_response(f"No bounty found with ID: {bounty_id}")
    else:
        print(f"Gettind data of bounty: {bounty_id} ...")
        data = result[0].__dict__
        data.pop('_sa_instance_state')

        data_json = jsonify(data)

        return make_response(data_json)


def update_bounty(bounty_id=None):
    data = request.get_json()
    id = data['id']
    result = db.session.query(Bounty).filter(Bounty.id == id).all()
    if(len(result) == 0):
        return create_bounty(data)

    print(f"Updating bounty with ID:{id} ...")
    for key, value in data.items():
        if key == 'created' or key == 'updated':
            result[0].updated = dt.now()
            continue

        setattr(result[0], key, value)

    db.session.commit()

    return make_response(f"Updated bounty with ID:{id}")


def create_bounty(data=None):
    if data == None:
        data = request.get_json()

    data['timestamp'] = dt.now()  # set created date
    data['time_assigned'] = dt.now()  # set created date

    new_bounty = Bounty(**data)

    # add to database
    db.session.add(new_bounty)
    db.session.commit()
    return make_response(f"New bounty created with ID:{new_bounty.id}")


def get_all_bounties():
    print("Getting all Bounties")

    result = db.session.query(Bounty).all()
    if(len(result) == 0):
        return make_response(f"No bounty found!")

    bounties = []
    for i in range(len(result)):
        bounty = result[i].__dict__
        bounty.pop('_sa_instance_state')

        bounties.append(bounty)

    return jsonify(bounties)


def get_uncompleted_bounties_in_radius(pos, radius):
    # Getting all bounties within radius
    # pos--> (long, lat)
    # radius--> in km

    result = db.session.query(Bounty).filter(Bounty.completed == False).all()

    if(len(result) == 0):
        return make_response(f"No bounty found!")

    bounties = []
    for i in range(len(result)):
        bounty = result[i].__dict__
        bounty_pos = (bounty['long'], bounty['lat'])
        distance = geopy.distance.distance(pos, bounty_pos).km

        if distance <= radius:
            bounty.pop('_sa_instance_state')
            bounties.append(bounty)

    return jsonify(bounties)
