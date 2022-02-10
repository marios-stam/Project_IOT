from flask import request, make_response
from ..models import db, Bounty
from flask import jsonify
from datetime import datetime as dt
from ..utils import diff_time
from ..__config__ import REFRESH_INTERVAL, NUM_MEASUREMENTS
import geopy.distance
from datetime import datetime


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


def update_bounty(data=None):
    if data is None:
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


def get_uncompleted_bounties_in_radius():
    # Getting all bounties within radius
    # pos--> (long, lat)
    # radius--> in km

    # get data from json
    data = request.get_json()
    pos = (data['long'], data['lat'])
    radius = data['radius']

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


def assign_bounty(bounty_id, usr_id):
    # Please fix... this won't work
    if get_bounty(bounty_id).json is None:
        # Return HTTP code 404
        return make_response("ERROR")

    update_bounty({
        'id': bounty_id,
        'time_assigned': datetime.now(),
        'assigned_usr_id': usr_id
    })

    return make_response(f"Succesfully assigned {usr_id} to bounty {bounty_id}")


def complete_bounty(bounty_id, usr_id):
    if get_bounty(bounty_id).json['usr_id'] != usr_id:
        # Return HTTP code 403
        return make_response("ERROR")

    update_bounty({
        'id': bounty_id,
        'completed': True
    })

    return make_response(f"Succesfully assigned {usr_id} to bounty {bounty_id}")


def get_uncompleted_bountries_of_user(usr_id):
    result = db.session.query(Bounty).filter(
        Bounty.usr_id == usr_id).filter(Bounty.completed == False).all()

    if(len(result) == 0):
        return make_response(f"No uncompleted bounty found for user with user_id:", usr_id, "!")

    bounties = []
    for i in range(len(result)):
        bounty = result[i].__dict__
        bounty.pop('_sa_instance_state')

        bounties.append(bounty)

    return jsonify(bounties)
